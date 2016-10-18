# Lab3 code
# Zhuo Chen zc292
# Rui Min rm977
import RPi.GPIO as GPIO
import time

CHANNEL = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL, GPIO.OUT)

# here the frequency has been changed to different value during the test
# frequency = 1
frequency = 500
p = GPIO.PWM(CHANNEL, frequency)
p.start(50)
time.sleep(100)
p.stop()
GPIO.cleanup()
