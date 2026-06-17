#!/usr/bin/env python3
import re

def getBoardModelFromCpu(cpu_model):
    m = str(cpu_model).lower()

    # ===== Intel 老平台 =====
    if re.search(r"pentium 4|celeron", m):
        return "845 / 850 / 865 等 (Socket 478)"
    if re.search(r"pentium d", m):
        return "865 / 945 / 955 / 975 (LGA775)"
    if re.search(r"core 2 duo|core 2 quad|core 2 extreme", m):
        return "945 / 965 / P35 / P45 / G31 / G41 (LGA775)"
    if re.search(r"xeon 30[0-9]|xeon 31[0-9]|xeon 32[0-9]|xeon 33[0-9]", m):
        return "5000 / 5100 芯片组 (LGA771)"
    if re.search(r"xeon 51[0-9]|xeon 52[0-9]|xeon 53[0-9]|xeon 54[0-9]", m):
        return "5000 / 5400 芯片组 (LGA771)"

    # ===== Intel 主流平台 =====
    if re.search(r"i[3579]-1[234]\d{3}", m):
        return "H610 / B660 / B760 / Z690 / Z790 (LGA1700)"
    if re.search(r"i[3579]-1[01]\d{3}", m):
        return "H410 / B460 / B560 / Z490 / Z590 (LGA1200)"
    if re.search(r"i[3579]-[89]\d{3}", m):
        return "H310 / B360 / B365 / Z370 / Z390 (LGA1151 v2)"
    if re.search(r"i[3579]-[67]\d{3}", m):
        return "H110 / B150 / B250 / Z170 / Z270 (LGA1151 v1)"
    if re.search(r"i[3579]-[45]\d{3}|e3-12\d{2} v3", m):
        return "H81 / B85 / H97 / Z97 (LGA1150)"
    if re.search(r"i[3579]-[23]\d{3}|e3-12\d{2} v[12]", m):
        return "H61 / B75 / H77 / Z77 (LGA1155)"

    # ===== AMD FM 系列 =====
    if re.search(r"a[468]-3\d{3}", m):
        return "A55 / A75 (FM1)"
    if re.search(r"a[4610]-[0-4]\d{3}", m):
        return "A55 / A75 / A85X (FM2)"
    if re.search(r"a[4610]-[5678]\d{3}", m):
        return "A58 / A68H / A78 / A88X (FM2+)"

    # ===== AMD AM1 =====
    if re.search(r"athlon [2456][12468]0|sempron 2[456]0", m):
        return "AM1 SoC (A68N 等)"

    # ===== AMD AM3 / AM3+ =====
    if re.search(r"phenom ii|athlon ii", m):
        return "760G / 770 / 785G / 790X / 790FX (AM3)"
    if re.search(r"fx-\d{4}", m):
        return "970 / 990X / 990FX (AM3+)"

    # ===== AMD AM4 / AM5 =====
    if re.search(r"ryzen [3579] [1-5]\d{3}", m):
        return "A320 / B350 / B450 / X370 / X470 / B550 / X570 (AM4)"
    if re.search(r"ryzen [3579] [789]\d{3}|ryzen [3579] 1[012]\d{3}", m):
        return "A620 / B650 / B650E / X670 / X670E (AM5)"

    return "未知/未匹配"

if __name__ == "__main__":
    test_cpus = [
        # Intel 老平台
        "Intel(R) Pentium(R) 4 2.40GHz",
        "Intel(R) Pentium(R) D 805",
        "Intel(R) Core(TM)2 Duo CPU E4500",
        "Intel(R) Core(TM)2 Quad CPU Q6600",
        "Intel(R) Xeon(R) CPU 3040",
        "Intel(R) Xeon(R) CPU 5140",
        "Intel(R) Xeon(R) CPU 5410",

        # Intel LGA1155
        "Intel(R) Core(TM) i3-2120",
        "Intel(R) Core(TM) i5-3450",
        "Intel(R) Xeon(R) CPU E3-1230 V2",

        # Intel LGA1150
        "Intel(R) Core(TM) i3-4160",
        "Intel(R) Core(TM) i5-4590",
        "Intel(R) Xeon(R) CPU E3-1231 V3",

        # Intel LGA1151
        "Intel(R) Core(TM) i5-6500",
        "Intel(R) Core(TM) i7-7700K",
        "Intel(R) Core(TM) i5-8400",
        "Intel(R) Core(TM) i7-9700K",

        # Intel 新平台
        "Intel(R) Core(TM) i5-10400",
        "Intel(R) Core(TM) i7-11700",
        "Intel(R) Core(TM) i5-12400",
        "Intel(R) Core(TM) i9-14900K",

        # AMD FM 系列
        "AMD A4-5300",
        "AMD A8-3870K",
        "AMD A10-5800K",
        "AMD A10-7850K",
        "AMD A12-9800",

        # AMD AM1
        "AMD Athlon 5350",
        "AMD Sempron 2650",

        # AMD AM3 / AM3+
        "AMD Phenom II X4 955",
        "AMD Athlon II X2 250",
        "AMD FX-6300",
        "AMD FX-8350",

        # AMD AM4
        "AMD Ryzen 3 1200",
        "AMD Ryzen 5 2600",
        "AMD Ryzen 7 3700X",
        "AMD Ryzen 5 5600X",

        # AMD AM5
        "AMD Ryzen 5 7600",
        "AMD Ryzen 7 7800X3D",
        "AMD Ryzen 9 9950X",
    ]

    print("====== CPU 主板芯片组推测测试 ======\n")
    for cpu in test_cpus:
        result = getBoardModelFromCpu(cpu)
        print(f"{cpu:<40} => {result}")
