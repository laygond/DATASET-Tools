# -----------------------------
#   USAGE
# -----------------------------
# python json_splitter.py --input 'Weapon-images-outdoor/*allguns.json' --tag 'outdoor_' -c 0.15
#
# DESCRIPTION:
# Creates a copy of the annotation data but split in the following way:
# - split_data
#     - train
#         - data1.json
#         - data2.json
#         - ...
#     - val
#         - data3.json
#         - data4.json
#         - ...
# It will split data with 20% in validation by default (unless specified) and will create
# the corresponding directories wherever the script is run (be careful). If directory
# already exists then it will just add the data. Since data coming from different 
# datasets may have the same name ,e.g IMG_data_00001, a tag can be appended to the name
# when copying. Also, the input accepts the use of wildcards (*) see USAGE example.
#
# Author: Bryan Laygond
# Website: http://www.laygond.com


# Import modules
from random import random
import os
from glob import glob
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" Files from where to extract")
ap.add_argument("-c", "--threshold", type=float, default=0.2,
	help=" Data split threshold between 0-1")
ap.add_argument("-t", "--tag", type=str, default="",
	help=" optional tag to differentiate incoming data")
args = vars(ap.parse_args())

# Verify script Parameters
assert args["threshold"] >0 and args["threshold"] <1,"threshold must be between 0-1"

# Path to annotations
annotation_files = glob(args["input"])

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

# Helper function since some file names have spaces
def quote(s):
    """
    Adds single quotes to incoming string
    """
    return "\'"+str(s)+"\'"

# Split Data (20% in validation unless specified)
for ann_file in annotation_files:
    file_name = ann_file.split('/')[-1]
    # Data goes to Validation folder if ...
    if random() < args["threshold"]:
        os.system("cp "+ quote(ann_file) +" "+ quote("split_data/val/"+args["tag"]+file_name) )
    else:
        os.system("cp "+ quote(ann_file) +" "+ quote("split_data/train/"+args["tag"]+file_name) ) 

