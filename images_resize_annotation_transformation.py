import os
from PIL import Image
import os.path

def load_annotation(annotation_path):
    with open(annotation_path, 'r') as f:
        lines = f.readlines()
    return [list(map(float, line.replace(',', ' ').strip().split())) for line in lines]

def save_annotation(annotation_path, boxes):
    with open(annotation_path, 'w') as f:
        for box in boxes:
            print("BOX: ", box)
            f.write(" ".join(map(str, box)) + '\n')
            
def resize_images(image_folder, annotation_folder, new_size = (1280, 1280)):
    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)
        image = Image.open(image_path)
        resizedImage = image.resize(new_size)
        resizedImage.save(image_path)
        print("Saving image with size ", str(resizedImage.size), " in path: ", image_path)
        
        annotation_path = os.path.join(annotation_folder, os.path.splitext(image_name)[0] + ".txt")
        original_boxes = load_annotation(annotation_path)
        for box in original_boxes:
            box[1] *= new_size[0] / image.width #x_center
            box[2] *= new_size[1] / image.height  # y_center
            box[3] *= new_size[0] / image.width  # width
            box[4] *= new_size[1] / image.height  # height  
            
        save_annotation(annotation_path, original_boxes)

image_folder = '/media/mvouz/Elements/YOLOV6/YOLOv6/images'
annotation_folder = '/media/mvouz/Elements/YOLOV6/YOLOv6/labels'

resize_images(image_folder, annotation_folder)