from cv2 import cv2
from core import adb

debug = False

adbkit = adb.adbKit()


def standby(template, acc=0.85, special=False):
    adbkit.debug = debug
    target_img = adbkit.screenshots()
    if special == True:
        cv2.rectangle(target_img, (0, 0), (1280, 420),
                      color=(0, 0, 0), thickness=-1)
    find_img = cv2.imread(str(template))
    find_height, find_width = find_img.shape[:2:]

    # 模板匹配
    result = cv2.matchTemplate(target_img, find_img, cv2.TM_CCOEFF_NORMED)
    reslist = cv2.minMaxLoc(result)

    if debug:
        cv2.rectangle(target_img, reslist[3], (reslist[3][0]+find_width,
                                               reslist[3][1]+find_height), color=(0, 255, 0), thickness=2)
        #cv2.imwrite("screencap.png", target_img)
        cv2.imshow("screenshots", target_img)
        cv2.waitKey(0)

    if reslist[1] > acc:
        if debug:
            print("[Detect]acc rate:", round(reslist[1], 2))
        return reslist[3], find_height, find_width
    else:
        if debug:
            print("[Detect]acc rate:", round(reslist[1], 2))
        if special:
            return False, 0, 0
        else:
            return False


def tap(pos):
    adbkit.click(pos[0], pos[1])


def swipe(x1, y1, x2, y2, delay):
    adbkit.swipe(x1, y1, x2, y2, delay)
