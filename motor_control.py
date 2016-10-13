import RPi.GPIO as GPIO
import time

class pwm_motor():
	def __init__(self, channel, 
				 center_pulse = 1.5, 
				 f_clkwise_pulse = 1.3, 
				 f_cclkwise_pulse = 1.7, 
				 base_pulse = 20, 
				 step_number = 10):

		
		self.channel = channel
		GPIO.setup(self.channel, GPIO.OUT)
		self.base_pulse = base_pulse
		self.center_pulse = center_pulse
		self.f_clkwise_pulse = f_clkwise_pulse
		self.f_cclkwise_pulse = f_cclkwise_pulse
		self.pulse_interval = (center_pulse - f_clkwise_pulse)/step_number
		self.current_stage = 0
		self.pulse = 0
		frequency, duty_cycle = self.get_frequency_dutycycle(self.current_stage)
		# print frequency, duty_cycle

		self.pwm = GPIO.PWM(self.channel, frequency)
		self.pwm.start(duty_cycle)

	def get_frequency_dutycycle(self, stage):
		self.pulse = self.center_pulse + stage*self.pulse_interval
		# print(self.pulse)
		period = self.base_pulse + self.pulse
		duty_cycle = 100 * self.pulse / period
		freq = 1000 / period
		# print pulse, freq, duty_cycle
		return freq, duty_cycle

	def change_speed(self, stage):
		if stage > 10 or stage < -10:
			print "Input stage %d, should be within [-10, 10]"%(stage)
		self.current_stage = stage
		frequency, duty_cycle = self.get_frequency_dutycycle(self.current_stage)
		self.pwm.ChangeDutyCycle(duty_cycle)
		self.pwm.ChangeFrequency(frequency)

	def stop_motor(self):
		self.change_speed(0)
		self.pwm.stop()
		time.sleep(0.1)
		GPIO.cleanup()

	def print_states(self):
		frequency, duty_cycle = self.get_frequency_dutycycle(self.current_stage)
		if self.current_stage == 0:
			stage = 'Stopped'
		elif self.current_stage > 0:
			stage = 'counterclockwise'
		else:
			stage = 'clockwise'
		print "current stage: %s %d, frequency: %.3f, duty cycle: %.3f, pulse: %.3f"\
		%(stage, abs(self.current_stage), frequency, duty_cycle, self.pulse)



if __name__ == '__main__':
	def GPIO27_callback(channel):
		print "Button 27 pressed, quit"
		motor.stop_motor()

	PWM_CHANNEL = 13
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(27, GPIO.FALLING, callback = GPIO27_callback, bouncetime = 300)

	motor = pwm_motor(channel = PWM_CHANNEL)
	motor.change_speed(0)
	# motor.print_states()
	time.sleep(100)
	# motor.change_speed(5)
	# motor.print_states()
	# time.sleep(5)
	# motor.stop_motor()




