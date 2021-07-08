import numpy as np
import cv2
import cv2.aruco as aruco

def detectArUco(image):
    #detectArUco = {}
    img = image

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    # Detect the markers.
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict,
                                                          parameters=parameters)

    #idsList = ids.tolist()
    #print(corners[1][0])

    #for i in range(len(corners)):
    #    detectArUco[idsList[i][0]] = corners[i][0]

    return corners


image = cv2.imread("F:/finalNTI2/image/test/F_0.jpg")
print(detectArUco(image))