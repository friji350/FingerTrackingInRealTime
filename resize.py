import numpy as np
import cv2
import cv2.aruco as aruco
from transform import four_point_transform


def detect(img):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict,
                                                          parameters=parameters)
    #out = aruco.drawDetectedMarkers(img, corners, ids)
    return corners


def getInnerPoint(points, centerX, centerY):
    isRight = points[0][0] < centerX
    isUp = points[0][1] < centerY

    tempX = 10000 if isRight else 0
    tempY = 10000 if isUp else 0
    #print(points)
    for point in points:
        if point[0] > tempX and not isRight:
            tempX = point[0]
        if point[0] < tempX and isRight:
            tempX = point[0]
        if point[1] > tempY and not isUp:
            tempY = point[1]
        if point[1] < tempY and isUp:
            tempY = point[1]
    return tempX, tempY


def getInnerPointsClockwice(corners, centerX, centerY):
    inners = [getInnerPoint(corner[0], centerX, centerY) for corner in corners]
    firstIndex = 0
    print(len(inners))
    if len(inners) == 4:
        for i in range(1, 4):
            if inners[i][0] + 100 < inners[firstIndex][0] or inners[i][1] + 100 < \
                    inners[firstIndex][1]: firstIndex = i

    return [inners[(firstIndex + 0) % 4], inners[(firstIndex + 1) % 4],
            inners[(firstIndex + 2) % 4],
            inners[(firstIndex + 3) % 4]]


def transform(clockwice):
    pts = np.array(eval(
        f'[[{clockwice[0][0]}, {clockwice[0][1]}], [{clockwice[1][0]},'
        f' {clockwice[1][1]}], [{clockwice[2][0]}, {clockwice[2][1]}],'
        f' [{clockwice[3][0]}, {clockwice[3][1]}]]'),
                   dtype="float32")
    return pts



def crop(image):
    corners = detect(image)
    clockwice = getInnerPointsClockwice(corners, 300, 300)

    warped = four_point_transform(image, transform(clockwice))
    #print(transform(clockwice)[0][0])

    return transform(clockwice)
    #return warped


def resize(image):
    _image = cv2.resize(image, (int(1420), int(200)),
                        interpolation=cv2.INTER_CUBIC)
    return _image


def formattingImage(img) -> object:
    new_image = resize(crop(img))
    return new_image


def fix(dx, dy, height):
    realX = dx - dx / 1.75 * height
    realY = dy - dy / 1.75 * height
    return realX, realY




#C:\Users\Robo-teacher\Downloads\dwa\finalNTI2\image\test
#C:/Users/Robo-teacher/Downloads/dwa/finalNTI2/1625658582633.jpg
#image = formattingImage("C:/Users/Robo-teacher/Downloads/dwa/finalNTI2/1625662318933.jpg")
#cv2.imshow('vo', image)
#cv2.waitKey()
#cv2.destroyAllWindows()