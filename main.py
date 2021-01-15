from configparser import ConfigParser
import os
from re import escape
from core import decoder
from core.auto import auto
from core import client
import sys


def get_cfg(path):
    cfg_path = "{}/UserData/config".format(path)
    file_list = os.listdir(cfg_path)
    cfg_list = []
    for cfg in file_list:
        if ".ini" in cfg:
            cfg_list.append(cfg)
    return cfg_list


def select_cfg(cfg_list):
    print("請選擇設定檔")
    i = 1
    for cfg in cfg_list:
        print("\033[1;34m {0}: {1}\033[0m".format(i, cfg))
        i += 1
    print("\033[1;31m e: 離開\033[0m")
    try:
        inputIndex = input(
            " 請輸入設定檔編號 [0 ~ {0}]: ".format(i-1))
        value = int(inputIndex)
        if value >= i:
            raise Exception("index is to big.")
        return value
    except (KeyboardInterrupt, SystemExit):
        raise Exception("KeyboardInterrupt")
    except Exception as e:
        if "e" == inputIndex or "E" == inputIndex:
            return -1
        else:
            print(
                "\033[1;31m編號錯誤,請確認後輸入\033[0m")
            input("請輸入enter繼續")
            return select_cfg(cfg_list)


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    os.system("{0}/adb/adb.exe kill-server".format(path))
    os.system("{0}/adb/adb.exe start-server".format(path))
    while True:
        os.system('cls')
        try:
            device = client.get_devices(path)
        except Exception as e:
            print(e.args[0])
            break
        print("\033[1;33m你選擇的設備是: {}\n\033[0m".format(device))
        try:
            cfg_name = get_cfg(path)[int(select_cfg(get_cfg(path)))-1]
        except Exception as e:
            print(e.args[0])
            break
        print("\033[1;33m你選擇的設定檔是: {}\n\033[0m".format(cfg_name))
        ini_path = "{}/UserData/config/{}".format(path, cfg_name)
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
            round = auto("menu.png", support, int(apple_count), apple, device, int(
                recover_time) * 60, run_time=int(run_times), ver=ver)
            instr = decoder.decode(codelist)
            round.quick_start(True)
            for runs in range(int(run_times)):
                for i in range(0, len(instr)):
                    exec(instr[i])
        except Exception as e:
            input("按下Enter結束執行                       ")
        finally:
            ctrl = input("請輸入Enter繼續,或輸入'e'已離開程式")
            if ctrl.lower() == "e":
                break
            else:
                os.system("cls")
