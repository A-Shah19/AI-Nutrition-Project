import numpy as np
import math
from keras import applications
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical


def calculate_steps(filenames, batch_size):
  filenames_len = len(filenames)
  val = filenames_len / batch_size
  val_add = int(val) + 1
  return val_add

train_dir = 'data/train'
validation_dir = 'data/validation'

part1_train_generator = ImageDataGenerator(rescale=1.0/255).flow_from_directory(train_dir, target_size=(224, 224), batch_size=16, class_mode=None, shuffle=False)
part2_train_generator = ImageDataGenerator(rescale=1.0/255).flow_from_directory(train_dir, target_size=(224, 224), batch_size=16, class_mode='categorical', shuffle=False)
train_categorical_classes = to_categorical(part2_train_generator.classes, num_classes=8)

val_generator = ImageDataGenerator(rescale=1.0/255).flow_from_directory(validation_dir, target_size=(224, 224), batch_size=16, class_mode=None, shuffle=False)
validation_categorical_classes = to_categorical(val_generator.classes, num_classes=8)

vgg_model = applications.VGG16(include_top=False, weights='imagenet')

train_features_steps = calculate_steps(part1_train_generator.filenames, 16)
validation_features_steps = calculate_steps(val_generator.filenames, 16)

train_features = vgg_model.predict_generator(part1_train_generator, train_features_steps, verbose=1)

validation_features = vgg_model.predict_generator(val_generator, validation_features_steps, verbose=1)

train_features_shape = train_features.shape
train_input_shape = train_features_shape[1:]

model = Sequential()
model.add(Flatten(input_shape=train_input_shape))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_features, train_categorical_classes, epochs=50, batch_size=16, validation_data=(validation_features, validation_categorical_classes), verbose=1)

np.save('categories_dict.npy', val_generator.class_indices)
model.save_weights('weights.h5')

print(model.evaluate(validation_features, validation_categorical_classes, batch_size=16, verbose=1))
