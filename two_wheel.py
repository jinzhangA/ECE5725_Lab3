# Lab3 code
# Zhuo Chen zc292
# Rui Min rm977

import RPi.GPIO as GPIO
import time
from motor_control import pwm_motor
from wheel import Wheel

# define the key pressing functions
def GPIO17_callback(channel):
	print "Button 17 pressed, Left servo, forward"
	left_wheel.forward()

def GPIO22_callback(channel):
	print "Button 22 pressed, Left servo backward"
	left_wheel.backward()

def GPIO23_callback(channel):
	print "Button 23 pressed, Right servo, forward"
	right_wheel.forward()

def GPIO27_callback(channel):
	print "Button 27 pressed, Right servo backward"
	right_wheel.backward()

def GPIO16_callback(channel):
	print "Button 16 pressed, Left servo stopped"
	left_wheel.stop()

def GPIO12_callback(channel):
	print "Button 12 pressed, right servo stopped"
	right_wheel.stop()

# GPIO setups
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.add_event_detect(17, GPIO.FALLING, callback = GPIO17_callback, bouncetime = 300)
GPIO.add_event_detect(22, GPIO.FALLING, callback = GPIO22_callback, bouncetime = 300)
GPIO.add_event_detect(23, GPIO.FALLING, callback = GPIO23_callback, bouncetime = 300)
GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)
GPIO.add_event_detect(16, GPIO.FALLING, callback = GPIO16_callback, bouncetime = 300)
GPIO.add_event_detect(12, GPIO.FALLING, callback = GPIO12_callback, bouncetime = 300)


LEFT_CHANNEL = 13
RIGHT_CHANNEL = 19
left_wheel = Wheel('left', LEFT_CHANNEL)
right_wheel = Wheel('right', RIGHT_CHANNEL)


# all the buttons has been occupied. Instead of button 27, use the keypad to stop the
# program safely
while True:
	try:
		time.sleep(0.01)
	except KeyboardInterrupt:
		left_wheel.terminate()
		right_wheel.terminate()
		GPIO.cleanup()
		exit()


