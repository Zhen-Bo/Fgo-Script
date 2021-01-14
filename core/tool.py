import os
import subprocess
import numpy as np
from cv2 import cv2
import time


class adbKit():
    def __init__(self, device, debug=False) -> None:
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.debug = debug
        self.capmuti = 1
        self.device = device
        self.breakline = self.get_SDK()

    def debug_get_write(self):
        t1 = time.time()
        pipe = subprocess.Popen("{0}/adb/adb.exe -s {1} shell screencap -p".format(self.path, self.device),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read()
        print(image_bytes[0:10])
        image_bytes = image_bytes.replace(b'\r\n', b'\n')
        print(image_bytes[0:10])
        t2 = time.time()
        image = cv2.imdecode(np.frombuffer(
            image_bytes, dtype='uint8'), cv2.IMREAD_COLOR)
        print("耗時 {0} 秒".format(round(t2-t1, 2)))
        cv2.imwrite("screenshot.png", image)
        raw = input("按Enter鍵關閉視窗")

    def get_SDK(self):
        SDK_version = subprocess.Popen("{0}/adb/adb.exe -s {1} shell getprop ro.build.version.release".format(
            self.path, self.device), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        SDK_version = SDK_version.stdout.read().decode("utf-8")
        if int(SDK_version[0]) >= 7:
            return '\r\n'
        elif int(SDK_version[0]) <= 5:
            return '\r\r\n'
        else:
            print("不是android5或android7")

    def screenshots(self, raw=False):
        pipe = subprocess.Popen("{0}/adb/adb.exe -s {1} shell screencap -p".format(self.path, self.device),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read()
        image_bytes = image_bytes.replace('{0}'.format(
            self.breakline).encode(encoding="utf-8"), b'\n')
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
        os.system(
            '{0}/adb/adb.exe -s {1} shell input tap {2} {3}'.format(self.path, self.device, Px, Py))

    def swipe(self, x1, y1, x2, y2, delay):
        cmdSwipe = '{0}/adb/adb.exe -s {1} shell input swipe {2} {3} {4} {5} {6}'.format(
            self.path, self.device, int(x1), int(y1), int(x2), int(y2), int(delay*1000))
        if self.debug:
            print('[ADB]adb shell swipe from X:{0} Y:{1} to X:{2} Y:{3} Delay:{4}'.format(
                int(x1), int(y1), int(x2), int(y2), int(delay*1000)))
        os.system(cmdSwipe)


class tool():
    def __init__(self, device, debug=False) -> None:
        self.debug = debug
        self.adbkit = adbKit(device)
        self.adbkit.capmuti = self.get_width_muti()
        self.screenshot = None

    def get_width_muti(self):
        sample = self.adbkit.screenshots(raw=True)
        return sample.shape[0] / 720

    def compare(self, img_list, acc=0.85, special=False):
        imgs = []
        self.screenshot = self.adbkit.screenshots()
        for item in img_list:
            imgs.append(cv2.imread(item))

        if special:
            cv2.rectangle(self.screenshot, (0, 0), (1280, 420),
                          color=(0, 0, 0), thickness=-1)
        for img in imgs:
            find_height, find_width = img.shape[:2:]
            result = cv2.matchTemplate(
                self.screenshot, img, cv2.TM_CCOEFF_NORMED)
            reslist = cv2.minMaxLoc(result)
            if self.debug:
                cv2.rectangle(self.screenshot, reslist[3], (
                    reslist[3][0]+find_width, reslist[3][1]+find_height), color=(0, 250, 0), thickness=2)
            if reslist[1] > acc:
                if self.debug:
                    print("[Detect]acc rate:", round(reslist[1], 2))
                pos = [reslist[3][0], reslist[3][1]]
                pos = [x*self.adbkit.capmuti for x in pos]
                return pos, find_height*self.adbkit.capmuti, find_width*self.adbkit.capmuti
        if special:
            return False, 0, 0
        else:
            return False

    def tap(self, pos, raw=False):
        if raw:
            self.adbkit.click(pos[0], pos[1], raw=True)
        else:
            self.adbkit.click(pos[0], pos[1])

    def swipe(self, x1, y1, x2, y2, delay):
        self.adbkit.swipe(x1, y1, x2, y2, delay)
