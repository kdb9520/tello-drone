from djitellopy import tello
from time import sleep

def main():
    me = connect()
    takeoff(me)
    premadeflight(me)


def connect():
    me = tello.Tello
    me.connect()
    print(me.get_battery())
    return me


def takeoff(me):
    me.takeoff()


def premadeflight(me):
    me.send_rc_control(0, 50, 0, 0)
    sleep(2)
    me.send_rc_control(30, 0, 0, 0)
    sleep(2)
    me.send_rc_control(0, 0, 0, 0)


def land(me):
    me.land()


if __name__ == '__main__':
    main()
