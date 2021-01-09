import time
import random
from types import coroutine
from core import util
from configparser import ConfigParser


class auto():
    def __init__(self, ckp: str, spt: str, apl_count: int, apl_type: str = (0, ""), timer=12000, run_time=1, debug=False):
        self.checkpoint = ckp
        self.support = spt
        self.counts = int(apl_count)  # apple counts
        self.apple = apl_type
        self.timer = int(timer)
        self.cfg = ConfigParser()
        self.cfg.read("core/button.ini")
        self.debug = debug
        self.run_time = run_time
        self.total_time = 0
        self.now_time = 0
        self.t_begin = 0
        self.t_end = 0
        util.debug = self.debug

    def debugfuc(self):
        print(self.cfg.sections())

    def quick_start(self, first=False):
        self.select_task(self.checkpoint, first)
        self.advance_support()
        if first or self.now_time == 1:
            self.start_battle()

    def select_task(self, ckp: str, first=False):
        if first or self.now_time == 0:
            print("[INFO] Waiting Task selected")
            while not util.standby(self.checkpoint):
                time.sleep(0.2)
            util.tap((1100, 170))
            time.sleep(1)
        time.sleep(1)
        self.t_begin = time.time()
        if util.standby("core/images/noap.png"):
            print("[INFO] Out of AP!")
            if self.counts >= 0:
                self.counts -= 1
                if self.counts == -1:
                    util.tap((635, 610))
                    self.wait_ap(self.timer)
                    self.select_task(self.checkpoint, first=True)
                else:
                    self.eat_apple()
            elif self.counts == -1:
                util.tap((635, 610))
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
            util.tap((375, 320))
        elif self.apple == 'ag':
            print("Ag")
            util.tap((375, 470))
        elif self.apple == 'sq':
            print("Sq")
            util.tap((375, 170))
        time.sleep(0.2)
        util.tap((830, 560))
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
        if util.standby("core/images/update.png"):
            util.tap((835, 125))
            time.sleep(0.5)
            if util.standby("core/images/close.png"):
                util.tap((640, 560))
                print("[INFO] Wait to refresh friend list")
                time.sleep(2)
            else:
                util.tap((840, 560))
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
                print("[INFO] Friend not found", end='\r')
                if flag2:
                    bar_pos = util.standby("core/images/bar.png")
                    if bar_pos:
                        if self.debug:
                            print("no bar")
                        self.update_support()
                    else:
                        if self.debug:
                            print("have bar")
                        flag2 = False
                        end_pos = util.standby("core/images/friendEnd.png")
                        if end_pos:
                            print("[INFO] End of friend list")
                            self.update_support()
                            flag2 = True
                        else:
                            gap_pos, gap_h, gap_w = util.standby(
                                "core/images/friend_gap.png", 0.8, True)
                            if gap_pos:
                                util.swipe(
                                    gap_pos[0]+(gap_w/2), gap_pos[1]+(gap_h/2), gap_pos[0]+(gap_w/2), 210, 1.5)
                else:
                    end_pos = util.standby(
                        "core/images/friendEnd.png", acc=0.8, special=True)
                    if end_pos != False:
                        print("[INFO] End of friend list")
                        self.update_support()
                        flag2 = True
                    else:
                        if self.debug:
                            print("swipe down")
                        gap_pos, gap_h, gap_w = util.standby(
                            "core/images/friend_gap.png", 0.8, True)
                        if gap_pos:
                            util.swipe(
                                gap_pos[0]+(gap_w/2), gap_pos[1]+(gap_h/2), gap_pos[0]+(gap_w/2), 210, 1.5)
            else:
                flag1 = False
                util.tap((int(spt_pos[0][0])+int(spt_pos[2]/2),
                          int(spt_pos[0][1])+int(spt_pos[1]/2)))

    def start_battle(self):
        while not util.standby("core/images/start.png"):
            time.sleep(0.2)
        util.tap((1180, 670))
        print("[INFO] Battle started.")

    def select_servant_skill(self, skill: int, tar: int = 0):
        while not util.standby("core/images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end='\r')
            time.sleep(1)
        pos = self.cfg['skills']['%s' % skill]
        pos = pos.split(',')
        util.tap(pos)
        if tar != 0:
            print("[Skill] Use servent", str(int((skill-1)/3 + 1)),
                  "skill", str((skill-1) % 3 + 1), "to servent", tar)
            time.sleep(1)
            self.select_servant(tar)
        else:
            print("[Skill] Use servent", str(int((skill-1)/3 + 1)),
                  "skill", str((skill-1) % 3 + 1), "      ")
            time.sleep(1)

    def select_servant(self, servant: int):
        while not util.standby("core/images/select.png"):
            print("[SKILL] Waiting for servent select", end='\r')
            time.sleep(0.2)
        pos = self.cfg['servent']['%s' % servant]
        pos = pos.split(',')
        util.tap(pos)
        time.sleep(0.5)

    def select_cards(self, cards):
        time.sleep(1)
        while not util.standby("core/images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end='\r')
            time.sleep(0.2)
        # tap ATTACK
        pos = self.cfg['attack']['button']
        pos = pos.split(',')
        util.tap(pos)
        time.sleep(1.2)
        while len(cards) < 3:
            x = random.randrange(1, 6)
            if x in cards:
                continue
            cards.append(x)
        # tap CARDS
        for card in cards:
            pos = self.cfg['attack']['%s' % card]
            pos = pos.split(',')
            util.tap(pos)
        print("[BATTLE] Selected cards: ", cards)

    def select_master_skill(self, skill: int, org: int = 0, tar: int = 0):
        while not util.standby("core/images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end='\r')
            time.sleep(0.2)
        self.toggle_master_skill()
        pos = self.cfg['master']['%s' % skill]
        pos = pos.split(',')
        util.tap(pos)
        print("[M_Skill] Use master skill", skill)
        if org != 0 and tar == 0:
            self.select_servant(org)
        elif org != 0:
            self.change_servant(org, tar)

    def toggle_master_skill(self):
        while not util.standby("core/images/attack.png"):
            print("[BATTLE] Waiting for Attack button", end='\r')
            time.sleep(0.2)
        pos = self.cfg['master']['button']
        pos = pos.split(',')
        util.tap(pos)
        print("[M_Skill] Toggle master skill bar")

    def change_servant(self, org: int, tar: int):
        while not util.standby("core/images/order_change.png"):
            print("[M_Skill] Waiting for order change")
            time.sleep(0.2)
        pos = self.cfg['servent']['s%s', org]
        pos = pos.split(',')
        util.tap(pos)
        time.sleep(0.1)
        pos = self.cfg['servent']['a%s', tar]
        pos = pos.split(',')
        util.tap(pos)
        time.sleep(0.1)
        util.tap((650, 620))  # confirm btn

    def finish_battle(self):
        while not util.standby("core/images/next.png"):
            print("[FINISH] Waiting next button", end='\r')
            util.tap((920, 45))
            time.sleep(0.2)
        util.tap((1105, 670))
        if self.now_time < self.run_time:
            continue_flag = True
        else:
            continue_flag = False
        ckp = False
        flag = True
        friend_flag = False
        while flag:
            time.sleep(0.5)
            pos = util.standby("core/images/friendrequest.png")
            util.tap((920, 45))
            if pos and not friend_flag:
                util.tap((330, 610))
                friend_flag = True
                print("[FINISH] Reject friend request")
            else:
                pos = util.standby("core/images/continue.png")
                if pos:
                    flag = False
                elif util.standby(self.checkpoint):
                    flag = False
                    ckp = True
        self.t_end = time.time()
        self.total_time += int(self.t_end-self.t_begin)
        print("執行 {0} 次;用時 {1} 秒; 總計 {2} 秒;".format(
            self.now_time, int(self.t_end-self.t_begin), self.total_time))
        if continue_flag:
            if not ckp:
                pos = util.standby("core/images/continue.png")
                util.tap((int(pos[0][0])+int(pos[2]/2),
                          int(pos[0][1])+int(pos[1]/2)))
            self.quick_start(ckp)
        elif util.standby("core/images/noap.png"):
            util.tap((635, 610))
        elif not continue_flag:
            pos = util.standby("core/images/close.png")
            while not pos:
                pos = util.standby("core/images/close.png")
            util.tap(pos)
