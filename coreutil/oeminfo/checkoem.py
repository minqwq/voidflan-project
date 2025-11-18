import os
import sys
import json

oemjson_pre = open(os.path.dirname(os.path.abspath(__file__)) + "/oeminfo.json", "r", encoding="utf-8")
oemjson = json.load(oemjson_pre)
abspath = os.path.dirname(os.path.abspath(__file__))

model = oemjson["model"]

print("ABSPATH=" + abspath)
if model.startswith("SpracServer"):
    os.system(sys.executable + " " + abspath + "/oembootscrs/spracsrv.py")
elif model == "IBM PC" or model == "IBM XT":
    os.system(sys.executable + " " + abspath + "/oembootscrs/ibmpc.py")
elif model.startswith("SGI Indigo"):
    os.system(sys.executable + " " + abspath + "/oembootscrs/sgiindigo.py")
