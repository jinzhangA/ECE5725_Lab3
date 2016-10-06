import RPi.GPIO as GPIO
import time
from motor_control import pwm_motor

def GPIO27_callback(channel):
	print "Button 27 pressed, quit"
	left_wheel.terminate()
	right_wheel.terminate()

	exit()

class Wheel():
	def __init__ (self, left_right, channel):
		if left_right == 'left':
			self.left_right = 'left'
		else:
			self.left_right = 'right'

		self.channel = channel
		self.motor = pwm_motor(channel = self.channel)

	def forward(self, speed = 5):
		if self.left_right == 'left':
			self.motor.change_speed(speed)
		else:
			self.motor.change_speed(-speed)

	def backward(self, speed = 5):
		if self.left_right == 'left':
			self.motor.change_speed(-speed)
		else:
			self.motor.change_speed(speed)

	def stop(self):
		self.motor.change_speed(0)

	def terminate(self):
		self.motor.stop_motor()





LEFT_CHANNEL = 21
RIGHT_CHANNEL = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)

left_wheel = Wheel('left', LEFT_CHANNEL)
right_wheel = Wheel('right', RIGHT_CHANNEL)

# left_wheel.forward()
# right_wheel.forward()
# time.sleep(5)

# left_wheel.backward()
# right_wheel.backward()
# time.sleep(5)

left_wheel.stop()
right_wheel.stop()
# time.sleep(5)

# left_wheel.terminate()
# right_wheel.terminate()


