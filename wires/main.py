from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np


def find_wire(img):
    count = 0
    count_2 = 0
    for y in range(binary_erosion(img).shape[0]):
        if binary_erosion(img)[y].any() == 1:
            count+=1
    for y in range(img.shape[0]):
        if img[y].any() == 1:
            count_2+=1
    if count_2 / 3 > count:
        count+=1
    return count


def parts(img,num_of_wires):
    count = 1
    for y in range(img.shape[0]):
        if img[y].all() == 1:
            print(f"{count} провод цел")
            count += 1
        elif count==num_of_wires and y == img.shape[0]-1:
            print(f"{count} провод полностью порван")
            count += 1
        elif img[y].any() == 1:
            print(f"{count} провод состоит {max(label(img[y]))} частей")
            count += 1


for i in range(1,7):
    im = np.load(f"wires/wires{i}npy.txt")

    print(f"Изображение номер {i} содержит {find_wire(im)} проводов")
    parts(binary_erosion(im), find_wire(im))
    plt.subplot(121)
    plt.imshow(im)
    plt.show()