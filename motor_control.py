# Lab3 code
# Zhuo Chen zc292
# Rui Min rm977

import RPi.GPIO as GPIO
import time

class pwm_motor():
	def __init__(self, channel, 
				 center_pulse = 1.5, 
				 f_clkwise_pulse = 1.3, 
				 f_cclkwise_pulse = 1.7, 
				 base_pulse = 20, 
				 step_number = 10):

		# period = base_pulse + pulse
		# frequency = 1/period
		# duty cycle = pulse/period

		# As discribed on the datasheet, when pulse is 1.5ms, the motor
		# 	should stopped.
		# When pulse is 1.3, the motor should running clockwise at full speed.
		# When pulse is 1.7, the motor should running counter_clockwise at full speed.
		# At each direction, the speed is divided into 10 stages.
		# 	then the speed can be changed by adding intervals to the base pulse
		self.channel = channel
		GPIO.setup(self.channel, GPIO.OUT)
		self.base_pulse = base_pulse
		self.center_pulse = center_pulse
		self.f_clkwise_pulse = f_clkwise_pulse
		self.f_cclkwise_pulse = f_cclkwise_pulse
		self.pulse_interval = (center_pulse - f_clkwise_pulse)/step_number
		self.current_stage = 0
		self.pulse = 0

		# get the frequency and duty cycle for 0 speed
		frequency, duty_cycle = self.get_frequency_dutycycle(self.current_stage)

		# start the pwm with given paramenter.
		self.pwm = GPIO.PWM(self.channel, frequency)
		self.pwm.start(duty_cycle)

	def get_frequency_dutycycle(self, stage):
		# period = base_pulse + pulse
		# frequency = 1/period
		# duty cycle = pulse/period
		self.pulse = self.center_pulse + stage*self.pulse_interval
		period = self.base_pulse + self.pulse

		# Notice, the unit is 1ms, so using 1000 instead of 1
		duty_cycle = 100 * self.pulse / period
		freq = 1000 / period
		return freq, duty_cycle

	# the speed stage is defined as 21 stages
	# the [1, 10] is defined as counter-clockwise
	# the [-1, -10] is defined as clockwise
	# 0 is stop
	def change_speed(self, stage):
		# if wrong stage is assigned, change is to 0 for safty.
		if stage > 10 or stage < -10:
			print "Input stage %d, should be within [-10, 10]"%(stage)
			stage = 0
		self.current_stage = stage
		frequency, duty_cycle = self.get_frequency_dutycycle(self.current_stage)
		self.pwm.ChangeDutyCycle(duty_cycle)
		self.pwm.ChangeFrequency(frequency)

	def stop_motor(self):
		# stop the motor safely and clean the GPIO
		self.change_speed(0)
		self.pwm.stop()
		# GPIO.cleanup()

	def print_states(self):
		# debug tools, to display all the important info
		frequency, duty_cycle = self.get_frequency_dutycycle(self.current_stage)
		if self.current_stage == 0:
			stage = 'Stopped'
		elif self.current_stage > 0:
			stage = 'counterclockwise'
		else:
			stage = 'clockwise'
		print "current stage: %s %d, frequency: %.3f, duty cycle: %.3f, pulse: %.3f"\
		%(stage, abs(self.current_stage), frequency, duty_cycle, self.pulse)
