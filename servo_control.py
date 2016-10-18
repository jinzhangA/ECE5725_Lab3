# Lab3 code
# Zhuo Chen zc292
# Rui Min rm977

import RPi.GPIO as GPIO
import time
from motor_control import pwm_motor

# use button 27 to terminate the program safely
def GPIO27_callback(channel):
	print "Button 27 pressed, quit"
	motor.stop_motor()
	exit()

PWM_CHANNEL = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)

motor = pwm_motor(channel = PWM_CHANNEL)

# speed change in stage [0, -10]
for speed in range(0, -11, -1):
	motor.change_speed(speed)
	motor.print_states()
	time.sleep(3)

# speed change in stage [0, 10]
for speed in range(0, 11):
	motor.change_speed(speed)
	motor.print_states()
	time.sleep(3)


motor.change_speed(0)
motor.print_states()
time.sleep(1)
motor.stop_motor()
