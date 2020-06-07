import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    print("loading files...")

    for subdir, dir, files in os.walk("./gtsrb"):
        for file in files:
            img = cv2.imread(subdir + os.sep + file)
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            images.append(img)

            dir_name = subdir.split(os.sep)[-1]
            labels.append(dir_name)
    
    print("files successfully loaded")

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)

    model = tf.keras.models.Sequential([
        
        # Convolution, Pooling 1
        tf.keras.layers.Conv2D(32, (5, 5), input_shape=input_shape, activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # Convolution, Pooling 2
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten Layer
        tf.keras.layers.Flatten(),

        # Hidden Layer + Dropout 1
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Output
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=['accuracy']
    )

    model.summary()

    return model


if __name__ == "__main__":
    main()
