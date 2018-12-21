import os
import sys
from sklearn.model_selection import train_test_split
from shutil import copyfile
from glob import glob

images_dir_path = sys.argv[1] ## path to cropped annotations
annotations_dir_path = sys.argv[2] ## path to cropped annotations

train_split_path = os.path.join(images_dir_path, "train_split")
test_split_path = os.path.join(images_dir_path, "test_split")

if not os.path.exists(train_split_path):
	os.mkdir(train_split_path)
	os.mkdir(os.path.join(train_split_path, "images"))
	os.mkdir(os.path.join(train_split_path, "annotations"))
if not os.path.exists(test_split_path):
	os.mkdir(test_split_path)
	os.mkdir(os.path.join(test_split_path, "images"))
	os.mkdir(os.path.join(test_split_path, "annotations"))

image_filenames = glob(os.path.join(images_dir_path, "*.jpg"))

get_image_name = lambda raw_file_name: raw_file_name.split(os.sep)[-1].split('.')[0][14:]

train_idx, test_idx = train_test_split(list(range(len(image_filenames))), test_size=0.2)

with open(os.path.join(images_dir_path, "train_split.txt"), 'w+') as train_file:
	for idx in train_idx:
		image_filename = image_filenames[idx]
		train_file.write("%s\n" % image_filename)
		copyfile(image_filename, os.path.join(train_split_path, "images", image_filename.split(os.sep)[-1]))
		image_name = get_image_name(image_filename)
		annotation_file_name = os.path.join(annotations_dir_path, "annotation_" + image_name + ".txt")
		copyfile(annotation_file_name, os.path.join(train_split_path, "annotations", "annotation_" + image_name + ".txt"))

with open(os.path.join(images_dir_path, "test_split.txt"), 'w+') as test_file:
	for idx in test_idx:
		image_filename = image_filenames[idx]
		test_file.write("%s\n" % image_filename)
		copyfile(image_filename, os.path.join(test_split_path, "images", image_filename.split(os.sep)[-1]))
		image_name = get_image_name(image_filename)
		annotation_file_name = os.path.join(annotations_dir_path, "annotation_" + image_name + ".txt")
		copyfile(annotation_file_name, os.path.join(test_split_path, "annotations", "annotation_" + image_name + ".txt"))
