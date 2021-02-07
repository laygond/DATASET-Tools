# -----------------------------
#   USAGE
# -----------------------------
# python split_id_and_annotation_per_label.py --label "/m/0gxl3" --subset train --input train-annotations-object-segmentation.csv 
#
# DESCRIPTION:
# Split IDs and annotations per label. Annotions and IDs per label are filtered from the input csv file.
# csv-label annotations and txt-label IDs files are created. 
# The subset field depends on where the input csv file comes from: train, validation, test  
# 
# NOTE: 
# An image can have multiple instances. Every row in annotation file is an instance.
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# ------------------------------

# Import the necessary packages
import csv
import argparse


# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--label", type=str,
	help="label of interest e.g. /m/0gxl3 ")
ap.add_argument("-i", "--input", type=str,
	help="annotations of all objects from subset")
ap.add_argument("-s", "--subset", type=str,
	help="Either train, validation, or test ")
args = vars(ap.parse_args())

# Read csv of all objects annotations
f = open(args["input"])
data = csv.DictReader(f) 

# Writer of csv-label annotations and txt-label IDs
writer = csv.DictWriter(open("m" + args["label"].split("/")[-1] + "_annotations.csv", 'w'), fieldnames=data.fieldnames)
f = open("downloader_IDs_for_m"+ args["label"].split("/")[-1]+"_"+args["subset"]+".txt",'w')

# Keep track of IDs per label since image can have multiple instances
image_IDs_label = []

# Read and Write per row
writer.writeheader()
for row in data:
    if args["label"] in row['LabelName']:
        print(row)
        # Write label annotation
        writer.writerow(row)

        # Add Image ID without duplicates 
        if row['ImageID'] in image_IDs_label:
            print("[INFO] Image already registered")
        else:
            print("[INFO] New image found")
            image_IDs_label.append(row['ImageID'])
            f.write(args["subset"]+"/"+row['ImageID']+"\n") # Format required by downloader.py

