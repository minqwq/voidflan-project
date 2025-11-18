import os
import sys
import time
import random

tstmem = 0
while tstmem < random.randint(1024128, 1024576):
    tstmem += 512
    print(str(tstmem) + " KB Pass...", end="\r")
    time.sleep(0.005)
time.sleep(1)
print("SGI Indigo Series is now starting up your Operating System...")
time.sleep(3)
