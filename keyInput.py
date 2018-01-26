import sys
print(sys.version)

import pyautogui as pg
from time import sleep

for i in range(5)[::-1]:
	print(i)
	sleep(1)

pg.FAILSAFE = True

try:
	while True:
		pg.keyDown('up')
		sleep(0.5)
		pg.keyUp('up')
		sleep(0.5)
		pg.keyDown('down')
		sleep(0.5)
		pg.keyUp('down')

finally:
	pg.FAILSAFE = False
	pg.keyUp('up')
	pg.keyUp('down')