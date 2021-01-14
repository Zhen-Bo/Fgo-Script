import os
import subprocess
import numpy as np
from cv2 import cv2
import time


class adbKit():
    def __init__(self, debug=False) -> None:
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.debug = debug
        self.capmuti = 1
        os.system("{0}/core/adb/adb.exe kill-server".format(self.path))
        os.system("{0}/core/adb/adb.exe start-server".format(self.path))

    def debug_get(self):
        t1 = time.time()
        pipe = subprocess.Popen("{0}/core/adb/adb.exe shell screencap -p".format(self.path),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read()
        print(image_bytes[0:10])
        image_bytes = image_bytes.replace(b'\r\n', b'\n')
        print(image_bytes[0:10])
        t2 = time.time()
        image = cv2.imdecode(np.frombuffer(
            image_bytes, dtype='uint8'), cv2.IMREAD_COLOR)
        print(t2-t1)
        raw = input("按Enter鍵關閉視窗")

    def screenshots(self, raw=False):
        pipe = subprocess.Popen("/adb/adb.exe shell screencap -p",
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read()
        # android5寫法,android7為\r\n
        image_bytes = image_bytes.replace(b'\r\n', b'\n')
        image = cv2.imdecode(np.frombuffer(
            image_bytes, dtype='uint8'), cv2.IMREAD_COLOR)
        if image.shape[0] != 720 and image.shape[1] != 1280 and not raw:
            image = self.reimage(image)
        return image

    def reimage(self, images):
        images = cv2.resize(images, (1280, 720))
        return images

    def click(self, pointx, pointy, raw=False):
        if raw:
            Px = str(pointx)
            Py = str(pointy)
        else:
            Px = str(int(pointx)*self.capmuti)
            Py = str(int(pointy)*self.capmuti)
        if self.debug:
            print('[ADB]adb shell input tap ' + Px + ' ' + Py)
        os.system('/adb/adb.exe shell input tap ' + Px + ' ' + Py)

    def swipe(self, x1, y1, x2, y2, delay):
        cmdSwipe = '/adb/adb.exe shell input swipe {0} {1} {2} {3} {4}'.format(
            int(x1), int(y1), int(x2), int(y2), int(delay*1000))
        if self.debug:
            print('[ADB]adb shell swipe from X:{0} Y:{1} to X:{2} Y:{3} Delay:{4}'.format(
                int(x1), int(y1), int(x2), int(y2), int(delay*1000)))
        os.system(cmdSwipe)


# ad = adbKit(debug=True)
# ad.click(70, 1250)
