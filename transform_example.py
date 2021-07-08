from transform import four_point_transform
import numpy as np
import argparse
import cv2

image = cv2.imread("F:/finalNTI2/image/test/F_0.jpg")
pts = np.array(eval('[(73, 239), (356, 117), (475, 265), (187, 443)]'), dtype = "float32")
warped = four_point_transform(image, pts)
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)