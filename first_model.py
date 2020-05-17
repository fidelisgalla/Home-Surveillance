# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:34:02 2020

@author: admin1
"""

#first CNN

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.layers import Flatten
from keras.layers import Dense

#build model
model = Sequential()
model.add(Conv2D(32,3,3,input_shape = (64,64,3), activation='relu'))

#model pooling
model.add(MaxPool2D(pool_size=(2,2)))

#model flattening
model.add(Flatten())

#dense layer
model.add(Dense(output_dim=128,activation='relu'))
model.add(Dense(output_dim=1,activation = 'sigmoid'))

#compiling the CNN
model.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics = ['accuracy'])

#DATA AUGMENTATION
from keras.preprocessing.image import ImageDataGenerator

train_data_gen = ImageDataGenerator(rescale = 1./255,shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
test_data_gen = ImageDataGenerator(rescale = 1./255)
path_test = 'C:\\Users\\admin1\\Downloads\\P14-Convolutional-Neural-Networks\\Convolutional_Neural_Networks\dataset\\test_set'
path_training = 'C:\\Users\\admin1\\Downloads\\P14-Convolutional-Neural-Networks\\Convolutional_Neural_Networks\\dataset\\training_set'

training_set = train_data_gen.flow_from_directory(path_training,class_mode='binary',target_size=(64,64),batch_size=64)
test_set = train_data_gen.flow_from_directory(path_test,class_mode='binary',target_size=(64,64),batch_size=64)

from IPython.display import display
from PIL import Image

model.fit_generator(training_set,steps_per_epoch=8000, epochs=10,validation_data=test_set,validation_steps=800)


