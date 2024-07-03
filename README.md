# Style Transfer

This project uses Streamlit to deploy a machine learning model into a web application.

## Description

The app takes 2 images as input. Then the ML model transfers the style from one image to the other.
VGG19 pretrained model is used as a backbone.

A user queue feature is also implemented.

## Features

- Upload 2 images
- Choose the number of epochs
- Transfer the style from one image to the other
- Add images to the processing queue

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/neurokind/style-transfer-app.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run main.py
   ```
4. Open the application in a web browser at `http://localhost:8501`.

Or activate Docker image using the Dockerfile:

1. Run the following command from the app/ directory on your server to build the image:
   ```
   docker build -t streamlit .
   ```
2. Run the streamlit container by executing:
   ```
   docker run -p 8501:8501 streamlit
   ```
3. Access the app in a browser at:
   ```
   http://0.0.0.0:8501 or http://localhost:8501
   ```

## Technologies

- Python
- Streamlit
- Torch
- Docker
- Machine Learning (style transfer model)
