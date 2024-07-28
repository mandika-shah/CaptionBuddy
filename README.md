# CaptionX

CaptionX is a web application that generates captions for images using deep learning techniques. Built with Django, this project utilizes a pre-trained neural network model to provide descriptive captions for uploaded images.

## Table of Contents

- [Dataset](#dataset)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Ecountered Problems](#encountered-problems)

## Dataset
-The [Flickr8k dataset] is used for training and evaluating the image captioning system. It consists of 8,091 images, each with five captions describing the content of 
 the image. The dataset provides a diverse set of images with multiple captions per image, making it suitable for training caption generation models.

## Features

- User-friendly interface for easy image uploads.
- Generates captions for images using deep learning models.
- Supports various image formats (e.g., JPEG, PNG).
- Built-in error handling for unsupported file types and large files.

## Technologies Used

- Python 
- Django Framework
- TensorFlow (for the image captioning model)
- HTML/CSS/JavaScript (for frontend development)
- SQLite (for the database)

## Encountered Problems

- **Out of memory issue**:
  - Try lowering 'batch_size' parameter to reduce memory consumption.
- **Results may vary with each run**:
  - The results may vary slightly with each execution of the script.
- **Results lack a high degree of accuracy.**
