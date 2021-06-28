import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread('test-data/1.jpg', 3)
mask = np.ones((3, 256))
mask[0, 0:128] = 0
mask[1, 128:] = 0
mask[2, :200] = 0
print(mask)
print(mask.shape, img.shape)
result = filter(img, mask).astype(np.uint8)
print(result.dtype)
result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
plt.imshow(result)
plt.show()
