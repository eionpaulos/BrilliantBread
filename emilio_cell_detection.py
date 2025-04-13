import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load and convert to grayscale
img = cv2.imread('breadboard.webp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Optional: blur to reduce noise
blur = cv2.GaussianBlur(gray, (5,5), 0)

# Setup SimpleBlobDetector
params = cv2.SimpleBlobDetector_Params()
params.filterByCircularity = True
params.minCircularity = 0.7
params.filterByArea = True
params.minArea = 5
params.maxArea = 200
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs (the holes)
keypoints = detector.detect(blur)

# Draw red circles at each keypoint (hole)
img_with_dots = cv2.drawKeypoints(img, keypoints, None, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Convert and show
img_rgb = cv2.cvtColor(img_with_dots, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(12, 8))
plt.imshow(img_rgb)
plt.title("Detected Breadboard Holes")
plt.axis('off')
plt.show()
