import numpy as np
import tensorflow as tf
import cv2
from tensorflow import keras

model = tf.keras.models.load_model('./model.h5')

# Filepath of image to predict
img = cv2.imread("./gtsrb/26/00000_00001.ppm")

img = cv2.resize(img, (30, 30))
img = img.reshape(1, 30, 30, 3)
img = tf.cast(img, tf.float32)

print(np.argmax(model.predict(img)))
