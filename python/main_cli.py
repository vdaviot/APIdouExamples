import logging
import sys
import time
import argparse
from subprocess import call
from test import *
from apidou import *
from pdsend import *
from comsend import *
import pygatt.backends
import os, time, pygame, pyglet
from multiprocessing import Pool

compt = 0
start_time = 0
apidou = ''
volume = 50
number = 0
file_list = []



# def get_bpm(touched):
# 	count = 0
# 	count = record(touched, count)
# 	# print "BPM:{}".format(bpm)
# 	return translate_bpm(count)

# def	record(touched, count):
# 	t = time.time()
# 	status = True
# 	while status == True:
# 		t2 = time.time()
# 		if touched:
# 			count += 1
# 		if t2 >= t + 2:
# 			status = False
# 	return count

# def	translate_bpm(count):
# 	bpm = count * 30
# 	return bpm

def	action(what, number, volume):
	if what == apidou.LEFT_EAR:
		set_volume(volume, 1)
	elif what == apidou.RIGHT_EAR:
		set_volume(volume, 0)
	elif what == apidou.RIGHT_HAND:
		switch_track(1, number)
	elif what == apidou.LEFT_HAND:
		if number > 0:
			number -= 1
		switch_track(0, number)
	elif what == apidou.ANTENNA:
		play_track(number)
	# if bpm:
		# index = find_song(bpm)
		# play_track(index)

def	play_track(nb):
	pygame.mixer.music.load(file_list[nb])
	pygame.mixer.music.play(1)

def switch_track(bool, number):
	if bool == 1:
		if file_list[number]:
			pygame.mixer.music.load(file_list[number])
			play_track(number)
	else:
		if number > 0:
			if file_list[number]:
				pygame.mixer.music.load(file_list[number])
				play_track(number)

def	set_volume(volume, bool):
	valid = False
	print volume
	if bool == 1:
		volume = volume +  5
	elif bool == 0:
		volume -= 5
	while not valid:
	    try:
	        if (volume <= 100) and (volume >= 0):
	            call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
	            valid = True
	    except ValueError:
	        pass

def	init_music():
	pygame.init()
	pygame.mixer.init()
	folder = os.listdir("/home/shayn/Work/APIdouExamples/music")
	for track in folder:
		file_list.append(track)
		print track

def	do_all_the_shit(touch):
	# init_music()
	# while True:x`z
	# bpm = get_bpm(apidou.touch)
	bpm = 0
	action(touch, number, volume)


def APIdouCallback(handle, value):
	global apidou

	if handle == apidou.accel_handle:
		accel = struct.unpack("hhh", value)
		print "ACCEL", accel
	elif handle == apidou.gyro_handle:
		gyro = struct.unpack("hhh", value)
		print "GYRO", gyro
	elif handle == apidou.touch_handle:
		touch = struct.unpack("B", value)
		print "TOUCH", touch[0]

def handleMessage(device, message):
	if message == "1":
		device.setVibration(True)
		print "Vibration On"
	elif message == "0":
		device.setVibration(False)
		print "Vibration Off"
	else:
		print "Received an unknown message on socket"

def handleOutput(device, output, is_tcp):
	if is_tcp == True:
		# TODO : Implement a way to check which notification
		# is enabled and only send these ones
		output.send_packet(1, device.accel)
		output.send_packet(2, device.gyro)
		output.send_packet(3, {device.touch})
	else:
		output.send_packet(device)

	tmp = output.get_message()
	if tmp != "":
			handleMessage(device, tmp)

def main():
	global apidou

	logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

	parser = argparse.ArgumentParser()
	parser.add_argument('-type', '-t', required=True, choices=['bled112', 'linux'] ,\
		help='Are you using a BLED112 or regular BLE Adapter on Linux ?')
	parser.add_argument('-addr', '-a', required=True, \
		help='MAC address of your APIdou, e.g. 00:07:80:02:F2:F2')
	# To implement
	parser.add_argument('-tcp', required=False, \
		help='Activate a forward to TCP (port 3000)', action='store_true')
	parser.add_argument('-com', required=False, \
		help='Activate a forward to a COM port', action='store_true') 
	args = parser.parse_args()

	if args.tcp:
		output = PdSend()
	elif args.com:
		output = COMSend()

	try:
		apidou = APIdou(args.type, args.addr)
		apidou.connect()

		apidou.setNotifyAccel(True)
		# apidou.setNotifyGyro(True)
		apidou.setNotifyTouch(True)
		print "Connected"
		init_music()
		while True:
			if apidou.isTouched(APIdou.ANTENNA):
				print "The antenna is touched"
			# print "Accel: ", apidou.accel
			# print "Gyro: ", apidou.gyro
			do_all_the_shit(apidou.touch)
			print "touch: ", apidou.touch
			if args.tcp or args.com:
				handleOutput(apidou, output, args.tcp)
			time.sleep(0.01)

	except pygatt.exceptions.NotConnectedError:
		print "Could not connect. Check if device is on (program will exit)"
	except KeyboardInterrupt:
		print "\nCtrl-C pressed. Goodbye!"
	finally:
		apidou.disconnect()
		if args.tcp or args.com:
			output.close()

if __name__ == '__main__':
	main()

