import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
previous_27 = 0
GPIO.setup(24, GPIO.OUT)

def GPIO27_callback(channel):
    print "Button 27 pressed, quit"
    p.stop()
    GPIO.cleanup()
    exit()

GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)

channel = 24
frequency = 500

p = GPIO.PWM(channel, frequency)
p.start(99)
time.sleep(10)
p.stop()
GPIO.cleanup()
