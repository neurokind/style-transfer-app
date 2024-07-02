# -*- coding: utf-8 -*-
import torch
import torch.optim as optim
from torchvision import transforms, models
from PIL import Image


"""Methods for loading and normalising images and converting these back:"""

def load_image(img_path, max_size=400):
    image = Image.open(img_path).convert('RGB')

    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)

    in_transform = transforms.Compose([
        transforms.Resize((size, size)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))])

    image = in_transform(image).unsqueeze(0)
    return image


def im_convert(tensor):
    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze()
    image = image.transpose(1, 2, 0)
    image = image * (0.229, 0.224, 0.225) + (0.485, 0.456, 0.406)
    image = image.clip(0, 1)
    return image


def get_features(image, model, layers=None):
  if layers is None:
    layers = {'0': 'conv1_1',
              '5': 'conv2_1',
              '10': 'conv3_1',
              '19': 'conv4_1',
              '21': 'conv4_2', # Content representation
              '28': 'conv5_1'}

  features = {}
  x = image
  for name, layer in model._modules.items():
    x = layer(x)
    if name in layers:
      features[layers[name]] = x

  return features


def gram_matrix(tensor):
  _, d, h, w = tensor.size()
  tensor = tensor.view(d, h * w)
  gram = torch.mm(tensor, tensor.t())
  return gram
        

def inference_edit_image(content_image, style_image, epochs):
    # Set device here
    device = torch.device("cpu")
    
    # Prep (rescale, normalize) images
    content_image = load_image(content_image)
    style_image = load_image(style_image)
    
    """Loading the model vgg19 and determining the layers to calculate the losses:"""

    vgg = models.vgg19(weights=models.VGG19_Weights.IMAGENET1K_V1).features

    for param in vgg.parameters():
        param.requires_grad_(False)

    vgg.to(device)
    
    """Get features from content and style and calculate Gram matrix for style:"""

    content_features = get_features(content_image, vgg)
    style_features = get_features(style_image, vgg)

    style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

    """Set target image and optimisator:"""

    target = content_image.clone().requires_grad_(True).to(device)

    style_weights = {'conv1_1': 1.0,
                    'conv2_1': 0.75,
                    'conv3_1': 0.2,
                    'conv4_1': 0.2,
                    'conv5_1': 0.2}

    content_weight = 1 # alpha
    style_weight = 1e6 # beta

    optimizer = optim.Adam([target], lr=0.4)

    """The style transfer:"""

    steps = epochs

    for i in range(1, steps+1):
        target_features = get_features(target, vgg)

        content_loss = torch.mean((target_features['conv4_2'] - content_features['conv4_2'])**2)

        style_loss = 0
        for layer in style_weights:
            target_feature = target_features[layer]
            target_gram = gram_matrix(target_feature)
            style_gram = style_grams[layer]
            layer_style_loss = style_weights[layer] * torch.mean((target_gram - style_gram)**2)
            b, d, h, w = target_feature.shape
            style_loss += layer_style_loss / (d * h * w)

        total_loss = content_weight * content_loss + style_weight * style_loss

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        print('Epoch: ', i)


        if  i % 5 == 0:
            print('Total loss: ', total_loss.item())
    
    target = Image.fromarray((im_convert(target) * 255).astype('uint8'))
    return target
    

if __name__ == "__main__":
    # Path to images
    content_image_path = 'img/content.jpg'
    style_image_path = 'img/waves.jpg'

    # Load images
    content_image = load_image(content_image_path)
    style_image = load_image(style_image_path)

    # Save the result
    target = inference_edit_image(content_image, style_image, 3)
    target.save("img/result.jpg")
