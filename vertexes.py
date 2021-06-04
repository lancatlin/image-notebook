import cv2


def detect_vertexes(img):
    edges = cv2.Canny(img, 50, 200)
    return edges


if __name__ == "__main__":
    img = cv2.imread('test-data/test.jpg', -1)
    img = cv2.resize(img, (1200, 900))
    cv2.imshow('origin', img)
    cv2.imshow('output', detect_vertexes(img))
    cv2.waitKey(0)
