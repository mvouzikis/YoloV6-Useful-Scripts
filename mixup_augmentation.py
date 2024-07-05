import cv2
import os
import random
import numpy as np

def load_annotation(annotation_path):
    with open(annotation_path, 'r') as f:
        lines = f.readlines()
    return [list(map(float, line.replace(',', ' ').strip().split())) for line in lines]

def mixup_augmentation(image_folder, annotation_folder, output_folder, mixup_percentage=0.1):

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    num_images_to_augment = max(1, int(mixup_percentage * len(image_files)))

    for i in range(num_images_to_augment):
        # Randomly select two images for mixup
        selected_images = random.sample(image_files, 2)
        image1_path = os.path.join(image_folder, selected_images[0])
        image2_path = os.path.join(image_folder, selected_images[1])

        # Load images
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        # Resize images to a common size
        common_size = (min(image1.shape[1], image2.shape[1]), min(image1.shape[0], image2.shape[0]))
        image1 = cv2.resize(image1, common_size)
        image2 = cv2.resize(image2, common_size)

        # Random mixup ratio (lambda)
        mixup_ratio = random.uniform(0.3, 0.7)

        # Perform mixup
        mixed_image = cv2.addWeighted(image1, mixup_ratio, image2, 1 - mixup_ratio, 0)

        # Save mixed image
        mixed_image_name = f"mixup_aug_{i + 1}.jpg"
        mixed_image_path = os.path.join(output_folder, mixed_image_name)
        cv2.imwrite(mixed_image_path, mixed_image)
        print("save image to path: ", mixed_image_path)

        # Load and transform bounding boxes for mixup
        annotation1_path = os.path.join(annotation_folder, os.path.splitext(selected_images[0])[0] + ".txt")
        annotation2_path = os.path.join(annotation_folder, os.path.splitext(selected_images[1])[0] + ".txt")

        boxes1 = load_annotation(annotation1_path)
        boxes2 = load_annotation(annotation2_path)

        # Sample the same number of bounding boxes from each image
        min_boxes = min(len(boxes1), len(boxes2))
        selected_boxes1 = random.sample(boxes1, min_boxes)
        selected_boxes2 = random.sample(boxes2, min_boxes)

        # Convert back to NumPy arrays
        boxes1 = np.array(selected_boxes1)
        boxes2 = np.array(selected_boxes2)

        # Resize bounding boxes to match the resized images
        boxes1[:, [1, 3]] *= common_size[0] / image1.shape[1]
        boxes1[:, [2, 4]] *= common_size[1] / image1.shape[0]

        boxes2[:, [1, 3]] *= common_size[0] / image2.shape[1]
        boxes2[:, [2, 4]] *= common_size[1] / image2.shape[0]

        # Mixup bounding boxes
        mixed_boxes = mixup_ratio * boxes1 + (1 - mixup_ratio) * boxes2

        # Save mixed bounding boxes
        mixed_annotation_path = os.path.join(annotation_folder, os.path.splitext(mixed_image_name)[0] + ".txt")
        np.savetxt(mixed_annotation_path, mixed_boxes, delimiter=',')
        print("save box to path: ", mixed_annotation_path)


# Example usage
image_folder = "./YOLOv6/images"
annotation_folder = "./YOLOv6/labels"
output_folder = "./YOLOv6/images"

mixup_augmentation(image_folder, annotation_folder, output_folder)
