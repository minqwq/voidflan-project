import os
import sys
import json

def getoeminfo(jsonfile):
    oem = json.load(open(jsonfile, "r", encoding="utf-8"))
    manufacturer = oem["manufacturer"]
    model = oem["model"]
    supportphone = oem["supportphone"]
    supporturl = oem["supporturl"]

    print(f"Manufacturer: {manufacturer}\n"+
          f"Model: {model}\n"+
          f"Support Phone: {supportphone}\n"+
          f"Support URL: {supporturl}")
