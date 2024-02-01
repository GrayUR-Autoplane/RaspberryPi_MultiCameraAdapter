import RPi.GPIO as gp
import os
from datetime import datetime

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)


def main():
    print('Start testing the camera A')
    i2c = "i2cset -y 1 0x70 0x00 0x04"
    os.system(i2c)
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    capture(1)
    print('Start testing the camera B') 
    i2c = "i2cset -y 1 0x70 0x00 0x05"
    os.system(i2c)
    gp.output(7, True)
    gp.output(11, False)
    gp.output(12, True)
    capture(2)
    print('Start testing the camera C')
    i2c = "i2cset -y 1 0x70 0x00 0x06"
    os.system(i2c)
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    capture(3)
    print('Start testing the camera D')
    i2c = "i2cset -y 1 0x70 0x00 0x07"
    os.system(i2c)
    gp.output(7, True)
    gp.output(11, True)
    gp.output(12, False)
    capture(4)
    
def capture(cam):
    #cmd = "libcamera-raw -t 2000 -o 'images/cam_%d_" %(cam) + str(datetime.now()) + ".mp4'"
    cmd = "libcamera-still -o 'images/cam_%d_" %(cam) + str(datetime.now()) + ".png'"
    os.system(cmd)

if __name__ == "__main__":
    #main()
    i2c = "i2cset -y 1 0x70 0x00 0x04"
    os.system(i2c)
    capture(1)
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
