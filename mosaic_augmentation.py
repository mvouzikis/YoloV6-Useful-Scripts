from PIL import Image
import os
import random

def load_annotation(annotation_path):
    with open(annotation_path, 'r') as f:
        lines = f.readlines()
    return [list(map(float, line.replace(',', ' ').strip().split())) for line in lines]

def save_annotation(annotation_path, boxes):
    with open(annotation_path, 'w') as f:
        for box in boxes:
            f.write(" ".join(map(str, box)) + '\n')

def mosaic_augmentation(image_folder, annotation_folder, output_folder, new_size=(1280, 1280), augmentation_percentage=0.1):

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    num_images_to_augment = max(1, int(augmentation_percentage * len(image_files)))

    for i in range(num_images_to_augment):
        selected_images = random.sample(image_files, 4)

        mosaic = Image.new('RGB', (new_size[0] * 2, new_size[1] * 2))
        boxes = []

        for j, image_name in enumerate(selected_images):
            x_offset = 0 if j % 2 == 0 else new_size[0]
            y_offset = 0 if j < 2 else new_size[1]

            image_path = os.path.join(image_folder, image_name)
            image = Image.open(image_path)

            mosaic.paste(image, (x_offset, y_offset))

            annotation_path = os.path.join(annotation_folder, os.path.splitext(image_name)[0] + ".txt")
            original_boxes = load_annotation(annotation_path)

            for box in original_boxes:
                box[1] += x_offset / (new_size[0] * 2)  # x_center
                box[2] += y_offset / (new_size[1] * 2)  # y_center

                if j % 2 == 1:  # Adjust boxes for second column
                    box[1] += 0.5
                if j >= 2:  # Adjust boxes for second row
                    box[2] += 0.5

                box[3] *= new_size[0] / (image.width * 2)  # width
                box[4] *= new_size[1] / (image.height * 2)  # height

                boxes.append(box)

        mosaic_name = f"mosaic_aug_{i + 1}.jpg"
        mosaic_path = os.path.join(output_folder, mosaic_name)
        annotation_path = os.path.join(annotation_folder, os.path.splitext(mosaic_name)[0] + ".txt")

        mosaic.save(mosaic_path)
        print("Saved: ", mosaic_name, " in path: ", mosaic_path)
        save_annotation(annotation_path, boxes)
        print("Saved box: ",box , " in path: ", annotation_path)

# Example usage
image_folder = './YOLOv6/images'
annotation_folder = './YOLOv6/labels'
output_folder = './YOLOv6/images'

mosaic_augmentation(image_folder, annotation_folder, output_folder)
