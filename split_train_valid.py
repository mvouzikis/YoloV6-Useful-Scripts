import os
import shutil
import random

labels = 'YOLOv6/labels'
images = 'YOLOv6/images'

#create train & valid folders if not created
os.makedirs(os.path.join(labels, "train"), exist_ok=True)
os.makedirs(os.path.join(labels, "valid"), exist_ok=True)
os.makedirs(os.path.join(images, "train"), exist_ok=True)
os.makedirs(os.path.join(images, "valid"), exist_ok=True)

count = 0

for file in os.listdir(images + "/train"):
    count += 1

#count = number of images

n_random_images = int((20/100) * count)

print(count)
print("20% equals to: ", n_random_images)

for i in range(n_random_images):

    imglist = os.listdir(images + "/train")
    
    random_choice_img = random.choice(imglist)
    print("Random: ", random_choice_img)

    random_choice_txt = random_choice_img[:-4] + ".txt"
    print("Random txt: ", random_choice_txt)

    #copy image to valid
    shutil.copy(images + "/train/" + random_choice_img, os.path.join(images, "valid"))

    #copy label to valid
    shutil.copy(labels + "/train/" + random_choice_txt, os.path.join(labels, "valid"))

    os.remove(images + "/train/" + random_choice_img)
    print("DELETED", images+"/train/"+random_choice_img)

    os.remove(labels + "/train/" + random_choice_txt)
    print("DELETED", labels+"/train/"+random_choice_txt)
    
    print((i/n_random_images)*100, "%")