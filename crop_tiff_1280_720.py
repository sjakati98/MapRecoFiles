import numpy as np
import os
import cv2
import sys
from glob import glob


images_dir_path = sys.argv[1]
save_to_dir_path = sys.argv[2]

image_filenames = glob(os.path.join(images_dir_path, "*.tiff"))

if not os.path.exists(save_to_dir_path):
	os.mkdir(save_to_dir_path)
if not os.path.exists(os.path.join(save_to_dir_path, "cropped_images")):
	os.mkdir(os.path.join(save_to_dir_path, "cropped_images"))
for i, image_file in enumerate(image_filenames):
	#print( i, image_file)
	image_original_name = image_file
	file_path_pieces = image_original_name.split(os.sep)
	file_stripped_name = file_path_pieces[-1].split('.')[0]
	
	current_image = cv2.imread(image_file)
	(width, height, channels) = current_image.shape

	image_x_max = height 
	image_y_max = width

	image_crop_x = 1280
	x_0 = 0
	image_crop_y = 720
	y_0 = 0
	image_crop_step = 200

	for y_0 in range(0, image_y_max - image_crop_y, image_crop_step):
		for x_0 in range(0, image_x_max - image_crop_x, image_crop_step):
			save_to_image = os.path.join(save_to_dir_path, "cropped_images", ("cropped_image_%s_%d_%d.tiff" % (file_stripped_name, x_0 , y_0)))
			cropped = current_image[y_0:y_0+image_crop_y, x_0:x_0+image_crop_x]
			cv2.imwrite(save_to_image, cropped)
			if(x_0+image_crop_x > width):
				break
		if (y_0+image_crop_y > height):
                	break  
