print("Hello!");
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

print("Done importing libraries!");

dirt = imread('https://gitlab.com/aer224/summer-2022-soil/-/raw/main/Soil%20Photos/soil_photo%20(1).jpg')
imshow(dirt);

dirt_gray = rgb2gray(dirt)
otsu_thresh = threshold_otsu(dirt_gray)
dirt_binary = dirt_gray < otsu_thresh
imshow(dirt_binary, cmap = 'gray'); #Showing greyscale image

dirt_hsv = rgb2hsv(dirt[:,:,:3])
plt.figure(num=None, figsize=(8, 6), dpi=80)
plt.imshow(dirt_hsv[:,:,0], cmap='hsv') #Showing HSV
plt.colorbar();

lower_mask = dirt_hsv [:,:,0] > 0.80
upper_mask = dirt_hsv [:,:,0] <= 1.00
mask = upper_mask*lower_mask
red = dirt[:,:,0]*mask
green = dirt[:,:,1]*mask
blue = dirt[:,:,2]*mask
dirt_mask = np.dstack((red,green,blue))
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(dirt_mask);

dirt_hsv = rgb2hsv(dirt[:,:,:3])
plt.figure(num=None, figsize=(8, 6), dpi=80)
plt.imshow(dirt_hsv[:,:,2], cmap='gray')
plt.colorbar();

lower_mask = dirt_hsv [:,:,0] > 0.80
upper_mask = dirt_hsv [:,:,0] <= 1.00
value_mask = dirt_hsv [:,:,2] < .90
mask = upper_mask*lower_mask*value_mask
red = dirt[:,:,0] * mask
green = dirt[:,:,1] * mask
blue = dirt[:,:,2] * mask
dirt_mask = np.dstack((red, green, blue))
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(dirt_mask);

lower_mask = dirt_hsv [:,:,0] > 0.80
upper_mask = dirt_hsv [:,:,0] <= 1.00
value_mask = dirt_hsv [:,:,2] < .90
mask = median_filter(upper_mask*lower_mask*value_mask, 10)
red = dirt[:,:,0] * mask
green = dirt[:,:,1] * mask
blue = dirt[:,:,2] * mask
dirt_mask = np.dstack((red, green, blue))
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(dirt_mask);

dirt_blobs = label(rgb2gray(dirt_mask) > 0)
imshow(dirt_blobs, cmap = 'tab10');

properties =['area','bbox','convex_area','bbox_area',
             'major_axis_length', 'minor_axis_length',
             'eccentricity']
df = pd.DataFrame(regionprops_table(dirt_blobs, properties = properties))


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
ax.imshow(dirt);
ax.set_axis_off()

df = df[df['eccentricity'] < df['eccentricity'].max()]

fig, ax = plt.subplots(1, len(blob_coordinates), figsize=(15,5))
for n, axis in enumerate(ax.flatten()):
    axis.imshow(dirt[int(blob_coordinates[n][0]):
                     int(blob_coordinates[n][2]), 
                     int(blob_coordinates[n][1]):
                     int(blob_coordinates[n][3])]);
    
fig.tight_layout()

plt.show(block=True) #this is the wonderful command that actually plots everything (on my machine at least)