# Cropping Code

`crop_tiff_1280_720.py`

This code produces the crops of all the images in the directory that are tiff files.

First command line argument should be the directory with all the images in full size .tiff form. The second command line argument should be the parent directory you want the crops to go. The script will additionally create a directory called `cropped_images` for the images to go.

`original_annotation_script.py`

This code produces the crops of all the annotations files. 

First command line argument is the directory with the full size annotations. Second command line argument is the directory where all the **full size** maps are, do not point it at the cropped images.

It will create a sub directory in the folder where the annotations currently live called `cropped`.

**Converting To JPG**

Tensorflow Object Detection API requires that images are JPG, so run the following script to create JPGs within the `cropped_images` folder.

`convert_crops_to_jpeg.py` 

**Run this after you split the images as below.**

# Train Test Split Code

`create_train_test_split.py`

This file requires `sklearn`. Create copies of the images into new sub directories called `train_split` and `test_split`. Additionally two files called `train_split.txt` and `test_split.txt`, each containing the files in each. *(Can use to get the sizes of the splits)*

Each of the split directories will also have sub directories `annotations` and `images`. 

*Script to run*:
```shell
#!/bin/bash
python3 /home/sgkelley/pixel_link/create_train_test_split.py /mnt/nfs/scratch1/sgkelley/cropped_images /mnt/nfs/scratch1/sgkelley/crop\
ped
```

# Changes to Pixel Link Code

`dataset_factory.py`

This file is used to create the dataset in the correct format by Pixel Link itself. The only modification was to add the correct format for our maps.

**You must use the version of this file in this repo for pixel link to detect the dataset correctly**

The train and test split size is based on the size of the crops generated with 1280 x 720 images. If you have more or less those numbers should be changed.

To get the number of the splits, I just run `wc -l train_split.txt` and `wc -l test_split.txt`. 

*Snippet*:
```python
maptext = DatasetConfig(
    file_pattern = 'maps_%s.tfrecord',
    split_sizes = {
        'train': 13889,
        'test': 3473
    }
)
```

*Config Snippet*:
```python
datasets_map = {
    'icdar2013':icdar2013,
    'icdar2015':icdar2015,
    'scut':scut,
    'td500':td500,
    'tr400':tr400,
    'synthtext':synthtext,
    'maptext': maptext,
}
```


`map_to_tfrecord.py `

This file assumes that there exists a raw dataset in ICDAR 2015 format. To meet the requirements of the file, make sure that the 
line 63 points to the correct directory where you would like the TFRecord files. 

```python
output_dir = "/home/sgkelley/pixel_link/datasets"
```

Also make sure that lines 65 and 66 point to the correct train and test splits.

```python
train_split_dir = '/mnt/nfs/scratch1/sgkelley/cropped_images/train_split'
    test_split_dir = '/mnt/nfs/scratch1/sgkelley/cropped_images/test_split'
```

If you used the above scripts to generate the splits, **you will need to make sure that you subsequently convert the files to JPG**. 

*Correct Command*: 
```shell
#!/bin/bash                                  
python /home/sgkelley/pixel_link/datasets/map_to_tfrecord.py
```

`scripts/train.sh`

Minor changes made to the training script. Modify the file in the original pixel_link directory by using the file in this directory. 

*Snippet*: 
```shell
DATASET=maptext
DATASET_DIR=/mnt/nfs/scratch1/sgkelley/cropped_images/

python train_pixel_link.py \
            --train_dir=${TRAIN_DIR} \
            --num_gpus=${NUM_GPUS} \
            --learning_rate=1e-4\
            --gpu_memory_fraction=-1 \
            --train_image_width=1280 \
            --train_image_height=720 \
            --batch_size=${BATCH_SIZE}\
            --dataset_dir=${DATASET_DIR} \
            --dataset_name=${DATASET} \
            --dataset_split_name=train \
            --max_number_of_steps=100\
            --checkpoint_path=${CKPT_PATH} \
            --using_moving_average=1

python train_pixel_link.py \
            --train_dir=${TRAIN_DIR} \
            --num_gpus=${NUM_GPUS} \
            --learning_rate=1e-4\
            --gpu_memory_fraction=-1 \
            --train_image_width=1280 \
            --train_image_height=720 \
            --batch_size=${BATCH_SIZE}\
            --dataset_dir=${DATASET_DIR} \
            --dataset_name=${DATASET} \
            --dataset_split_name=train \
            --checkpoint_path=${CKPT_PATH} \
            --using_moving_average=1\
            2>&1 | tee -a ${TRAIN_DIR}/log.log
```

*Correct Command*:
```shell
#!/bin/bash          
/home/sgkelley/pixel_link/scripts/train.sh 0 4
```

## Testing

Pretrained Weights:

```shell
#!/bin/bash
/home/sgkelley/pixel_link/scripts/test.sh 3 /home/sgkelley/conv3_3/model.ckpt-38055 /home/sgkelley/data/ch4_test_images
```

Fine Tuned Weights:

Pixel Link logs many different checkpoints, and they are all useable. Simple follow the following format:

```shell
#!/bin/bash
/home/sgkelley/pixel_link/scripts/test.sh 0 /home/sgkelley/models/pixel_link/model.ckpt-XXX /mnt/nfs/scratch1/sgkelley/cropped_images/\
test_split/images
```

Where XXX is any of the model checkpoints you'd like to use. The model checkpoints are stored in `~/models/pixel_link`.