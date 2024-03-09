from skimage.measure import label
import matplotlib.pyplot as plt
import numpy as np

def areas(LB,label):
    coins = []
    for i in range(1,label+1):
        coins.append((LB==i).sum())
    return coins

im = np.load("money/coins.npy.txt")

lb = label(im)

coins = areas(lb,lb.max())
nom = sorted(list(set(coins)))

ones = coins.count(nom[0])
twos = coins.count(nom[1]) * 2
fives = coins.count(nom[2]) * 5
tens = coins.count(nom[3]) * 10

print(ones+twos+fives+tens)


# plt.subplot(121)
# plt.imshow(im)
# plt.subplot(122)
# plt.imshow(lb)
# plt.show()