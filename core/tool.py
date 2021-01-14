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
        os.system("{0}/adb/adb.exe kill-server".format(self.path))
        os.system("{0}/adb/adb.exe start-server".format(self.path))
        self.device = self.read_devices()
        index = self.selectDevices(self.device)
        self.device = self.device[index]
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
            raise Exception("不是android5或android7")

    def read_devices(self):
        devices = subprocess.Popen("{0}/adb/adb.exe devices".format(self.path),
                                   shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
        lists = devices.split("\n")
        devicesNames = []
        for item in lists:
            if(item.strip() == ""):
                continue
            elif (item.startswith("List of")):
                continue
            else:
                devicesNames.append(item.split("\t")[0])
        return devicesNames

    def selectDevices(self, devicesIds):
        print("Please Select Devices:")
        i = 0
        for deviceId in devicesIds:
            print("\033[1;34m {0}:{1}\033[0m".format(i, deviceId))
            i += 1
        print("\033[1;34m e: exit\033[0m")
        try:
            inputIndex = input(
                " Enter your device index [0 ~ {0}]:".format(i-1))
            value = int(inputIndex)
            if value >= i:
                raise Exception("index is to big.")
            return value
        except (KeyboardInterrupt, SystemExit):
            return -1
        except Exception as e:
            if "e" == inputIndex or "E" == inputIndex:
                return -1
            else:
                print(
                    "\033[1;31mYour select index is error, please try again.\033[0m")
                return self.selectDevices(devicesIds)

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
    def __init__(self, debug=False) -> None:
        self.debug = debug
        self.adbkit = adbKit()
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

    # debug = False
    # adbkit = adb.adbKit()

    # def get_width_muti():
    #     sample = adbkit.screenshots(raw=True)
    #     adbkit.capmuti = sample.shape[0] / 720


# def standby(template, acc=0.85, special=False):
#     adbkit.debug = debug
#     target_img = adbkit.screenshots()
#     if special == True:
#         cv2.rectangle(target_img, (0, 0), (1280, 420),
#                       color=(0, 0, 0), thickness=-1)
#     find_img = cv2.imread(str(template))
#     find_height, find_width = find_img.shape[:2:]
#     # 模板匹配
#     result = cv2.matchTemplate(target_img, find_img, cv2.TM_CCOEFF_NORMED)
#     reslist = cv2.minMaxLoc(result)
#     if debug:
#         cv2.rectangle(target_img, reslist[3], (reslist[3][0]+find_width,
#                                                reslist[3][1]+find_height), color=(0, 255, 0), thickness=2)
#         # cv2.imwrite("screencap.png", target_img)
#         cv2.imshow("screenshots", target_img)
#         cv2.waitKey(0)
#     if reslist[1] > acc:
#         if debug:
#             print("[Detect]acc rate:", round(reslist[1], 2))
#         pos = [reslist[3][0], reslist[3][1]]
#         pos = [x*adbkit.capmuti for x in pos]
#         return pos, find_height*adbkit.capmuti, find_width*adbkit.capmuti
#     else:
#         if debug:
#             print("[Detect]acc rate:", round(reslist[1], 2))
#         if special:
#             return False, 0, 0
#         else:
#             return False


# def tap(pos, raw=False):
#     if raw:
#         adbkit.click(pos[0], pos[1], raw=True)
#     else:
#         adbkit.click(pos[0], pos[1])


# def swipe(x1, y1, x2, y2, delay):
#     adbkit.swipe(x1, y1, x2, y2, delay)
