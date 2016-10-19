# Zhuo Chen zc292
# Rui Min rm977
# lab3
import pygame
import os
import RPi.GPIO as GPIO
import time
from wheel import Wheel
from collections import deque

WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLACK = 0, 0, 0

# When debugging on the monitor, comment the following four lines
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_VIDEODRIVER','fbcon')

# pygame setuo
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240))
my_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 20)

# buttons
quit = ('quit', (160, 80))
resume = ('resume', (160, 80))
panic_stop_button = ('panic stop', (160, 30))

# this is the position of the states printing
left_state_pos = (80, 140)
right_state_pos = (240, 140)

end_while = False

# initialize the history queue. Length should be 4, the last element will
# 	be adding with the initial motor state
left_history = deque([None]*3)
right_history = deque([None]*3)

# define the button pressing functions
# here, every the motor state changes, the history should be updated.
# the least recent one will be popped out.
def GPIO17_callback(channel):
	left_wheel.forward()
	left_history.appendleft(left_wheel.get_state())
	left_history.pop()


def GPIO22_callback(channel):
	left_wheel.backward()
	left_history.appendleft(left_wheel.get_state())
	left_history.pop()


def GPIO23_callback(channel):
	right_wheel.forward()
	right_history.appendleft(right_wheel.get_state())
	right_history.pop()

def GPIO27_callback(channel):
	right_wheel.backward()
	right_history.appendleft(right_wheel.get_state())
	right_history.pop()

def GPIO16_callback(channel):
	left_wheel.stop()
	left_history.appendleft(left_wheel.get_state())
	left_history.pop()

def GPIO12_callback(channel):
	right_wheel.stop()
	right_history.appendleft(right_wheel.get_state())
	right_history.pop()

# GPIO setups
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

# initialize two wheels and add the state to the history
left_wheel = Wheel('left', LEFT_CHANNEL)
left_history.appendleft(left_wheel.get_state())

right_wheel = Wheel('right', RIGHT_CHANNEL)
right_history.appendleft(right_wheel.get_state())

# When resuming from panic stop, the previous state should be resumes.
# 	This is the cache to store the states
left_cache = ('stop', 0)
right_cache = ('stop', 0)

# this is a flag for the panic stop
stop = False

while not end_while:
	time.sleep(0.01)
	# clean the screen
	screen.fill(BLACK)   

	# if not panic stopped: display the 'panic stop' button
	# else, display the 'resume' button              
	if not stop: 
		text_surface = my_font.render(panic_stop_button[0], True, RED)
	else:
		text_surface = my_font.render(resume[0], True, GREEN)
	# Same position of the potential two buttons
	rect = text_surface.get_rect(center=panic_stop_button[1])
	screen.blit(text_surface, rect)

	# render the quit button
	quit_text = my_font.render(quit[0], True, WHITE)
	quit_rect = quit_text.get_rect(center=quit[1])
	screen.blit(quit_text, quit_rect)

	# print left wheel history
	left_offset = 0
	for state in list(left_history):
		# as the history was initialized with Nones, print only not none
		if state:
			text_surface = small_font.render(state, True, WHITE)
			rect = text_surface.get_rect(center=(left_state_pos[0], left_state_pos[1]+left_offset))
			# move to next line
			left_offset += 10
			screen.blit(text_surface, rect)

	right_offset = 0
	for state in list(right_history):
		if state:
			text_surface = small_font.render(state, True, WHITE)
			rect = text_surface.get_rect(center=(right_state_pos[0], right_state_pos[1]+right_offset))
			right_offset += 10
			screen.blit(text_surface, rect)

	pygame.display.flip()

    # Detect touch event
	for event in pygame.event.get():
		if(event.type == pygame.MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			if y >= 50 and y <= 90:
				end_while = True
			elif y < 50:
				# prepare to panic stop if not stopped.
				if not stop:
					# if the panic stop is pressed.
					# cache all the states then stop the wheels
					left_cache = (left_wheel.state, left_wheel.speed)
					right_cache = (right_wheel.state, right_wheel.speed)
					left_wheel.stop()
					right_wheel.stop()
					stop = not stop

				else:
					# if resume pressed,
					# resume the states of the wheels with cache
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

				# either panic stop or resume press, the state will change
				# record it.
				left_history.appendleft(left_wheel.get_state())
				left_history.pop()
				right_history.appendleft(right_wheel.get_state())
				right_history.pop()
# cleanout and quit.
left_wheel.terminate()
right_wheel.terminate()
GPIO.cleanup()
pygame.quit()

