from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

img = np.load(Path(Path.cwd(), 'figures', 'ps.npy.txt'))

lb = label(img)

fs = {}

for l in np.unique(lb)[1:]:
    x, y = np.where(lb == l)
    x = x - x.min()
    y = y - y.min()
    k = (str(x), str(y))
    if k not in fs.keys():
        fs[k] = 1
    else:
        fs[k] += 1

for i, (fi, coun) in enumerate(fs.items()):
    plt.subplot(1, 5, i + 1)
    fi = (
        np.fromstring(fi[0][1:-1], dtype=int, sep=" "),
        np.fromstring(fi[1][1:-1], dtype=int, sep=" "),
    )
    fig = np.zeros((max(fi[0]) + 1, max(fi[1]) + 1))
    fig[fi[0], fi[1]] = 1
    plt.title(f"{coun}")
    plt.imshow(fig)
plt.suptitle(f"Всего: {lb.max()}")
plt.show()