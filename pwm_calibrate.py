import RPi.GPIO as GPIO
import time
from motor_control import pwm_motor

# use button to exit the program
def GPIO27_callback(channel):
	print "Button 27 pressed, quit"
	motor.stop_motor()
	exit()


PWM_CHANNEL = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)

# setting up the motor
motor = pwm_motor(channel = PWM_CHANNEL)
motor.print_states()

# the motor should be initialed with speed of 0. However, set it to 0
while 1:
	time.sleep(1)