import serial
import time
import keyboard

# CONFIG
jsUp = 'w'
jsDown = 's'
jsLeft = 'a'
jsRight = 'd'
rotateJoystick = False
dPadUp = 't'
dPadDown = 'g'
dPadLeft = 'f'
dPadRight = 'h'
keyMode = 'hold' # 'hold' or 'ak47'
sensiThreshold = 255
serialPort = '/dev/ttyUSB0' # /dev/ttyUSB1 in the other joystick
serialBaudrate = 115200
serialTimeout = .1
# END CONFIG

# STATE
keysDown = {}
arduinoSerial = serial.Serial()
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


def handleJoystickInput(x, y):
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


def handleButtonsInput(up, down, left, right):
	if up == 1:
		keyDown(dPadUp)
	else:
		keyUp(dPadUp)
	if down == 1:
		keyDown(dPadDown)
	else:
		keyUp(dPadDown)
	if left == 1:
		keyDown(dPadLeft)
	else:
		keyUp(dPadLeft)
	if right == 1:
		keyDown(dPadRight)
	else:
		keyUp(dPadRight)


arduinoSerial.port = serialPort
arduinoSerial.baudrate = serialBaudrate
arduinoSerial.timeout = serialTimeout


while True:
	if arduinoSerial.is_open:
		try:
			line = arduinoSerial.readline().strip().decode('utf-8')
		except:
			arduinoSerial.close()
			continue

		if len(line) < 11: # 0,0,0,0,0,0
			continue

		splitted = line.split(',', 5)

		if len(splitted) != 6:
			continue

		y = int(splitted[1])
		if abs(y) < sensiThreshold:
			y = 0

		x = int(splitted[0])
		if abs(x) < sensiThreshold:
			x = 0

		if rotateJoystick:
			x *= -1
			y *= -1

		up = int(splitted[2])
		down = int(splitted[3])
		left = int(splitted[4])
		right = int(splitted[5])

		handleButtonsInput(up, down, left, right)
		handleJoystickInput(x, y)
	else:
#		time.sleep(2)
#		print('closed ' + str(time.time()))
		try:
			arduinoSerial.open()
		except:
			continue


