# -*- coding: utf-8 -*-
"""Capstone.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zb-03Kls_PyumMaZYfNFp6nREuPJ0V--
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Activation
from tensorflow.keras.utils import to_categorical
import tensorflow.keras.backend as K

import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
import pickle
import random

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
from packaging import version

from google.colab import drive
drive.mount('/content/drive')

dirtrain='/content/drive/MyDrive/Grapes Leaf disease detection/Grapes Leaves Dataset (images)/Grapes Leaves Dataset (images)/train'
dirtest='/content/drive/MyDrive/Grapes Leaf disease detection/Grapes Leaves Dataset (images)/Grapes Leaves Dataset (images)/test'
categories=["Black_rot","Esca_(Black_Measles)","Healthy","Leaf_blight_(Isariopsis_Leaf_Spot)"]

for c in categories:
    path=os.path.join(dirtrain,c)
    for i in os.listdir(path):
        img_array=cv2.imread(os.path.join(path,i))
        #print(len(img_array),len(img_array[0]),len(img_array[0][0]))
        print(img_array.shape)
        plt.imshow(img_array)
        plt.show()
        break
    break
print(os.listdir(path))

training_data = []
def create_training_data():
    count=[]
    for c in categories:
        path=os.path.join(dirtrain,c)#creating the path of each class (folder)
        class_num=categories.index(c)#label is equal to the position of the class in 'categories' variable
        c=0
        for i in os.listdir(path):
            c=c+1
            try:
                img_array=cv2.imread(os.path.join(path,i))#creating the path of each image
                training_data.append([img_array,class_num])
            except Exception as e:
                pass
        count.append(c)
    return count
count_train=create_training_data()

testing_data = []
def create_testing_data():
    count=[]
    for c in categories:
        path=os.path.join(dirtest,c)
        class_num=categories.index(c)
        c=0
        for i in os.listdir(path):
            c=c+1
            try:
                img_array=cv2.imread(os.path.join(path,i))
                #img_array=cv2.resize(img_array,(128,128))
                testing_data.append([img_array,class_num])
            except Exception as e:
                pass
        
        count.append(c)
    return count

count_test=create_testing_data()
print(img_array.shape)

print(len(training_data))
print(count_train)
print(len(testing_data))
print(count_test)

random.shuffle(training_data)
random.shuffle(testing_data)

x_train = []
y_train = []
x_test = []
y_test = []

for features, label in training_data:
    x_train.append(features)
    y_train.append(label)
x_train=np.array(x_train).reshape(-1,256,256,3)

x=cv2.resize(training_data[0][0],(256,256))
plt.imshow(x,cmap='gray')

for features, label in testing_data:
    x_test.append(features)
    y_test.append(label)
x_test=np.array(x_test).reshape(-1,256,256,3)

def save_training_data(x_train,y_train):
    pickle_out=open("x_train_coloured.pickle","wb")
    pickle.dump(x_train,pickle_out)
    pickle_out.close()
    pickle_out=open("y_train_coloured.pickle","wb")
    pickle.dump(y_train,pickle_out)
    pickle_out.close 
save_training_data(x_train,y_train)

def save_testing_data(x_test,y_test):
    pickle_out=open("x_test_coloured.pickle","wb")
    pickle.dump(x_test,pickle_out)
    pickle_out.close()
    pickle_out=open("y_test_coloured.pickle","wb")
    pickle.dump(y_test,pickle_out)
    pickle_out.close()
save_testing_data(x_test,y_test)

def load_data():
    pickle_in=open("x_train_coloured.pickle","rb")
    x_train=pickle.load(pickle_in)
    return x_train

K.clear_session()
model=Sequential() 
model.add(layers.Conv2D(32,(3,3),padding='same',input_shape=(256,256,3),activation='relu'))
model.add(layers.Conv2D(32,(3,3),activation='relu'))


model.add(layers.MaxPool2D(pool_size=(8,8)))

model.add(layers.Conv2D(32,(3,3),padding='same',activation='relu'))
model.add(layers.Conv2D(32,(3,3),activation='relu'))

model.add(layers.MaxPool2D(pool_size=(8,8)))

model.add(Activation('relu'))

model.add(Flatten())
model.add(layers.Dense(256,activation='relu'))
model.add(layers.Dense(4,activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

from tensorflow.keras.utils import plot_model
plot_model(model, to_file='model.png')

y_train_cat=to_categorical(y_train,4)

y_test_cat=to_categorical(y_test,4)

model.fit(x_train,y_train_cat,batch_size=32,
          epochs=10,verbose=1,validation_split=0.15,shuffle=True)

model.save("/content/drive/MyDrive/leaf_disease_coloured.h5")

path = '/content/drive/MyDrive/leaf_disease_coloured.h5'
new_model = keras.models.load_model(path)

loss, acc = new_model.evaluate(x_test,y_test_cat, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100*acc))

new_model=tf.keras.models.load_model("/content/drive/MyDrive/leaf_disease_coloured.h5")

d='/content/drive/MyDrive/Grapes Leaf disease detection/Grapes Leaves Dataset (images)/Grapes Leaves Dataset (images)/test/Black_rot/003d09ef-e16c-4e8a-badf-847d46cb3dc0___FAM_B.Rot 3184_final_masked.jpg'
img=cv2.imread(d)
#uncomment the below line if the image is not 256x256 by default
#img_array=cv2.resize(img_array,(256,256)) 
plt.imshow(img)

#reshaping the image to make it compatible for the argument of predict function
img=img.reshape(-1,256,256,3)
#predicting the class of the image
predict_class=np.argmax(new_model.predict(img), axis=1)
#will print a no. of the class to which the leaf belongs
print(predict_class)

#using the predict class as the index for categories defined at the beginning to display the name
print(categories[predict_class[0]])