import os 
import pathlib
import shutil
import glob 

fsoco_path = os.path.abspath('./fsoco_bounding_boxes')
labelspath = './YOLOv6/labels'
yoloimagepath = './YOLOv6/images'

for folder in os.listdir(fsoco_path):
    imagepath = os.path.join(os.path.join(fsoco_path, folder), "img")
    print("Image path: ", imagepath)
    
    for image in glob.glob(os.path.join(imagepath, '*jpg')) or glob.glob(os.path.join(imagepath, '*png')):
        print("File path: ", image)
        with open(image) as file:
            file_name = os.path.basename(file.name)
            print(file_name)
            shutil.copy(image, yoloimagepath)
