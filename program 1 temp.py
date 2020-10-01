#!/usr/bin/python3
import gpiozero		#gpio module
import math, sys, os, time
import subprocess
import socket

pin_rotaryenable = 26	# yellow
pin_countrotary = 19		# red
pin_hook = 16
button_hook = 12

rotaryenable = gpiozero.Button(pin_rotaryenable)
countrotary = gpiozero.Button(pin_countrotary)
hook = gpiozero.Button(pin_hook)
button = gpiozero.Button(button_hook)

class Dial():
	def __init__(self):
		print("Initializing...")
		self.pulses = 0
		self.number = ""
		self.counting = True
		self.calling = False

	def startcalling(self):
		print("Start calling")
		self.reset()
		self.calling = True
		self.player = subprocess.Popen(["mpg123", "--loop", "20", "-q", "dial.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	def stopcalling(self):
		print("Stop calling")
		self.calling = False
		self.reset()

	def startcounting(self):
		print ("Start counting")
		self.counting = self.calling

	def stopcounting(self):
		print("Stop counting")
		if self.calling:
			print ("Got %s pulses.." % self.pulses)
			if self.pulses > 0:
				if math.floor(self.pulses / 2) == 10:
					self.number += "0"
				else:
					short_num = str(math.floor(self.pulses/2))
					self.number += short_num
			print("Than %s is dialed!" % self.number)
			self.pulses = 0
		self.counting = False

	def addpulse(self):
		print("Add pulse")
		if self.counting:
			print("real addpulse")
			self.pulses += 1

	def getnumber(self):
		return self.number

	def counterreset(self):
		print("Reset counter")
		self.pulses = 0
		self.number = ""
		
	def reset(self):
		print("Reset all")
		self.counterreset()
		try:
			self.player.kill()
		except:
			pass


if __name__ == "__main__":
	dial = Dial()
	countrotary.when_deactivated = dial.addpulse
	countrotary.when_activated = dial.addpulse
	rotaryenable.when_activated = dial.startcounting
	rotaryenable.when_deactivated = dial.stopcounting
	hook.when_activated = dial.stopcalling
	hook.when_deactivated = dial.startcalling
	while True:
		time.sleep(1)
