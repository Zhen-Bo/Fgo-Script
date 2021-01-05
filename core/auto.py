import time
import random
from core import util
from configparser import ConfigParser


class auto():
    def __init__(self, ckp: str, spt: str, apl: (int, str) = (0, ""), timer=12000, debug=False):
        self.checkpoint = ckp
        self.support = spt
        self.counts = int(apl[0])  # apple counts
        self.apple = apl[1]
        self.timer = int(timer)
        self.cfg = ConfigParser()
        self.cfg.read("core/ini/button.ini")
        self.debug = debug

    def debugfuc(self):
        print(self.cfg.sections())

    def quick_start(self, advance=True):
        self.select_task(self.checkpoint)
        self.advance_support()
        self.start_battle()

    def select_task(self, ckp: str):
        print("[INFO] Waiting Task selected")
        while not util.standby(self.checkpoint):
            time.sleep(0.2)
        util.tap(1100, 170)
        time.sleep(1)
        if util.standby("images/noap.png"):
            print("[INFO] Out of AP!")
            if self.counts > 0:
                self.counts -= 1
                self.eat_apple()
            elif self.counts == -1:
                util.tap(635, 610)
                self.wait_ap(self.timer)
                self.select_task(self.checkpoint)
            else:
                print("[INFO] Out of appale count")
                raise Exception("[INFO]Out of AP!")
        print("[INFO] Task selected.")

    def eat_apple(self):
        print("[INFO]Select apple:", end='')
        if self.apple == 'au':
            print("Au")
            util.tap(375, 320)
        elif self.apple == 'ag':
            print("Ag")
            util.tap(375, 470)
        elif self.apple == 'sq':
            print("Sq")
            util.tap(375, 170)
        time.sleep(0.2)
        util.tap(830, 560)
        print("[INFO] Remain apple counts:", self.counts)

    def wait_ap(self, timer):
        tStart = time.time()
        tEnd = time.time()
        print("[INFO] Start to wait AP")
        while not int(tEnd - tStart) >= timer:
            remain = timer - int(tEnd - tStart)
            if remain <= 60:
                print("[INFO] Remain", remain, "seconds")
            else:
                remain /= 60.0
                remain = round(remain, 1)
                print("[INFO] Remain", remain, "minutes")
            for i in range(30):
                tEnd = time.time()
                if int(tEnd - tStart) >= timer:
                    break
                time.sleep(1)

    def update_support(self):
        if util.standby("images/update.png"):
            util.tap(835, 125)
            time.sleep(0.5)
            if util.standby("images/close.png"):
                util.tap(640, 560)
                print("[INFO] Wait to refresh friend list")
                time.sleep(2)
            else:
                util.tap(840, 560)
                print("[INFO] friend list refresh")
            time.sleep(0.5)

    def advance_support(self, spt: str = None, tms: int = 3):
        if spt is None:
            spt = self.support
        flag1 = True
        flag2 = True
        while flag1:
            spt_pos = util.standby(spt)
            if spt_pos == False:
                print("[INFO] Friend not found")
                if flag2:
                    bar_pos = util.standby("images/bar.png")
                    if bar_pos == False:
                        if self.debug:
                            print("no bar")
                        self.update_support()
                    else:
                        if self.debug:
                            print("have bar")
                        flag2 = False
                        end_pos = util.standby("images/friendEnd.png")
                        end_pos = end_pos[:1]
                        if end_pos == False:
                            print("[INFO] End of friend list")
                            self.update_support()
                            flag2 = True
                        else:
                            gap_pos, gap_h, gap_w = util.standby(
                                "images/friend_gap.png", 0.8, True)
                            util.swipe(
                                gap_pos[0]+(gap_w/2), gap_pos[1]+(gap_h/2), gap_pos[0]+(gap_w/2), 210, 1.5)
                else:
                    end_pos = util.standby("images/friendEnd.png")
                    if end_pos[0] != False:
                        print("[INFO] End of friend list")
                        self.update_support()
                        flag2 = True
                    else:
                        if self.debug:
                            print("swipe down")
                        gap_pos, gap_h, gap_w = util.standby(
                            "images/friend_gap.png", 0.8, True)
                        util.swipe(
                            gap_pos[0]+(gap_w/2), gap_pos[1]+(gap_h/2), gap_pos[0]+(gap_w/2), 210, 1.5)
            else:
                flag1 = False
                spt_center = [int(spt_pos[0][0]+5),
                              int(spt_pos[0][1]+5)]
                util.list_tap(spt_center)

    def start_battle(self):
        while not util.standby("images/start.png"):
            time.sleep(0.2)
        util.tap(1180, 670)
        print("[INFO] Battle started.")

    def select_servant_skill(self, skill: int, tar: int = 0):
        while not util.standby("images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end="\r")
            time.sleep(1)
        pos = self.cfg['skills']['%s' % skill]
        pos = pos.split(',')
        util.tap(pos[0], pos[1])
        if tar != 0:
            print("[Skill] Use servent", str(int((skill-1)/3 + 1)),
                  "skill", str((skill-1) % 3 + 1), "to servent", tar)
            time.sleep(1)
            self.select_servant(tar)
        else:
            print("[Skill] Use servent", str(int((skill-1)/3 + 1)),
                  "skill", str((skill-1) % 3 + 1))
            time.sleep(1)

    def select_servant(self, servant: int):
        while not util.standby("images/select.png"):
            print("[SKILL] Waiting for servent select")
            time.sleep(0.2)
        pos = self.cfg['servent']['%s' % servant]
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(0.5)

    def select_cards(self, cards: [int]):
        time.sleep(1)
        while not util.standby("images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end="\r")
            time.sleep(0.2)
        # tap ATTACK
        pos = self.cfg['attack']['button']
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(1)
        while len(cards) < 3:
            x = random.randrange(1, 6)
            if x in cards:
                continue
            cards.append(x)
        # tap CARDS
        for card in cards:
            pos = self.cfg['attack']['%s' % card]
            pos = pos.split(',')
            util.list_tap(pos)
            time.sleep(0.2)
        print("[BATTLE] Selected cards: ", cards)

    def select_master_skill(self, skill: int, org: int = 0, tar: int = 0):
        while not util.standby("images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end="\r")
            time.sleep(0.2)
        self.toggle_master_skill()
        pos = self.cfg['master']['%s' % skill]
        pos = pos.split(',')
        util.list_tap(pos)
        print("[M_Skill] Use master skill", skill)
        if org != 0 and tar == 0:
            self.select_servant(org)
        elif org != 0:
            self.change_servant(org, tar)

    def toggle_master_skill(self):
        while not util.standby("images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end="\r")
            time.sleep(0.2)
        pos = self.cfg['master']['button']
        pos = pos.split(',')
        util.list_tap(pos)
        print("[M_Skill] Toggle master skill bar")

    def change_servant(self, org: int, tar: int):
        while not util.standby("images/order_change.png"):
            print("[M_Skill] Waiting for order change")
            time.sleep(0.2)
        pos = self.cfg['servent']['s%s', org]
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(0.1)
        pos = self.cfg['servent']['a%s', tar]
        pos = pos.split(',')
        util.list_tap(pos)
        time.sleep(0.1)
        util.tap(650, 620)  # confirm btn

    def finish_battle(self):
        while not util.standby("images/next.png"):
            print("[FINISH] Waiting next button")
            util.tap(920, 45)
            self.needattack()
            time.sleep(0.2)
        util.tap(1105, 670)
        flag = 0
        while not util.standby(self.checkpoint):
            if flag == 0 and util.standby("images/friendrequest.png"):
                print("[FINISH] Check friend request screen")
                util.tap(330, 610)
                print("[FINISH] Reject friend request")
                flag = 1
            elif flag == 1:
                util.tap(920, 45)
            else:
                util.tap(920, 45)
            time.sleep(1)
        print("[INFO] Battle Finished.")

    def waiting_phase(self, phase: int):
        if phase == 1:
            while not util.standby("images/phase1.png", 0.78):
                util.tap(920, 45)
                if self.debug:
                    print("Waiting for phase1")
                time.sleep(0.2)
        elif phase == 2:
            while not util.standby("images/phase2.png", 0.78):
                util.tap(920, 45)
                if self.debug:
                    print("Waiting for phase2")
                self.needattack()
                time.sleep(0.2)
        elif phase == 3:
            while not util.standby("images/phase3.png", 0.78):
                util.tap(920, 45)
                if self.debug:
                    print("Waiting for phase3")
                self.needattack()
                time.sleep(0.2)

    def needattack(self):
        if util.standby("images/attack.png"):
            print("[BATTLE] Need extra attack")
            self.select_cards([1, 2, 3])
        else:
            print("[BATTLE] Dont need extra attack")
