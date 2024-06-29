# Style Transfer

This project uses Streamlit to deploy a machine learning model into a web application.

## Description

The app takes 2 images as input. Then the ML model transfers the style from one image to the other.

A user queue feature is also implemented.

## Features

- Upload 2 images
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

## Technologies

- Python
- Streamlit
- Docker
- Machine Learning (style transfer model)
