# -*- coding: utf-8 -*-
"""digits_model_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DzpTlInwGFYO4I7QgYSz-MGbfDVJyA4F
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.4.1

tflite_model_name = 'digits_model'
c_model_name = 'digits_model'

import math
import numpy as np
from sklearn.datasets import load_digits
import tensorflow as tf
from tensorflow.keras import layers

#IMPORT DATA FILE
x_values, y_values = load_digits(return_X_y=True)

print(x_values.shape)
print(y_values.shape)

#NORMALIZATION
x_values /= x_values.max()

#BUILDING INPUT VECTOR
X_values = x_values.reshape((len(x_values), 8, 8, 1)) #For CNN model
print(X_values[0])

# ONE-HOT encoding
from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()
Y_values = enc.fit_transform(y_values[:, np.newaxis]).toarray()
print(Y_values)

num_classes = Y_values.shape[1]
print(num_classes)
num_features = X_values.shape[1:3]
print(num_features)

# Divide the data into train and test set (70:30)
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_values, Y_values, test_size = 0.3, random_state=25)

print(X_train.shape)
print(Y_train.shape)

print(X_test.shape)
print(Y_test.shape)

# Creating a CNN Model
model = tf.keras.Sequential()

# Convolution Layer
model.add(layers.Conv2D(8, kernel_size=(3, 3),strides=(1,1), activation='relu', input_shape=(8, 8, 1))) # 8 no of 3x3 filters with strides=1

# Pooling Layer
model.add(layers.MaxPooling2D((2, 2))) #Max pooling 2x2

# Flatten the output
model.add(layers.Flatten())

# Fully connected layer
model.add(layers.Dense(16, activation='relu'))  # Fully connected layer with 16 neurons

# Output layer
model.add(layers.Dense(num_classes, activation='softmax'))  # Output layer of 10 outputs

model.summary()

# Compilation
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer = 'adam')

# Train model
model.fit(X_train, Y_train, epochs=50, batch_size=20, validation_split=0.1)

(loss,accuracy)=model.evaluate(X_test,Y_test, batch_size=10,verbose=1)
accuracy*100

#Real time testing
new_img = X_test[0,:,:]   #[5.4, 3, 4.5,1.5]
img = np.reshape(new_img, (1,8,8,1))
Y_pred = np.argmax(model.predict(img))
print(Y_pred)

import matplotlib.pyplot as plt
new_img1 = np.reshape(new_img,(8,8))
plt.imshow(new_img1)
print(repr (np.reshape(new_img,(64))))

# Convert Keras model to a tflite model

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model to disk
open(tflite_model_name + '.tflite', "wb").write(tflite_model)

# Function: Convert some hex value into an array for C programming
def hex_to_c_array(hex_data, var_name):

  c_str = ''

  # Create header guard
  c_str += '#ifndef ' + var_name.upper() + '_H\n'
  c_str += '#define ' + var_name.upper() + '_H\n\n'

  # Add array length at top of file
  c_str += '\nunsigned int ' + var_name + '_len = ' + str(len(hex_data)) + ';\n'

  # Declare C variable
  c_str += 'unsigned char ' + var_name + '[] = {'
  hex_array = []
  for i, val in enumerate(hex_data) :

    # Construct string from hex
    hex_str = format(val, '#04x')

    # Add formatting so each line stays within 80 characters
    if (i + 1) < len(hex_data):
      hex_str += ','
    if (i + 1) % 12 == 0:
      hex_str += '\n '
    hex_array.append(hex_str)

  # Add closing brace
  c_str += '\n ' + format(' '.join(hex_array)) + '\n};\n\n'

  # Close out header guard
  c_str += '#endif //' + var_name.upper() + '_H'

  return c_str



# Write TFLite model to a C source (or header) file
with open(c_model_name + '.h', 'w') as file:
  file.write(hex_to_c_array(tflite_model, c_model_name))

cfile = open(c_model_name + '.h')
cfile.read()

