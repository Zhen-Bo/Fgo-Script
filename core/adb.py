import os
import subprocess
import numpy as np
from cv2 import cv2


class adbKit(object):
    def __init__(self, debug=False) -> None:
        self.debug = debug
        os.system("/adb/adb.exe kill-server")
        os.system("/adb/adb.exe start-server")

    def screenshots(self):
        pipe = subprocess.Popen("/adb/adb.exe shell screencap -p",
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        image = cv2.imdecode(np.frombuffer(
            image_bytes, dtype='uint8'), cv2.IMREAD_COLOR)
        return image

    def click(self, pointx, pointy):
        Px = str(pointx)
        Py = str(pointy)
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
