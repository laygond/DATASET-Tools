# -----------------------------
#   USAGE
# -----------------------------
# python class_changer.py --input "/directory/input"  --settings "[(12,0),(15,1),...]"
#
# DESCRIPTION:
# Switch classes according to list of tupples e.g. [(12,0),(15,1),...]
# In this case, all class 12 are switched to zero and all class 15 to 1
# This change in class happens for all .txt yolo files under input
# directory.  
#  
# NOTE:
# Absolute paths are required.
# Comma separated values are ignored
#
# Author: Bryan Laygond
# Website: http://www.laygond.com
# 
# ------------------------------

# Import the necessary packages
from imutils import paths
import argparse

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
	help="highest level directory where all labels are stored")
ap.add_argument("-s", "--settings", type=str,
	help="switch classes according to list of tupples e.g. [(0,1),(5,8),...]")
args = vars(ap.parse_args())
assert args['input'] and args['settings'] 

# Define
label_paths = list(paths.list_files(args['input'], validExts=(".txt",)))
shifts = eval(args['settings'])
def _isnumber(str_number):
    try:
        float(str_number)
        return True
    except:
        return False


# Change classes for all paths
print('[INFO] Switching classes...')
for p in label_paths:
    f = open(p, 'r')
    lines = f.readlines()
    if not lines:
        f.close() 
        continue
    first_line_check =  [_isnumber(elem) for elem in lines[0].split()]
    YOLO_style = True if len(first_line_check) == 5 and all(first_line_check) else False
    if not YOLO_style: # YOLO should have 5 numbers per line    
        f.close()
        continue
    for i in range(len(lines)):
        current_line = lines[i].split()
        current_class = int(current_line[0])
        for (old_class, new_class) in shifts:
            if current_class == old_class:
                current_line[0] = str(new_class)
                lines[i] = " ".join(current_line)
                break 
    f.close()
    with open(p, 'w') as f:
        f.write("".join(lines))
print('[INFO] Complete!')
