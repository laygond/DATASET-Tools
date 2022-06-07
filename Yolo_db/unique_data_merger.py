# -----------------------------
#   USAGE
# -----------------------------
# python unique_data_merger.py --src "/source/directory/" --dst "/destination/directory/" 
#
# DESCRIPTION:
# Merge image and label directories with no duplicates.
# Two different datasets often have same names for images (img001.jpg, img002.jpg, etc),
# images and labels will be renamed during the merge. Duplicate images will be later
# filtered and removed along with their labels.
# 
# NOTE:
# Absolute paths are required.
# It is assumed that src and dest have identical hierarchy directory:
# '.../train/dogs/img1.jpg' , '.../train/dog1.jpg' , etc 
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
# 
# ------------------------------

# Import the necessary packages
from imutils import paths
import cv2
import os
import shutil
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--flip", type=int,
	help="Include left-right flipped images as duplicates?")
ap.add_argument("-src", "--source", type=str,
	help="directory from which all data is acquired")
ap.add_argument("-dst", "--dest", type=str,
	help="directory that will add/receive data")
args = vars(ap.parse_args())

# Helper Functions:
def orb_sim(img1, img2, threshold = 50):
  """
  Compare images using ORB feature detectors.
  Returns percentage of similarity: 1.0 means
  identical & lower not similar.
  @threshold: from 0 to 100, the lower the closer the
              distance between features (more similar).  
  by Sreenivas Bhattiprolu (modified by Laygond)
  """
  # define ORB object
  orb = cv2.ORB_create()

  # detect keypoints and descriptors
  kp_a, desc_a = orb.detectAndCompute(img1, None)
  kp_b, desc_b = orb.detectAndCompute(img2, None)
  if desc_a is None or desc_b is None:
    return 0

  # define the bruteforce matcher object
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
  #perform matches. 
  matches = bf.match(desc_a, desc_b)
  if len(matches) == 0:
    return 0
  
  #Look for similar regions with distance < threshold. 
  similar_regions = [i for i in matches if i.distance < threshold] #the lower the more similar  
  return len(similar_regions) / len(matches) #Percentage of similar matches


def _remove(img_path, label_paths):
    f_name,f_ext = os.path.splitext(os.path.basename(img_path))
    os.remove(img_path)
    for l in label_paths:
        l_name,l_ext = os.path.splitext(os.path.basename(l))
        if l_name == f_name:
            os.remove(l)
            return


def remove_duplicates(img_paths, label_paths):
    print('[INFO] Filtering...')
    if len(img_paths) > 1 :
        for i in range(len(img_paths)-1):
            img1 = cv2.imread(img_paths[i])
            for j in range(i+1,len(img_paths)):
                img2 = cv2.imread(img_paths[j])
                
                similarity = orb_sim(img1, img2)
                if similarity > .95:
                    _remove(img_paths[j], label_paths)
                    continue

                if args['flip']:
                    similarity = orb_sim(img1, cv2.flip(img2,1))
                    if similarity > .95:
                        _remove(img_paths[j], label_paths)
    print('[INFO] Filtering. Done!')



# === Merge ===
assert args['source'] and args['dest']
print('[INFO] Merge Started...')
# Copy from src to dst according to their directory's structure
for dirpath, dirnames, filenames in os.walk(args['source']):
    for filename in filenames:
        f_name,f_ext = os.path.splitext(filename)
        new_name= f_name+'_'+f_ext
        relative_path = os.path.relpath(dirpath,args['source'])
        src_file = os.path.join(dirpath,filename)
        dst_file = os.path.join(args['dest'],relative_path, new_name)
        shutil.copyfile(src_file, dst_file)
# Remove duplicate images and label
img_paths = list(paths.list_images(args['dest']))            
label_paths = list(paths.list_files(args['dest'], validExts=(".txt",)))
remove_duplicates(img_paths, label_paths)
print('[INFO] Merge Complete!')
