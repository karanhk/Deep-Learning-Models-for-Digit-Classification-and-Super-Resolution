# -*- coding: utf-8 -*-
"""lenet5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m-1vq740LXTgzMo8juI7IlNfDGNOucmj

Implementation of LeNet 5 on MNIST dataset.
"""

#Changing current working directory
import os
directory = "/content/drive/MyDrive/Digit_Classification_Project"
os.chdir(directory)

#Libraries
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.metrics import categorical_crossentropy
from keras.models import Sequential,Model
from keras.layers import Conv2D, AveragePooling2D, Dense, Flatten,Input,Dropout,concatenate
from tensorflow.keras import datasets, losses
import numpy as np

#Importing dataset
(x_train, y_train), (x_test, y_test)=tf.keras.datasets.mnist.load_data()

#Configuring x_train
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

# Convert labels to one-hot encoded vectors
classes = 10
y_train = to_categorical(y_train, classes)
y_test = to_categorical(y_test, classes)

# Define the input tensor
input = Input(shape=(28, 28, 1))

x = Conv2D(6, (5, 5), padding='same', strides=1, activation='tanh')(input) #5x5 Convolution
x = AveragePooling2D()(x) #Average Pooling
x = Conv2D(16,(5,5),padding='valid',strides=1,activation='tanh')(x) #5x5 Convolution
x = AveragePooling2D()(x) #Average Pooling
x = Conv2D(120,(5,5),strides=1,activation='tanh',padding='valid')(x) #5x5 Convolution
x = Flatten()(x) #Flattening
x = Dense(84,activation='tanh')(x) #Dense Layer

output = Dense(10,activation='softmax')(x) #Output Layer

# Define the model
model = Model(input, output)

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(x_train.reshape(-1, 28, 28, 1), y_train, batch_size=256, epochs=10, validation_split=0.1)

# Evaluate the model on the test set
score = model.evaluate(x_test.reshape(-1, 28, 28, 1), y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#Save the model
model.save("LeNet5.h5")