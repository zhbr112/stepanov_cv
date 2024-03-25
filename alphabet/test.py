import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from collections import defaultdict
from pathlib import Path


def filling_factor(arr):
    return np.sum(arr) / arr.size


def count_holes(arr):
    labeled = label(np.logical_not(arr))
    regions = regionprops(labeled)
    holes = 0
    for region in regions:
        coords = np.transpose(region.coords, (1,0))
        ymin = np.min(coords[1])
        ymax = np.max(coords[1])
        xmin = np.min(coords[0])
        xmax = np.max(coords[0])
        if ymin == 0 or ymax == arr.shape[1]-1 or xmin == 0 or xmax == arr.shape[0]-1: continue
        holes += 1
    return holes


def count_holes_rame(arr):
    labeled = label(np.logical_not(arr))
    return np.max(labeled)


def count_vline(arr):
    return np.sum(arr.mean(0) == 1)


def recognize(region):
    if filling_factor(region.image) == 1.0:
        return '-'
    else:
        holes = count_holes(region.image)
        if holes == 2: # B or 8
            if count_vline(region.image) >= 3:
                return 'B'
            else: return '8'
        elif holes == 1: #A or 0
            if count_vline(region.image)>=2:
                ecc=region.eccentricity
                if ecc<0.65:
                    return 'D'
                else:
                    return 'P'
            else: 
                if abs((region.local_centroid[0] / region.image.shape[0]) - (region.local_centroid[1] / region.image.shape[1])) > 0.02:
                    return 'A'        
                else: return '0'
        else:
            if count_vline(region.image) >= 1:
                return '1'
            else:
                ecc=region.eccentricity
                if ecc<0.4:
                    return '*'
                match count_holes_rame(region.image):
                    case 2: return '/'
                    case 4: return 'X'
                    case _: return 'W'
    return '_'

img = plt.imread('Test/symbols.png')

img = np.mean(img, axis=2)
thrash = threshold_otsu(img)
img[img > 0] = 1

regions = regionprops(label(img))

result = defaultdict(lambda: 0)

path = Path('.') / 'Test/result'
path.mkdir(exist_ok=True)

for i,region in enumerate(regions):
    symbol = recognize(region)
    if symbol in ['P','D']:
        plt.clf()
        plt.title(f"{symbol}")
        plt.imshow(region.image)
        plt.savefig(path / f"{i}")
        result[symbol] += 1

print(result, sum(result.values()))
