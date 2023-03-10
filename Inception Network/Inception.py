# -*- coding: utf-8 -*-
"""Inception.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZZhrmiczF-6wJK7ff7EjB481jzzBorbR

Inception Network (3 inception layers) implementation on MNIST dataset.
"""

#Change directory
import os
directory = "/content/drive/MyDrive/Digit_Classification_Project"
os.chdir(directory)

#Libraries
import numpy as np
import pandas as pd
from tensorflow.keras import losses
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Conv2D,concatenate,MaxPooling2D,Flatten,Dropout,Dense,Input
from keras.metrics import categorical_crossentropy
from keras.utils import to_categorical

#Importing Dataset
(x_train,y_train),(x_test,y_test) = tf.keras.datasets.mnist.load_data()

# Normalize pixel values
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

# Convert labels to one-hot encoded vectors
classes = 10

y_train = to_categorical(y_train, classes)
y_test = to_categorical(y_test, classes)

def inception_module(input_):
    # 1x1 convolution layer
    conv1x1 = Conv2D(64, (1, 1), padding='same', activation='relu')(input_)
    
    # 3x3 convolution layer
    conv3x3 = Conv2D(64, (3, 3), padding='same', activation='relu')(conv1x1)
    
    # 5x5 convolution layer
    conv5x5 = Conv2D(64, (5, 5), padding='same', activation='relu')(conv1x1)
    
    # Max pooling layer
    pool = MaxPooling2D((3, 3), strides=(1, 1), padding='same')(input_)
    
    # Concatenate the output of all the convolutional layers
    input_ = concatenate([conv1x1, conv3x3, conv5x5, pool], axis=-1)
    
    return input_

# Define the input tensor
input = Input(shape=(28, 28, 1))

# Add the first convolutional block

x = Conv2D(64, (7, 7), padding='same', activation='relu')(input)
x = MaxPooling2D((3, 3), strides=(1, 1), padding='same')(x)

# Add the first inception layer
x = inception_module(input)
x = Dropout(0.25)(x)

# Add the second inception layer
x = inception_module(x)
x = Dropout(0.25)(x)

# Add the third inception layer
x = inception_module(x)
x = Dropout(0.25)(x)

# Flatten the output of the second convolutional block
x = Flatten()(x)

#Add fully coneected layer
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)

x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)

# Add output layer
output = Dense(10, activation='softmax')(x)

#making the model
model = Model(input, output)

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#Fit the training dataset
batch_size = 256
epochs = 4
history = model.fit(x_train.reshape(-1, 28, 28, 1), y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

# Evaluate the model on the test set
score = model.evaluate(x_test.reshape(-1, 28, 28, 1), y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#Save the model
model.save("Inception.h5")