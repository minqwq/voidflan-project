import os
import time
import random

tstmem = 0
fun = random.randint(1, 10)
if fun == 1:
    print("113 Keyboard Error")
elif fun == 2:
    print("426 Memory Changed")
elif fun == 3:
    print("428 Memory Error")

while tstmem < 640:
    tstmem += 64
    print(str(tstmem) + " KB OK", end="\r")
    time.sleep(1)
time.sleep(2)
