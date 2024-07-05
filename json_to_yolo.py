import glob
import json
import optparse
import os
from shutil import copyfile

fsoco_path = os.path.abspath(r'./fsoco_bounding_boxes')
yolo_path = os.path.abspath(r'./YOLOv6')
print("fsoco path: ", fsoco_path)
print("yolo path: ", yolo_path)

def get_class_names_from_supervisely():
    class_names_array = []
    class_name_path = fsoco_path + '/meta.json'
    with open(class_name_path, 'r') as file:
        json_classes = json.load(file)["classes"]
        for json_class in json_classes:
            class_names_array.append(json_class["title"])
    return class_names_array

def create_yolo_structure():
    labeldir = yolo_path + "/labels"
    imagedir = yolo_path + "/images"
    os.makedirs(labeldir, exist_ok=True)
    os.makedirs(imagedir, exist_ok=True)
    print("Created path: ", labeldir)
    print("Created path: ", imagedir)
    
def create_class_file(class_names_array):
    class_file_path = yolo_path + "/labels/classes.txt"
    with open(class_file_path, 'w') as f:
        for class_name in class_names_array:
            f.write('%s\n' %class_name)

def get_yolo_annotation_info(folder_name, file_name, class_names_array):    
    import shutil
    image_path = fsoco_path + "/" + folder_name + "/img/" + file_name
    print("image path:", image_path)
    
    image_json_path = fsoco_path + "/" +folder_name + "/ann" + "/" + file_name + ".json"
    with open(image_json_path, 'r') as file:
        json_object = json.load(file)
        
    class_coord_list = []
    
    class_id = 0
    if len(json_object["objects"]) > 0:
        os.makedirs(yolo_path + "/images/train", exist_ok=True)
        copy_path = yolo_path + "/images/" + "/train/" + os.path.basename(image_path) 
        print("COPY PATH IS: ", copy_path)
        shutil.copy(image_path, copy_path)
        
    #getting the coordinates from the json file(exterior = [[left, [top], [right, bottom]])
        for obj in json_object["objects"]:  
            points = obj["points"]["exterior"]
            img_width = json_object["size"]["width"]
            img_height = json_object["size"]["height"]
            box_width = points[1][0] - points[0][0]
            box_height = points[1][1] - points[0][1]
            x1 = round((points[0][0] + box_width/2)/ img_width, 5)   
            y1 = round((points[0][1] + box_height / 2) / img_height, 5)
            x2 = round(box_width / img_width, 5)
            y2 = round(box_height / img_height, 5)     
            
            class_id = class_names_array.index(obj["classTitle"])
            class_coord_list.append({"class_id":class_id, "x1":x1, "y1":y1, "x2":x2, "y2":y2})
    return class_coord_list

def create_text_file(folder_name, file_name, class_names_array):
    class_coord_list = get_yolo_annotation_info(folder_name, file_name, class_names_array)
    
    if len(class_coord_list)>0:
        text_file_path = yolo_path + "//labels//" + "//train//" + os.path.splitext(file_name)[0] + ".txt"
        with open(text_file_path, 'w') as file:
            for coord in class_coord_list:
                class_id = coord["class_id"]
                x1 = coord["x1"]
                y1 = coord["y1"]
                x2 = coord["x2"]
                y2 = coord["y2"]                
                file.write('{} {} {} {} {}'.format(class_id, x1, y1, x2, y2))
                file.write('\n')
                
print("Proccessing...")
try:
    class_names_array = get_class_names_from_supervisely()
except IOError:
    print('Error [meta.json not found] => There should be a folder with json at {0}'.format(fsoco_path[:11]))
    exit(1)
    
create_yolo_structure()

create_class_file(class_names_array)

#dataset_folders = [folder for folder in os.listdir(fsoco_path)]
for folder in os.listdir(fsoco_path):
    labels_path = os.path.join(os.path.join(fsoco_path, folder), 'ann')
    print("Labels path: ", labels_path)
    
    for file_path in glob.glob(os.path.join(labels_path, '*json')):
        print("File path: ", file_path)
        with open(file_path) as file:
            file_name = os.path.basename(file.name)[:-5]
            create_text_file(folder, file_name, class_names_array)
    print("Yolo structure created at {0}".format(yolo_path))
