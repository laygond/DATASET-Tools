# -----------------------------
#   USAGE
# -----------------------------
# python extract_json_object.py --input Weapon-images
#
# DESCRIPTION:
# All objects have their own json files. This scripts combines all gun instances
# in an image into a single json file. For every image in a given directory it
# will output one json file. 
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# NOTE: 
# An image can have several object instances. Every object might be formed by
# several contour sets (contours might be split in parts due to occlusion, etc)
# ------------------------------

# Import the necessary packages
import json
from glob import glob
from imutils import paths
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" directory to json files and images")
args = vars(ap.parse_args())

# Grab all images in directory
imagePaths = list(paths.list_images(args["input"]))

# For every image create single json file to store all gun instances
for imagePath in imagePaths:

    gun_dict = {
        "imgfile" : imagePath.split('/')[-1],
        "source"  : imagePath.split('/')[-2],
        "height"  : 720,
        "width"   : 1280,
        "name"    : 'gun',   
        "instances": []     # if empty then no instances
    } 
    # Grab paths to objects inside an image
    img_json_obj_paths = glob(imagePath.split("original")[0] + '*.json')
    try:
        img_json_obj_paths.remove(imagePath.split("original")[0] + 'allguns.json') # in case it already exists
    except:
        pass

    # Collect contours from gun objects in an image
    for obj_path in img_json_obj_paths:
        annotations = json.load(open(obj_path))
        if annotations['objectId'] == 2998: # gun ID
            gun_dict['instances'].append(annotations['contours'])

    # Write to json file and move to directory
    with open(imagePath.split("original")[0]+ 'allguns.json', "w") as outfile:  
        json.dump(gun_dict, outfile) 