# -----------------------------
#   USAGE
# -----------------------------
# python unique.py --input "/directory/duplicated/images" #FILTERING CASE
# python unique.py --src "/source/directory/images" --dst "/destination/directory/images" #TRANSFER CASE
#
# DESCRIPTION:
# Outputs image directories with no duplicate images.
# There are two cases: Filtering and Transfer
# In the case of filtering it removes all duplicate images under a directory.
# For Transfer it transfers a copy of all unique images between the two 
# directories to the destination directory 
# 
# NOTE:
# Absolute paths are required.
# It is assumed that src and dest have same hierarchy directory:
# '.../train/dogs/img1.jpg' or '.../train/dog1.jpg' 
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
# 
# ------------------------------

# Import the necessary packages
from imutils import paths
import cv2
import numpy as np
import os
import shutil
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
	help="directory for filtering duplicates")
ap.add_argument("-f", "--flip", type=int,
	help="Include left-right flipped images as duplicates")
ap.add_argument("-src", "--source", type=str,
	help="directory from which all unique images will be acquired")
ap.add_argument("-dst", "--dest", type=str,
	help="directory that will add/receive all unique images")
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


# Filtering Case
def filter_case(img_paths):
    print('[INFO] Filtering...')
    if len(img_paths) > 1 :
        for i in range(len(img_paths)-1):
            img1 = cv2.imread(img_paths[i])
            for j in range(i+1,len(img_paths)):
                img2 = cv2.imread(img_paths[j])
                
                similarity = orb_sim(img1, img2)
                #print(i,j,similarity)
                if similarity > .95:
                    os.remove(img_paths[j])
                    continue

                if args['flip']:
                    similarity = orb_sim(img1, cv2.flip(img2,1))
                    if similarity > .95:
                        os.remove(img_paths[j])
    print('[INFO] Filtering. Done!')


# Tranfer Case
# TODO: 
# Option# 2 Check time efficiency other way around -> imgs from src against 
#       dst and copy on the go (therefore must increase dst on every round)
# Option# 3 Send everything to dst(including duplicates) and then filter dst
def transfer_case(dir1, dir2):
    print('[INFO] Transfering unique images to destination...')
    if len(dir1) > 0:
        if len(dir2) == 0:
            shutil.copytree(args['source'], args['dest'], dirs_exist_ok=True)
        else: #compare imgs from dest against source if duplicate then
            indeces_to_remove=[]    #remove from src dir
            for i in range(len(dir2)):
                img_d2 = cv2.imread(dir2[i])
                for j in range(len(dir1)):
                    img_d1 = cv2.imread(dir1[j])
                    
                    similarity = orb_sim(img_d2, img_d1)
                    if similarity > .95:
                        indeces_to_remove.append(j)

                    if args['flip'] and similarity <= .95:
                        similarity = orb_sim(img_d2, cv2.flip(img_d1,1))
                        if similarity > .95:
                            indeces_to_remove.append(j)

            indeces_unique=np.arange(len(dir1))
            indeces_unique=np.delete(indeces_unique, indeces_to_remove)
            word_bank =['train','test','val','validation']
            up_1 = True if os.path.basename(os.path.dirname(dir1[0])) in word_bank else False
            up_2 = True if os.path.basename(os.path.dirname(os.path.dirname(dir1[0]))) in word_bank else False
            no_up = not up_1 and not up_2
            no_up = True if os.path.basename(args['dest']) in word_bank else no_up

            if no_up:
                for k in indeces_unique:
                    f_name,f_ext = os.path.splitext(os.path.basename(dir1[k]))
                    new_name= f_name+'_'+f_ext
                    dest_file = os.path.join(args['dest'], new_name)
                    shutil.copyfile(dir1[k], dest_file)
            elif up_1:                
                for k in indeces_unique:
                    tvt_dir = os.path.basename(os.path.dirname(dir1[k])) #train,val,test
                    f_name,f_ext = os.path.splitext(os.path.basename(dir1[k]))
                    new_name= f_name+'_'+f_ext
                    dest_file = os.path.join(args['dest'],tvt_dir, new_name)
                    shutil.copyfile(dir1[k], dest_file)
            elif up_2:                
                for k in indeces_unique:
                    tvt_dir = os.path.basename(os.path.dirname(os.path.dirname(dir1[k])))
                    group_dir = os.path.basename(os.path.dirname(dir1[k]))
                    f_name,f_ext = os.path.splitext(os.path.basename(dir1[k]))
                    new_name= f_name+'_'+f_ext
                    dest_file = os.path.join(args['dest'],tvt_dir,group_dir, new_name)
                    shutil.copyfile(dir1[k], dest_file)
    print('[INFO] Transfering. Done!')
    filter_case(list(paths.list_images(args['dest'])))



# Case checking
if args['input']:
    img_paths = list(paths.list_images(args['input']))
    filter_case(img_paths)
elif args['source'] and args['dest']:
    dir1 = list(paths.list_images(args['source']))
    dir2 = list(paths.list_images(args['dest']))
    transfer_case(dir1,dir2)
else:
    print("[ERROR] missing parameters! source needs a destination. Flip is optional in both cases:filtering and transfer.")



            
            
            