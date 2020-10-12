import cv2

if __name__ == "__main__":
    window_name = "Hello World"
    cv2.namedWindow(window_name)
    img = cv2.imread("./hat.jpg")

    screen_res = 1280, 720
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)

    cv2.resizeWindow(window_name, window_width, window_height)

    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
