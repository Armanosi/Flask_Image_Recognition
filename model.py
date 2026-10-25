
"""Image preprocessing and prediction utilities."""

import numpy as np
from keras.models import load_model
from keras.utils import img_to_array
from PIL import Image

# Load the trained hand-sign recognition model.
model = load_model("digit_model.h5")


def preprocess_img(img_path):
    """Prepare an uploaded image for model prediction."""
    with Image.open(img_path) as image:
        rgb_image = image.convert("RGB")
        resized_image = rgb_image.resize((224, 224))
        image_array = img_to_array(resized_image) / 255.0

    return image_array.reshape(1, 224, 224, 3)


def predict_result(image):
    """Return the class with the highest prediction score."""
    predictions = model.predict(image)
    return np.argmax(predictions[0], axis=-1)
