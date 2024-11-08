import numpy as np
import cv2 

image_path = "./media/tile/tile (01)"

def load_images(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at Path {image_path} could not be loaded.\n Please check again!")