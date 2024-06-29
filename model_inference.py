from PIL import Image, ImageDraw


class ModelInference():
    def edit_image(self, img):
        img = Image.open(img)
        
        # Создаем объект ImageDraw, связанный с изображением
        draw = ImageDraw.Draw(img)

        # Начертить линию (начальные координаты, конечные координаты, цвет)
        draw.line((100, 100, 500, 500), fill="red", width=20)
            
            
        return img
    
    
def inference_edit_image(image):
    model_handler = ModelInference()
    image = model_handler.edit_image(image)
    
    return image
