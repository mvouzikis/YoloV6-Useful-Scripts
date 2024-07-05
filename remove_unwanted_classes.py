import cv2
import os
import random
import numpy as np
import albumentations as al
from matplotlib import pyplot as plt
import shutil

image_folder = "./YOLOv6/images"
annotation_folder = "./YOLOv6/labels_test_reformed"
annotation_folder_train = "./YOLOv6/labels_test_reformed/train"
annotation_folder_valid = "./labels_test_reformed/valid"

labelcount = 0
unwantedIndexes = [0,1,3,4,5,6]

for file in os.listdir(annotation_folder_train):
    fileLines = []
    labelcount += 1
    with open(os.path.join(annotation_folder_train,file)) as f:
        lines = f.readlines()
        print(lines)
        for line in lines:
            if (line.split()[0] == "2"):
                newLine = "0 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
            if (line.split()[0] == "7"):
                newLine = "1 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
            if (line.split()[0] == "8"):
                newLine = "2 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
            if (line.split()[0] == "9"):
                newLine = "3 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
    with open(os.path.join(annotation_folder_train,file), 'w') as f:
        f.writelines(fileLines)
        print("Wrote new lines to file: " + file)

for file in os.listdir(annotation_folder_valid):
    fileLines = []
    labelcount += 1
    with open(os.path.join(annotation_folder_valid,file)) as f:
        lines = f.readlines()
        print(lines)
        for line in lines:
            if (line.split()[0] == "2"):
                newLine = "0 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
            if (line.split()[0] == "7"):
                newLine = "1 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
            if (line.split()[0] == "8"):
                newLine = "2 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
            if (line.split()[0] == "9"):
                newLine = "3 " + line.split()[1] + " " + line.split()[2] + " " + line.split()[3] + " " + line.split()[4] + "\n"
                fileLines.append(newLine)
                print(newLine+"\n")
                
    with open(os.path.join(annotation_folder_valid,file), 'w') as f:
        f.writelines(fileLines)
        print("Wrote new lines to file: " + file)
    
        
print("Label count: " + str(labelcount))   
