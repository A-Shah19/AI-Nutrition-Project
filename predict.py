from PIL import Image
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.utils.np_utils import to_categorical
import cv2


def predict_classes(image_paths):
	class_dict = np.load('categories_dict.npy').item()

	str_arr = []

	for image in image_paths:

		image_path = image
		print(image_path)

		image = load_img(image_path, target_size=(224, 224))
		image_arr = img_to_array(image)

		image_arr = image_arr / 255

		image_expanded = np.expand_dims(image_arr, axis=0)

		model = applications.VGG16(include_top=False, weights='imagenet')

		extract_features = model.predict(image_expanded)

		features_shape = extract_features.shape
		features_shape_input = features_shape[1:]

		model = Sequential()
		model.add(Flatten(input_shape=features_shape_input))
		model.add(Dense(256, activation='relu'))
		model.add(Dropout(0.5))
		model.add(Dense(8, activation='softmax'))

		model.load_weights('weights.h5')

		class_prediction = model.predict_classes(extract_features)

		class_index = class_prediction[0]

		for food_item, dict_index in class_dict.items():
			if dict_index == class_index:
				class_label = food_item

		str_arr.append(class_label)

	return(str_arr)


