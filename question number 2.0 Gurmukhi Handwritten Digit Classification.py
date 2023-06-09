

import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import seaborn as sn
from matplotlib import pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
import os
import cv2





# Define the paths
train = 'train'
val = 'val'





# Set the path
data_dir = train
# Set the image size
img_size = (32, 32)
# Create empty lists
images = []
labels = []
#  each folder from '0' to '9' loop over
for label in range(10):
    folder_path = os.path.join(data_dir, str(label))
    #  each image in the folder
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file_path.endswith(('.tiff','.bmp')):
           # Load the image and resize it
           img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
           img = cv2.resize(img, img_size)
           # Append the image and label to the lists
           images.append(img)
           labels.append(label)

#  lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Save the arrays in NumPy format
np.save('x_train.npy', images)
np.save('y_train.npy', labels)





# Set the path to the folder containing the 'val' folder
data_dir_val = val
# Set the image size
img_size_val = (32, 32)
# Create empty lists
images_val = []
labels_val = []
# Loop over each folder from '0' to '9'
for label in range(10):
    folder_path = os.path.join(data_dir_val,str(label))
    # Loop over each image in the folder
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file_path.endswith(('.tiff','.bmp')):
            # Load the image and resize it to the desired size
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, img_size_val)
            # Append the image and label to the lists
            images_val.append(img)
            labels_val.append(label)

# Convert the lists to NumPy arrays
images_val = np.array(images_val)
labels_val = np.array(labels_val)
# Save the arrays in NumPy format
np.save('x_test.npy', images_val)
np.save('y_test.npy', labels_val)





# Load the dataset
x_train = np.load('x_train.npy')
y_train = np.load('y_train.npy')
x_test = np.load('x_test.npy')
y_test = np.load('y_test.npy')





# test the images are loaded correctly
print(len(x_train))
print(len(x_test))
x_train[0].shape
x_train[0]
plt.matshow(x_train[0])
plt.matshow(x_train[999])
print(x_train.shape)
print(x_test.shape)
y_train





# flatten the dataset i.e, change 2D to 1D
x_rail_flat = x_train.reshape(len(x_train),32*32)
x_test = x_test.reshape(len(x_test),32*32)
print(x_rail_flat.shape)
print(x_test.shape)
x_rail_flat[0]





# simple nn
# create a dense layer
# activation function is sigmoid
model = keras.Sequential([
 keras.layers.Dense(10, input_shape=(1024,),activation = 'sigmoid')
])
# compile the nn
model.compile(optimizer='adam',
 loss='sparse_categorical_crossentropy',
 metrics=['accuracy']
 )
# train the model
# 5 iterations done here
model.fit(x_rail_flat, y_train,epochs= 5)





# creating a simple nn
# create a dense layer
# activation function is sigmoid
model = keras.Sequential([
    keras.layers.Flatten(),
    keras.layers.Dense(10, input_shape=(1024,),activation = 'sigmoid')
    ])
# compile the nn
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
              )
# train the model
# some 10 iterations done here
model.fit(x_train, y_train,epochs= 10, validation_data=(x_test, y_test))










# now scale and try to check the accuracy, divide dataset by 255
x_train_t = x_train/255
x_test_scaled = x_test/255
model.fit(x_train_t, y_train,epochs= 10, validation_data=(x_test_scaled, y_test))





# Observation : we got better result for all iterations on scaling the training dataset




# evaluate test dataset
model.evaluate(x_test_scaled,y_test)










# in 1st Dense layer,the input is 32 x 32 = 1024 neurons, which will give 10 output(numbers from 0 to 9)

model2 = keras.Sequential([
    keras.layers.Flatten(),
    keras.layers.Dense(1024,input_shape=(1024,), activation='relu'),
    keras.layers.Dense(10, activation='softmax')
    ])
# compile the nn
model2.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
              )
# train the model
# some 10 iterations done here
history = model2.fit(x_train_t, y_train,epochs= 10, validation_data=(x_test_scaled, y_test))






model2.evaluate(x_test_scaled,y_test)






# redo the confusion matrix
# build confusion matrix

y_predicted = model2.predict(x_test_scaled)
y_predicted[0]
y_predicted_labels=[np.argmax(i) for i in y_predicted]
print(y_predicted_labels, len(y_predicted_labels))
conf_mat = tf.math.confusion_matrix(labels=y_test, predictions=y_predicted_labels)
conf_mat





plt.figure(figsize = (10,10))
sn.heatmap(conf_mat,annot=True,fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Actual')





# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)
# Plot the training and validation accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

