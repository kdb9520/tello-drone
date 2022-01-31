from djitellopy import tello
import cv2


def main():
    me = connect()
    camera_on(me)


def connect():
    me = tello.Tello()
    me.connect()
    print(me.get_battery())
    return me


def camera_on(me):
    me.streamon()
    while True:
        img = me.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
