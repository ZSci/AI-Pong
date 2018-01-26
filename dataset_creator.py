import win32api as wapi
import win32con as wcon
import time

keyDict = {38:'up', 40:'dn'}
strokeList = list()

def checkKeyPress(key, t1):
	keySt = wapi.GetAsyncKeyState(key)
	if not keySt:
		return
	else:
		t2 = time.time()
		strokeList.append(str(t2-t1[0]) + ',' + 'nl')
		print(t2-t1[0], ',', 'nl')
		t1[0] = time.time()
		while keySt:
			keySt = wapi.GetAsyncKeyState(key)
		t2 = time.time()
		strokeList.append(str(t2-t1[0]) + ',' + keyDict[key])
		print(t2-t1[0], ',', keyDict[key])
		t1[0] = time.time()

t = [time.time()]

while True:
	checkKeyPress(wcon.VK_UP, t)
	checkKeyPress(wcon.VK_DOWN, t)
	if wapi.GetAsyncKeyState(wcon.VK_LEFT):
		print(strokeList)
		break

