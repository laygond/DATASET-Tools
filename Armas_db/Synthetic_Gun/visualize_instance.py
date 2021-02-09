# -----------------------------
#   USAGE
# -----------------------------
# python visualize_instance.py --input Weapon-images/weapon_9989_0.json
#
# DESCRIPTION:
# Visualize an instance mask by reading the 'contours' key from a json file
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
#
# ------------------------------

# Import the necessary packages
import os
import json
import numpy as np
import cv2
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help=" json file from where to extract contours")
args = vars(ap.parse_args())

# Read File
annotations = json.load(open(args["input"]))
contours = annotations['contours']
label    = annotations['tagName']
print("Class Name: ", label)

# Transform dictionary into numpy
#https://www.programmersought.com/article/7581250465/
polygons = []
for contour in contours:
    polygons.append( np.array( [[pts['x'],pts['y']] for pts in contour], dtype=np.int32))

# Display
img = np.zeros((720,1280), dtype=np.uint8)
cv2.fillPoly(img, polygons, 255)
cv2.imshow("Contours!!", img) 
cv2.waitKey(0)
