# edgecase.ai synthetic Gun Dataset

## Directory Structure
```
.Synthetic_Gun
├── README.md
├── extract_json_object.py
├── visualize_instance.py
├── Weapon-images            
├── Weapon-images-masks     
├── Weapon-images-outdoor
└── Weapon-images-outdoor-masks
```
No need to download `Weapon-images-masks` and `Weapon-images-outdoor-masks` since masks can be reconstructed from metadata.

## Explore Metadata
The json files contatining information for every mask instance is stored within either `Weapon-images` or `Weapon-images-outdoor` along with the original images.
To take a look at the json keys of a random json file instance, e.g., `Weapon-images-mask/weapon_9989_0.json`. Use of jq from terminal: 
```
sudo apt-get install jq #if not installed already
jq 'keys' Weapon-images-mask/weapon_9989_0.json
```
```
  "area",
  "bbox",
  "color",
  "contours",
  "isMain",
  "joints",
  "objectId",
  "tagName"
```
There are many objects besides gun, e.g., tables, chairs, etc. After some inspection you find out that json files with the key "objectId": 2998 and "tagName": weapon represent gun. Also of interest is key "objectId": 2999 which are people with weapons (weapon not included in object). 

To explore what type of objects there are in an image go across all json file instances for that image by using a wild card (*)
```
jq '.tagName' Weapon-images/weapon_9989_*.json 
``` 
[More jq shortcuts](https://gist.github.com/olih/f7437fb6962fb3ee9fe95bda8d2c8fa4) if interested.

## Visualize Contours
To further explore a json file instance I have added `visualize_instance.py`. The "contours" key is formatted in the same way as the famous coco dataset [[x1,y1,x2,y2,..], ... , [x1,y1,x2,y2,..]], i.e., a single mask object can be split in multiple parts due to occlusion, etc.
Before running the script you can take a quick look by:
```
jq '.contours' Weapon-images/weapon_9989_0.json 
``` 
A visual representation is achieved by (might need to install some python modules like opencv)
```
python `visualize_instance.py` --input Weapon-images/weapon_9989_0.json
```

## Extract Summarize object
To improve speed during training I have added `extract_json_object.py`. All objects have their own json files so this scripts combines all gun instances in an image into a single json file. For every image in a given directory it will output one json file.
```
python extract_json_object.py --input Weapon-images
``` 
this will will output, i.e., `Weapon-images/weapon_9989_allguns.json` for image `Weapon-images/weapon_9989_original.png` containing all gun instances. 
Take a look by running  
```
jq '.' Weapon-images/weapon_9989_allguns.json 
``` 
```
  "imgfile": "weapon_9989_original.png",
  "height": 720,
  "width": 1280,
  "name": "gun",
  "instances": [[[{"x": 551, "y": 306}, ... 
```
