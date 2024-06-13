import serial
import time
import keyboard

# CONFIG
jsUp = 'w'
jsDown = 's'
jsLeft = 'a'
jsRight = 'd'
dPadUp = 'i'
dPadDown = 'k'
dPadLeft = 'j'
dPadRight = 'l'
keyMode = 'hold' # 'hold' or 'ak47'
sensiThreshold = 255
# END CONFIG

# STATE
keysDown = {}
arduino = serial.Serial(
#	port = '/dev/ttyACM0',
	port = '/dev/ttyUSB0',
	baudrate = 115200,
	timeout = .1
)
# END STATE

def keyDown(key):
	if keyMode == 'ak47':
		keyboard.send(key)
#		print('[debug] key stroke', key)
	elif keyMode == 'hold':
		if key not in keysDown:
			keysDown[key] = True
			keyboard.press(key)
#			print('[debug] key down: ', key)


def keyUp(key):
	if key in keysDown:
		del(keysDown[key])
		keyboard.release(key)
#		print('[debug] key up: ', key)


def handleJoyStickInput(x, y):
	if x > 0:
		keyDown(jsRight)
		keyUp(jsLeft)
	elif x < 0:
		keyDown(jsLeft)
		keyUp(jsRight)
	else:
		keyUp(jsLeft)
		keyUp(jsRight)
	if y > 0:
		keyDown(jsUp)
		keyUp(jsDown)
	elif y < 0:
		keyDown(jsDown)
		keyUp(jsUp)
	else:
		keyUp(jsUp)
		keyUp(jsDown)


while True:
#	time.sleep(0.1)
	try:
		line = arduino.readline().strip().decode('utf-8')
	except:
		continue

#	print(len(line))
	if len(line) < 11: # 0,0,0,0,0,0
		continue

	splitted = line.split(',', 5)

#	print(len(splitted))
	if len(splitted) != 6:
		continue

# jak jestes w stanie przeczytac Keyes_SJoys to y,x to jest dobra orientacja xd
# w zasadzie to jednak na odwrut
	y = int(splitted[0])
	if abs(y) < sensiThreshold:
		y = 0
	x = int(splitted[1])
	if abs(x) < sensiThreshold:
		x = 0

	up = splitted[2]
	down = splitted[3]
	left = splitted[4]
	right = splitted[5]

	print(x, y, up, down, left, right)
#	handleJoyStickInput(x, y)

