# Lab3 code
# Zhuo Chen zc292
# Rui Min rm977

import RPi.GPIO as GPIO
from time import sleep
from motor_control import pwm_motor
from wheel import Wheel

LEFT_CHANNEL = 13
RIGHT_CHANNEL = 19
GPIO.setmode(GPIO.BCM)
left_wheel = Wheel('left', LEFT_CHANNEL)
right_wheel = Wheel('right', RIGHT_CHANNEL)

# move forward
left_wheel.forward()
right_wheel.forward()
sleep(3)

# stopped
left_wheel.stop()
right_wheel.stop()
sleep(3)

# move backward
left_wheel.backward()
right_wheel.backward()
sleep(3)

# stopped
left_wheel.stop()
right_wheel.stop()
sleep(3)

# Pivot left
left_wheel.backward()
right_wheel.forward()
sleep(3)

# stopped
left_wheel.stop()
right_wheel.stop()
sleep(3)

# Pivot right
left_wheel.forward()
right_wheel.backward()
sleep(3)

# stopped
left_wheel.stop()
right_wheel.stop()

left_wheel.terminate()
right_wheel.terminate()
GPIO.cleanup()
