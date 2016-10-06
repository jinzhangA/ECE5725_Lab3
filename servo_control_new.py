import RPi.GPIO as GPIO
import time
from motor_control import pwm_motor

def GPIO27_callback(channel):
	print "Button 27 pressed, quit"
	motor.stop_motor()
	exit()


PWM_CHANNEL = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)

motor = pwm_motor(channel = PWM_CHANNEL)

# for speed in range(-10, 11):
# 	motor.change_speed(speed)
# 	motor.print_states()
# 	time.sleep(3)

motor.change_speed(0)
motor.print_states()
while 1:
	pass


# motor.stop_motor()