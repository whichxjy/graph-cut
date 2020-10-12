import cv2

if __name__ == "__main__":
    window_name = "Hello World"
    cv2.namedWindow(window_name)
    img = cv2.imread("./hat.jpg")

    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
