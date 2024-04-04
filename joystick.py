import serial
import time
import keyboard

# CONFIG
jsUp = 'w'
jsDown = 's'
jsLeft = 'a'
jsRight = 'd'
keyMode = 'hold' # 'hold' or 'ak47'
sensiThreshold = 255
# END CONFIG

# STATE
keysDown = {}
arduino = serial.Serial(
	port = '/dev/ttyACM0',
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
	line = arduino.readline().strip().decode('utf-8')
	if len(line) < 1:
		continue
	splitted = line.split(',', 1)
	if len(splitted) != 2:
		continue

# jak jestes w stanie przeczytac Keyes_SJoys to y,x to jest dobra orientacja xd
	y = int(splitted[0])
	if abs(y) < sensiThreshold:
		y = 0
	x = int(splitted[1])
	if abs(x) < sensiThreshold:
		x = 0

#	print(x, y)
	handleJoyStickInput(x, y)

