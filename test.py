import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread('blah4.png')

print img

with open('blah.txt',mode='w') as f:
    for line in img:
        for point in line:
            f.write('[')
            for x in point:
                f.write('{0} '.format(str(x)))
            f.write(']')
        f.write('\n')

imgplot = plt.imshow(img)
plt.show()