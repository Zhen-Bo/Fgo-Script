from configparser import ConfigParser
import errno
import os
import os
from core import decoder
from core.auto import auto

if __name__ == '__main__':
    while True:
        cfg_name = input("請輸入設定檔名稱(不需輸入.ini):")
        ini_path = "UserData/config/" + cfg_name + ".ini"
        while not os.path.isfile(ini_path):
            cfg_name = input("請輸入設定檔名稱(不需輸入.ini):")
            ini_path = "UserData/config/" + cfg_name + ".ini"
        cfg = ConfigParser()
        cfg.read(ini_path)
        ver = cfg['version']['version']
        support = cfg['support']['support']
        apple_count = cfg['ap_recover']['count']
        apple = cfg['ap_recover']['apple']
        recover_time = cfg['recover_time']['recover_time']
        battle1_str = cfg['default_skill']['battle1']
        battle2_str = cfg['default_skill']['battle2']
        battle3_str = cfg['default_skill']['battle3']
        crd1_str = cfg['default_card']['battle1']
        crd2_str = cfg['default_card']['battle2']
        crd3_str = cfg['default_card']['battle3']

        codelist = [battle1_str, battle2_str,
                    battle3_str, crd1_str, crd2_str, crd3_str]
        run_times = input("請輸入次數")
        while not run_times.isdigit():
            os.system('cls')
            run_times = input("請輸入次數")
        try:
            round = auto("menu.png", support, int(apple_count), apple, int(
                recover_time) * 60, run_time=int(run_times), ver=ver)
            instr = decoder.decode(codelist)
            round.quick_start(True)
            for runs in range(int(run_times)):
                for i in range(0, len(instr)):
                    exec(instr[i])
        except Exception as e:
            print("[ERROR] " + e)
        finally:
            input("請輸入Enter繼續")
            os.system("cls")
