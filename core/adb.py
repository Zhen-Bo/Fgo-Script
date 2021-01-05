"""ADB"""
import os
import subprocess
import numpy as np
from cv2 import cv2


class adbKit(object):
    def __init__(self) -> None:
        os.system("/adb/adb.exe kill-server")
        os.system("/adb/adb.exe start-server")

    def screenshots(self):
        pipe = subprocess.Popen("/adb/adb.exe shell screencap -p",
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        target_img = cv2.imdecode(np.fromstring(
            image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return target_img
        # os.system('/adb/adb.exe shell screencap -p /sdcard/screencap.png')
        # os.system('/adb/adb.exe pull /sdcard/screencap.png > tmp/tmp.log')

    def click(self, pointx, pointy):
        Px = str(pointx)
        Py = str(pointy)
        print('[ADB]adb shell input tap ' + Px + ' ' + Py)
        os.system('/adb/adb.exe shell input tap ' + Px + ' ' + Py)

    def swipe(self, x1, y1, x2, y2, delay):
        cmdSwipe = '/adb/adb.exe shell input swipe {0} {1} {2} {3} {4}'.format(
            int(x1), int(y1), int(x2), int(y2), int(delay*1000))
        print('[ADB]adb shell swipe from X:{0} Y:{1} to X:{2} Y:{3} Delay:{4}'.format(
            int(x1), int(y1), int(x2), int(y2), int(delay*1000)))
        os.system(cmdSwipe)


# adbKit().screenshots()
