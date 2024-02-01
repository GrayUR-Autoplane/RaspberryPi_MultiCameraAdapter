from ast import Try
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QApplication, QWidget
from picamera2 import Picamera2
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import QThread
import RPi.GPIO as gp
import time
from datetime import datetime
import os
import numpy as np

width = 2592
height = 1944
cams = ["A", "B", "C", "D"]
camera = "A"
video = True
iterateCams = True
#use large value for max framerate
framerate = 1
timebuffer = 0.1
adapter_info = {  
    "A" : {   
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x04",
        "gpio_sta":[0,0,1],
    }, "B" : {
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x05",
        "gpio_sta":[1,0,1],
    }, "C" : {
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x06",
        "gpio_sta":[0,1,0],
    },"D" : {
        "i2c_cmd":"i2cset -y 10 0x70 0x00 0x07",
        "gpio_sta":[1,1,0],
    }
}

class WorkThread(QThread):

    def __init__(self):
        super(WorkThread,self).__init__()
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)


    def select_channel(self,index):
        channel_info = adapter_info.get(index)
        if channel_info == None:
            print("Can't get this info")
        gpio_sta = channel_info["gpio_sta"] # gpio write
        gp.output(7, gpio_sta[0])
        gp.output(11, gpio_sta[1])
        gp.output(12, gpio_sta[2])

    def init_i2c(self,index):
        channel_info = adapter_info.get(index)
        os.system(channel_info["i2c_cmd"]) # i2c write

    def run(self):
        global picam2
        # picam2 = Picamera2()
        # picam2.configure( picam2.still_configuration(main={"size": (320, 240),"format": "BGR888"},buffer_count=1))

        flag = False
        for item in cams:
            try:
                self.select_channel(item)
                self.init_i2c(item)
                time.sleep(0.5) 
                if flag == False:
                    flag = True
                else :
                    picam2.close()
                    # time.sleep(0.5) 
                print("init1 "+ item)
                picam2 = Picamera2()
                picam2.configure(picam2.create_video_configuration(main={"size": (width, height),"format": "BGR888"},buffer_count=2)) 
                #picam2.configure(picam2.create_preview_configuration(main={"size": (width, height),"format": "BGR888"},buffer_count=2)) 
                picam2.start()
                time.sleep(1)
                picam2.capture_array(wait=False)
                time.sleep(0.1)
            except Exception as e:
                print("except: "+str(e))

        directory = "testdata/FlightTest/"+"TestFlight_"+str(datetime.now())
        os.makedirs(directory)
        deltaT = 0.0
        frame = 0
        
        while video:
            print(deltaT)
            newDir = directory +"/"+ str(frame)
            os.makedirs(newDir)
            time.sleep(np.clip(((1.0/framerate)-deltaT),0,100))
            initalTime = time.time()
            for i in range(4):
                time.sleep(timebuffer)
                cam = cams[i]
                self.select_channel(cam)
                try:
                    buf = picam2.capture_array()
                    cvimg = QImage(buf, width, height,QImage.Format_RGB888)
                    pixmap = QPixmap(cvimg)
                    image_label.setPixmap(pixmap)
                    getTime = time.time() - initalTime
                    cvimg.save(newDir +"/cam_"+cam +"_"+ str(datetime.now()) + ".jpg")
                    saveTime = deltaT-getTime 
                    #print("image saved, it took: %f seconds" %(deltaT))
                    #print("get time: %f seconds," %(getTime)+"save time: %f seconds" %(saveTime))
                except Exception as e:
                    print("capture_buffer: "+ str(e))
                    os.abort()
            deltaT = time.time()-initalTime
            frame += 1

app = QApplication([])
window = QWidget()
layout_h = QHBoxLayout()
layout_v = QVBoxLayout()
image_label = QLabel()


# picam2 = Picamera2()

work = WorkThread()

if __name__ == "__main__":
    image_label.setFixedSize(width, height)
    window.setWindowTitle("Qt Picamera2 Arducam Multi Camera Demo")
    layout_h.addWidget(image_label)    
    layout_v.addLayout(layout_h,20)
    window.setLayout(layout_v)
    window.resize((int)(width/8),(int)(height/8))

    work.start()
    
    window.show()
    app.exec()
    work.quit()
    picam2.close()
