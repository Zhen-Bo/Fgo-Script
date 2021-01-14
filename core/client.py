import subprocess


def read_devices(path):
    devices = subprocess.Popen("{0}/adb/adb.exe devices".format(path),
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


def select_devices(devicesIds):
    print("請選擇你要控制的設備:")
    i = 0
    for deviceId in devicesIds:
        print("\033[1;34m {0}:{1}\033[0m".format(i, deviceId))
        i += 1
    print("\033[1;34m e: 離開\033[0m")
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
            return select_devices(devicesIds)


def get_devices(path):
    devices = read_devices(path)
    index = select_devices(devices)
    return devices[index]
