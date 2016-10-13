# Zhuo Chen zc292
# Rui Min rm977
# lab3
import pygame
import os
import RPi.GPIO as GPIO
import time
from wheel import Wheel

WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLACK = 0, 0, 0

# When debugging on the monitor, comment the following four lines
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_VIDEODRIVER','fbcon')

pygame.init()
# When debugging on the monitor, set set_visible() function to True
# pygame.mouse.set_visible(True)
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240))
my_font = pygame.font.Font(None, 50)
quit = ('quit', (160, 80))
resume = ('resume', (160, 80))
panic_stop_button = ('panic stop', (160, 30))
state_pos = (160, 120)
states = ["None", "None", "None"]

end_while = False

def GPIO17_callback(channel):
	# print "Button 17 pressed, Left servo, forward"
	left_wheel.forward()

def GPIO22_callback(channel):
	# print "Button 22 pressed, Left servo backward"
	left_wheel.backward()

def GPIO23_callback(channel):
	# print "Button 23 pressed, Left servo, forward"
	right_wheel.forward()

def GPIO27_callback(channel):
	# print "Button 27 pressed, Left servo backward"
	right_wheel.backward()

def GPIO16_callback(channel):
	# print "Button 16 pressed, Left servo stopped"
	left_wheel.stop()

def GPIO12_callback(channel):
	# print "Button 12 pressed, right servo stopped"
	right_wheel.stop()


LEFT_CHANNEL = 13
RIGHT_CHANNEL = 19

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

left_wheel = Wheel('left', LEFT_CHANNEL)
right_wheel = Wheel('right', RIGHT_CHANNEL)

left_cache = ('stop', 0)
right_cache = ('stop', 0)
stop = False

while not end_while:
	# Draw the quit button
	time.sleep(0.01)
	screen.fill(BLACK)                 

	if not stop: 
		text_surface = my_font.render(panic_stop_button[0], True, RED)
	else:
		text_surface = my_font.render(resume[0], True, GREEN)
	rect = text_surface.get_rect(center=panic_stop_button[1])
	screen.blit(text_surface, rect)

	quit_text = my_font.render(quit[0], True, WHITE)
	quit_rect = quit_text.get_rect(center=quit[1])
	screen.blit(quit_text, quit_rect)

	pygame.display.flip()

    # Detect touch event
	for event in pygame.event.get():
		if(event.type == pygame.MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			if y >= 50:
				end_while = True
			else:

				if not stop:
					left_cache = (left_wheel.state, left_wheel.speed)
					right_cache = (right_wheel.state, right_wheel.speed)
					left_wheel.stop()
					right_wheel.stop()
					stop = not stop

				else:
					if left_cache[0] == "forward":
						left_wheel.forward(left_cache[1])
					elif left_cache[0] == "backward":
						left_wheel.backward(left_cache[1])
					else:
						left_wheel.stop()

					if right_cache[0] == "forward":
						right_wheel.forward(right_cache[1])
					elif right_cache[0] == "backward":
						right_wheel.backward(right_cache[1])
					else:
						right_wheel.stop()
					stop = not stop

left_wheel.terminate()
right_wheel.terminate()
pygame.quit()

