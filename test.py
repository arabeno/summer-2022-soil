print("hello");
#All of this code is from https://towardsdatascience.com/image-processing-with-python-blob-detection-using-scikit-image-5df9a8380ade

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import skimage
from skimage.io import imread, imshow
from skimage.color import rgb2gray, rgb2hsv
from skimage.measure import label, regionprops, regionprops_table
from skimage.filters import threshold_otsu
from scipy.ndimage import median_filter
from matplotlib.patches import Rectangle
from tqdm import tqdm

print("done!");

tree = imread('soil_photo_1.jpg')
imshow(tree);

tree_gray = rgb2gray(tree)
otsu_thresh = threshold_otsu(tree_gray)
tree_binary = tree_gray < otsu_thresh
imshow(tree_binary, cmap = 'gray');

tree_hsv = rgb2hsv(tree[:,:,:3])
plt.figure(num=None, figsize=(8, 6), dpi=80)
plt.imshow(tree_hsv[:,:,0], cmap='hsv')
plt.colorbar();

lower_mask = tree_hsv [:,:,0] > 0.80
upper_mask = tree_hsv [:,:,0] <= 1.00
mask = upper_mask*lower_mask
red = tree[:,:,0]*mask
green = tree[:,:,1]*mask
blue = tree[:,:,2]*mask
tree_mask = np.dstack((red,green,blue))
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(tree_mask);

tree_hsv = rgb2hsv(tree[:,:,:3])
plt.figure(num=None, figsize=(8, 6), dpi=80)
plt.imshow(tree_hsv[:,:,2], cmap='gray')
plt.colorbar();

lower_mask = tree_hsv [:,:,0] > 0.80
upper_mask = tree_hsv [:,:,0] <= 1.00
value_mask = tree_hsv [:,:,2] < .90
mask = upper_mask*lower_mask*value_mask
red = tree[:,:,0] * mask
green = tree[:,:,1] * mask
blue = tree[:,:,2] * mask
tree_mask = np.dstack((red, green, blue))
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(tree_mask);

lower_mask = tree_hsv [:,:,0] > 0.80
upper_mask = tree_hsv [:,:,0] <= 1.00
value_mask = tree_hsv [:,:,2] < .90
mask = median_filter(upper_mask*lower_mask*value_mask, 10)
red = tree[:,:,0] * mask
green = tree[:,:,1] * mask
blue = tree[:,:,2] * mask
tree_mask = np.dstack((red, green, blue))
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(tree_mask);

tree_blobs = label(rgb2gray(tree_mask) > 0)
imshow(tree_blobs, cmap = 'tab10');

properties =['area','bbox','convex_area','bbox_area',
             'major_axis_length', 'minor_axis_length',
             'eccentricity']
df = pd.DataFrame(regionprops_table(tree_blobs, properties = properties))


blob_coordinates = [(row['bbox-0'],row['bbox-1'],
                     row['bbox-2'],row['bbox-3'] )for 
                    index, row in df.iterrows()]
fig, ax = plt.subplots(1,1, figsize=(8, 6), dpi = 80)
for blob in tqdm(blob_coordinates):
    width = blob[3] - blob[1]
    height = blob[2] - blob[0]
    patch = Rectangle((blob[1],blob[0]), width, height, 
                       edgecolor='r', facecolor='none')
    ax.add_patch(patch)
ax.imshow(tree);
ax.set_axis_off()

df = df[df['eccentricity'] < df['eccentricity'].max()]

plt.show(block=True) #this is the wonderful command that actually plots everything