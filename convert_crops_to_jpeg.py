import numpy as np
import os
import cv2
import sys
from glob import glob
from PIL import Image

images_dir_path = sys.argv[1]

image_filenames = glob(os.path.join(images_dir_path, "*.tiff"))
if not os.path.exists(os.path.join(images_dir_path, "cropped_images_jpeg")):
    os.mkdir(os.path.join(images_dir_path, "cropped_images_jpeg"))

for i, image_file in enumerate(image_filenames):
    full_filename_no_extension = image_file[:-5]
    image = Image.open(image_file)
    image.mode = 'I'
    image.point(lambda i: i*(1./256)).convert('L').save(full_filename_no_extension + ".jpeg")
    os.remove(full_filename_no_extension)
