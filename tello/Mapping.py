from djitellopy import tello
import KeyPressModule as kp
import numpy as np
import cv2
import math
from time import sleep

# Constants
FSPEED = 11.7  # forward speed 11.7 cm/s
ASPEED = 36  # angular speed in degree/s
INTERVAL = 0.25


def main(FSPEED=11.7, ASPEED=36, INTERVAL=0.25):
    dInterval, aInterval, x, y, a, yaw = init_values(FSPEED, ASPEED, INTERVAL)
    points, me = init_drone()
    run_loop(dInterval, aInterval, x, y, a, yaw, me, points)


def init_values(FSPEED, ASPEED, INTERVAL):
    dInterval = FSPEED * INTERVAL
    aInterval = ASPEED * INTERVAL
    x, y = 500, 500
    a = 0
    yaw = 0
    return dInterval, aInterval, x, y, a, yaw


def init_drone():
    kp.init()

    me = tello.Tello()
    me.connect()
    print(me.get_battery())

    points = [(0, 0), (0, 0)]

    return points, me


def getKeyboardInput(dInterval, aInterval, x, y, a, yaw, me):
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    angSpeed = 50
    d = 0

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -angSpeed
        yaw -= aInterval
    elif kp.getKey("d"):
        yv = angSpeed
        yaw += aInterval

    if kp.getKey("q"):
        me.land()
        sleep(3)
    if kp.getKey("e"):
        me.takeoff()

    sleep(INTERVAL)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 15, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100}, {(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)


def run_loop(dInterval, aInterval, x, y, a, yaw, me, points):
    while True:
        vals = getKeyboardInput(dInterval, aInterval, x, y, a, yaw, me)
        me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

        img = np.zeros((1000, 1000, 3), np.uint8)
        if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
            points.append((vals[4], vals[5]))

        drawPoints(img, points)
        cv2.imshow("Output", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
