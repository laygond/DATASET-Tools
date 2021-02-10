"""
The objective of this script is to split the data in the following way:

- split_data
    - train
        - data1.json
        - data2.json
        - ...
    - val
        - data3.json
        - data4.json
        - ...
NOTE:
  It will split data with 20% in validation and will create the corresponding
  directories wherever the script is run 

# Author: Bryan Laygond
# Website: http://www.laygond.com
"""

# Import modules
from random import random
import os
from glob import glob

# Path to annotations
annotation_files = glob('Weapon-images/*allguns.json')

# Create train and validation directories
try:
    os.mkdir("split_data")
except FileExistsError:
    print ("[INFO] split_data is ready already")
try:
    os.mkdir("split_data/val")
except FileExistsError:
    print ("[INFO] split_data/val is ready already")
try:
    os.mkdir("split_data/train")
except FileExistsError:
    print ("[INFO] split_data/train is ready already")    

# Split Data (20% in validation)
for ann_file in annotation_files:
    # Data goes to Validation folder if ...
    if random()<0.2:
        os.system("cp \'"+ ann_file + "\' split_data/val/")
    else:
        os.system("cp \'"+ ann_file + "\' split_data/train/")

