import cv2
import os
import random
import numpy as np
import albumentations as al
from matplotlib import pyplot as plt
import shutil

image_folder = "/media/mvouz/Elements/YOLOV6/YOLOv6/images"
annotation_folder = "/media/mvouz/Elements/YOLOV6/YOLOv6/labels"
output_folder = "/media/mvouz/Elements/YOLOV6/YOLOv6/images"

blur_aug = al.Blur(12, 1.0)
median_blur_aug = al.MedianBlur(11, 1.0)
togray_aug = al.ToGray(True, 1.0)
clahe_aug = al.CLAHE(4.0, (8, 8), True, 1.0)
random_Brightness_Contrast = al.RandomBrightnessContrast(0.4, 0.4, True, True, 1.0)
gamma = al.RandomGamma((80, 150),None, True, 1.0)


def simple_augs(image_folder, annotation_folder, aug_percent = 0.1):
    for folder in os.listdir(image_folder):
        image_files = [f for f in os.listdir(os.path.join(image_folder, folder)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        num_images_to_augment = max(1, int(aug_percent * len(image_files)))
        
        for i in range(num_images_to_augment):
            #selected_image_blur = random.sample(image_files, 1)
            #selected_image_median = random.sample(image_files, 1)
            selected_image_togray = random.sample(image_files, 1)
            selected_image_clahe = random.sample(image_files, 1)
            selected_image_brightness_contrast = random.sample(image_files, 1)
            selected_image_gamma = random.sample(image_files, 1)
            
            selected_image_path_clahe = os.path.join(os.path.join(image_folder, folder), selected_image_clahe[0])
            selected_image_path_gamma = os.path.join(os.path.join(image_folder, folder), selected_image_gamma[0])
            selected_image_path_brightness_contrast = os.path.join(os.path.join(image_folder, folder), selected_image_brightness_contrast[0])
            selected_image_path_togray = os.path.join(os.path.join(image_folder, folder), selected_image_togray[0])
            #selected_image_path_median = os.path.join(os.path.join(image_folder, folder), selected_image_median[0])
            #selected_image_path_blur = os.path.join(os.path.join(image_folder, folder), selected_image_blur[0])        

            #image_blur = cv2.imread(selected_image_path_blur)
            #image_median = cv2.imread(selected_image_path_median)
            image_togray = cv2.imread(selected_image_path_togray)
            image_clahe = cv2.imread(selected_image_path_clahe)
            image_brightness_contrast = cv2.imread(selected_image_path_brightness_contrast)
            image_gamma = cv2.imread(selected_image_path_gamma)
            
            #image_aug_blur = blur_aug(image = image_blur)['image']
            #image_aug_median = median_blur_aug(image = image_median)['image']
            image_aug_togray = togray_aug(image = image_togray)['image']
            image_aug_clahe = clahe_aug(image = image_clahe)['image']
            image_aug_brightness_contrast = random_Brightness_Contrast(image = image_brightness_contrast)['image']
            image_aug_gamma = gamma(image = image_gamma)['image']
 
            #annotation_path_blur = os.path.join(os.path.join(annotation_folder, folder), os.path.splitext(selected_image_blur[0])[0] + ".txt")
            #annotation_path_median = os.path.join(os.path.join(annotation_folder, folder), os.path.splitext(selected_image_median[0])[0] + ".txt")
            annotation_path_togray = os.path.join(os.path.join(annotation_folder, folder), os.path.splitext(selected_image_togray[0])[0] + ".txt")
            annotation_path_clahe = os.path.join(os.path.join(annotation_folder, folder), os.path.splitext(selected_image_clahe[0])[0] + ".txt")
            annotation_path_brightness_contrast = os.path.join(os.path.join(annotation_folder, folder), os.path.splitext(selected_image_brightness_contrast[0])[0] + ".txt")
            annotation_path_gamma = os.path.join(os.path.join(annotation_folder, folder), os.path.splitext(selected_image_gamma[0])[0] + ".txt")

            #aug_img_name = f"blur_aug_{i}.jpg"
            #median_img_name = f"median_aug_{i}.jpg"
            togray_img_name = f"togray_aug_{i}.jpg"
            clahe_img_name = f"clahe_aug_{i}.jpg"
            random_brightness_contrast_img_name = f"random_brightness_contrast_aug_{i}.jpg"
            gamma_img_name = f"gamma_aug_{i}.jpg"
            
            #annotation_name_blur = aug_img_name[:-3] + "txt"
            #annotation_name_median = median_img_name[:-3] + "txt"
            annotation_name_togray = togray_img_name[:-3] + "txt"
            annotation_name_clahe = clahe_img_name[:-3] + "txt"
            annotation_name_brightness_contrast = random_brightness_contrast_img_name[:-3] + "txt"
            annotation_name_gamma = gamma_img_name[:-3] + "txt"
            
            cv2.imwrite(os.path.join(os.path.join(image_folder, folder), gamma_img_name), image_aug_gamma)
            cv2.imwrite(os.path.join(os.path.join(image_folder, folder), random_brightness_contrast_img_name), image_aug_brightness_contrast)
            cv2.imwrite(os.path.join(os.path.join(image_folder, folder), clahe_img_name), image_aug_clahe)
            cv2.imwrite(os.path.join(os.path.join(image_folder, folder), togray_img_name), image_aug_togray)
            #cv2.imwrite(os.path.join(os.path.join(image_folder, folder), median_img_name), image_aug_median)
            #cv2.imwrite(os.path.join(os.path.join(image_folder, folder), aug_img_name), image_aug_blur)
            
            #shutil.copyfile(annotation_path_blur, os.path.join(os.path.join(annotation_folder, folder), annotation_name_blur))
            #shutil.copyfile(annotation_path_median, os.path.join(os.path.join(annotation_folder, folder), annotation_name_median))
            shutil.copyfile(annotation_path_togray, os.path.join(os.path.join(annotation_folder, folder), annotation_name_togray))
            shutil.copyfile(annotation_path_clahe, os.path.join(os.path.join(annotation_folder, folder), annotation_name_clahe))
            shutil.copyfile(annotation_path_brightness_contrast, os.path.join(os.path.join(annotation_folder, folder), annotation_name_brightness_contrast))
            shutil.copyfile(annotation_path_gamma, os.path.join(os.path.join(annotation_folder, folder), annotation_name_gamma))
            
            print("CLAHE: " + clahe_img_name + " | " + annotation_name_clahe)
            print("RANDOM BRIGHTNESS CONTRAST: " + random_brightness_contrast_img_name + " | " + annotation_name_brightness_contrast)
            print("GAMMA: " + gamma_img_name + " | " + annotation_name_gamma)
            
simple_augs(image_folder, annotation_folder)