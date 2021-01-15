import time
import random
import os
from types import coroutine
from core.tool import tool
from configparser import ConfigParser


class auto():
    def __init__(self, ckp, spt, apl_count, apl_type, devices, timer=12000, run_time=1, ver="JP", debug=False):
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.checkpoint = ckp
        self.support = []
        self.support = self.get_support(spt)
        self.counts = int(apl_count)  # apple counts
        self.apple = apl_type
        self.timer = int(timer)
        self.cfg = ConfigParser()
        self.cfg.read("{0}/core/button.ini".format(self.path))
        self.run_time = run_time
        self.total_time = 0
        self.now_time = 0
        self.t_begin = 0
        self.t_end = 0
        self.adbtool = tool(devices, debug=debug)
        self.ver = ver
        self.debug = debug

    def get_support(self, spt):
        if os.path.isfile("{0}/UserData/support/{1}".format(self.path, spt)):
            support = []
            support.append("{0}/UserData/support/{1}".format(self.path, spt))
            return support
        elif os.path.isdir("{0}/UserData/support/{1}".format(self.path, spt)):
            support = []
            for each in os.listdir("{0}/UserData/support/{1}".format(self.path, spt)):
                support.append(
                    "{0}/UserData/support/{1}/{2}".format(self.path, spt, each))
            return support
        else:
            print("無法找到助戰圖片")

    def get_img_path(self, img_name):
        img = []
        img_path = "{0}/images/{1}/{2}".format(self.path, self.ver, img_name)
        img.append(img_path)
        return img

    def quick_start(self, first=False):
        self.select_task(self.checkpoint, first)
        time.sleep(1)
        self.advance_support(self.support)
        if first or self.now_time == 1:
            self.start_battle()

    def select_task(self, ckp: str, first=False):
        if first or self.now_time == 0:
            print("[INFO] Waiting Task selected")
            # self.adbtool.compare(self.get_img_path(self.checkpoint)):
            while not self.adbtool.compare(self.get_img_path(self.checkpoint)):
                pass
            self.adbtool.tap((1100, 170))
        time.sleep(0.5)
        self.t_begin = time.time()
        if self.adbtool.compare(self.get_img_path("noap.png")):
            print("[INFO] Out of AP!")
            if self.counts >= 0:
                self.counts -= 1
                if self.counts == -1:
                    self.adbtool.tap((635, 610))
                    self.wait_ap(self.timer)
                    self.select_task(self.checkpoint, first=True)
                else:
                    self.eat_apple()
            elif self.counts == -1:
                self.adbtool.tap((635, 610))
                self.wait_ap(self.timer)
                self.select_task(self.checkpoint, first=True)
            else:
                print("[INFO] Out of appale count")
                raise Exception("[INFO]Out of AP!")
        self.now_time += 1
        print("[INFO] Task selected.")

    def eat_apple(self):
        print("[INFO]Select apple:", end='')
        if self.apple == 'au':
            print("Au")
            self.adbtool.tap((375, 320))
        elif self.apple == 'ag':
            print("Ag")
            self.adbtool.tap((375, 470))
        elif self.apple == 'sq':
            print("Sq")
            self.adbtool.tap((375, 170))
        time.sleep(0.2)
        self.adbtool.tap((830, 560))
        print("[INFO] Remain apple counts:", self.counts)

    def wait_ap(self, timer):
        tStart = time.time()
        tEnd = time.time()
        print("[INFO] Start to wait AP")
        while not int(tEnd - tStart) >= timer:
            remain = timer - int(tEnd - tStart)
            if remain <= 60:
                print("[INFO] Remain", remain, "seconds", end='\r')
            else:
                remain /= 60.0
                remain = round(remain, 1)
                print("[INFO] Remain", remain, "minutes", end='\r')
            for i in range(30):  # note i用來計時沒用到
                tEnd = time.time()
                if int(tEnd - tStart) >= timer:
                    break
                time.sleep(1)

    def update_support(self):
        if self.adbtool.compare(self.get_img_path("update.png")):
            self.adbtool.tap((835, 125))
            time.sleep(0.2)
            if self.adbtool.compare(self.get_img_path("close.png")):
                self.adbtool.tap((640, 560))
                print("[INFO] Wait to refresh friend list")
                time.sleep(2)
            else:
                self.adbtool.tap((840, 560))
                print("[INFO] friend list refresh")

    def advance_support(self, spt):
        flag1 = True
        flag2 = True
        # TODO 檢查確定進選好有畫面後再繼續動作
        while flag1:
            spt_pos = self.adbtool.compare(spt)
            if spt_pos == False:
                print("[INFO] Friend not found", end='\r')
                if flag2:
                    bar_pos = self.adbtool.compare(
                        self.get_img_path("bar.png"))
                    if bar_pos:
                        if self.debug:
                            print("no bar")
                        self.update_support()
                    else:
                        if self.debug:
                            print("have bar")
                        flag2 = False
                        end_pos = self.adbtool.compare(
                            self.get_img_path("friendEnd.png"))
                        if end_pos:
                            print("[INFO] End of friend list")
                            self.update_support()
                            flag2 = True
                        else:
                            gap_pos, gap_h, gap_w = self.adbtool.compare(
                                self.get_img_path("friend_gap.png"), 0.8, True)
                            if gap_pos:
                                gap_pos = [x for x in gap_pos]
                                self.adbtool.swipe(
                                    gap_pos[0]+(gap_w/2), gap_pos[1]+(gap_h/2), gap_pos[0]+(gap_w/2), 210, 1.5)
                else:
                    end_pos = self.adbtool.compare(
                        self.get_img_path("friendEnd.png"), acc=0.8)
                    if end_pos != False:
                        print("[INFO] End of friend list")
                        self.update_support()
                        flag2 = True
                    else:
                        if self.debug:
                            print("swipe down")
                        gap_pos, gap_h, gap_w = self.adbtool.compare(
                            self.get_img_path("friend_gap.png"), 0.8, True)
                        if gap_pos:
                            gap_pos = [x for x in gap_pos]
                            self.adbtool.swipe(
                                gap_pos[0]+(gap_w/2), gap_pos[1]+(gap_h/2), gap_pos[0]+(gap_w/2), 210, 1.5)
            else:
                flag1 = False
                self.adbtool.tap((int(spt_pos[0][0])+int(spt_pos[2]/2),
                                  int(spt_pos[0][1])+int(spt_pos[1]/2)), raw=True)

    def start_battle(self):
        while not self.adbtool.compare(self.get_img_path("start.png")):
            pass
        self.adbtool.tap((1180, 670))
        print("[INFO] Battle started.  ")

    def select_servant_skill(self, skill: int, tar: int = 0):
        time.sleep(0.5)
        while not self.adbtool.compare(self.get_img_path("attack.png")):
            print("[BATTLE] Waiting for Attack button", end='\r')
            self.adbtool.tap((920, 45))
        pos = self.cfg['skills']['%s' % skill]
        pos = pos.split(',')
        self.adbtool.tap(pos)
        if tar != 0:
            print("[Skill] Use servent", str(int((skill-1)/3 + 1)),
                  "skill", str((skill-1) % 3 + 1), "to servent", tar)
            self.select_servant(tar)
        else:
            print("[Skill] Use servent", str(int((skill-1)/3 + 1)),
                  "skill", str((skill-1) % 3 + 1), "      ")

    def select_servant(self, servant: int):
        time.sleep(0.5)
        while not self.adbtool.compare(self.get_img_path("select.png")):
            print("[SKILL] Waiting for servent select", end='\r')
        pos = self.cfg['servent']['%s' % servant]
        pos = pos.split(',')
        self.adbtool.tap(pos)

    def select_cards(self, cards):
        time.sleep(0.5)
        while not self.adbtool.compare(self.get_img_path("attack.png")):
            print("[BATTLE] Waiting for Attack button", end='\r')
            self.adbtool.tap((920, 45))
        # tap ATTACK
        pos = self.cfg['attack']['button']
        pos = pos.split(',')
        self.adbtool.tap(pos)
        time.sleep(1.2)
        i = 0
        while "x" in cards:
            if cards[i] == "x":
                x = random.randrange(1, 6)
                if x in cards:
                    continue
                else:
                    cards[i] = x
                    i += 1
            else:
                i += 1
        # while len(cards) < 3:
        #     x = random.randrange(1, 6)
        #     if x in cards:
        #         continue
        #     cards.append(x)
        # tap CARDS
        for card in cards:
            pos = self.cfg['attack']['%s' % card]
            pos = pos.split(',')
            self.adbtool.tap(pos)
        print("[BATTLE] Selected cards: ", cards)

    def select_master_skill(self, skill: int, org: int = 0, tar: int = 0):
        time.sleep(0.3)
        while not self.adbtool.compare(self.get_img_path("attack.png")):
            print("[BATTLE] Waiting for Attack button", end='\r')
            self.adbtool.tap((920, 45))
        self.toggle_master_skill()
        pos = self.cfg['master']['%s' % skill]
        pos = pos.split(',')
        pos = [x for x in pos]
        self.adbtool.tap(pos)
        print("[M_Skill] Use master skill", skill)
        if org != 0 and tar == 0:
            self.select_servant(org)
        elif org != 0:
            self.change_servant(org, tar)

    def toggle_master_skill(self):
        time.sleep(0.2)
        while not self.adbtool.compare(self.get_img_path("attack.png")):
            print("[BATTLE] Waiting for Attack button", end='\r')
            self.adbtool.tap((920, 45))
        pos = self.cfg['master']['button']
        pos = pos.split(',')
        self.adbtool.tap(pos)
        print("[M_Skill] Toggle master skill bar")

    def change_servant(self, org: int, tar: int):
        time.sleep(0.2)
        while not self.adbtool.compare(self.get_img_path("order_change.png")):
            print("[M_Skill] Waiting for order change")
        pos = self.cfg['servent']['s%s', org]
        pos = pos.split(',')
        self.adbtool.tap(pos)
        time.sleep(0.1)
        pos = self.cfg['servent']['a%s', tar]
        pos = pos.split(',')
        self.adbtool.tap(pos)
        time.sleep(0.1)
        self.adbtool.tap((650, 620))  # confirm btn

    def finish_battle(self):
        while not self.adbtool.compare(self.get_img_path("next.png")):
            print("[FINISH] Waiting next button", end='\r')
            self.adbtool.tap((920, 45))
        print("[FINISH] Battle finish      ")
        self.adbtool.tap((1105, 670))
        if self.now_time < self.run_time:
            continue_flag = True
        else:
            continue_flag = False
        ckp = False
        flag = True
        friend_flag = False
        while flag:
            time.sleep(0.1)
            pos = self.adbtool.compare(self.get_img_path("friendrequest.png"))
            self.adbtool.tap((920, 45))
            if pos and not friend_flag:
                self.adbtool.tap((330, 610))
                friend_flag = True
                print("[FINISH] Reject friend request")
            else:
                pos = self.adbtool.compare(self.get_img_path("continue.png"))
                if pos:
                    flag = False
                elif self.adbtool.compare(self.get_img_path(self.checkpoint)):
                    flag = False
                    ckp = True
        self.t_end = time.time()
        self.total_time += int(self.t_end-self.t_begin)
        print("執行 {0} 次;用時 {1} 秒; 總計 {2} 秒;".format(
            self.now_time, int(self.t_end-self.t_begin), self.total_time))
        if continue_flag:
            if not ckp:
                pos = self.adbtool.compare(self.get_img_path("continue.png"))
                self.adbtool.tap((int(pos[0][0])+int(pos[2]/2),
                                  int(pos[0][1])+int(pos[1]/2)), raw=True)
            self.quick_start(ckp)
        elif self.adbtool.compare(self.get_img_path("noap.png")):
            self.adbtool.tap((635, 610))
        elif continue_flag == False:
            pos = self.adbtool.compare(self.get_img_path("close.png"))
            while not pos:
                pos = self.adbtool.compare(self.get_img_path("close.png"))
                ckp = self.adbtool.compare(self.get_img_path(self.checkpoint))
                if ckp:
                    break
            if pos and not ckp:
                self.adbtool.tap(pos[0], raw=True)
