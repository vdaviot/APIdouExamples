
import os, time, pygame, pyglet

global volume = 50

def get_bpm(touched):
	count = 0
	bpm = record(touched, count)
	print "BPM:{}".format(bpm)
	return translate_bpm(bpm)

def	record(self, touched, count):
	t = os.timestamp()
	status = True
	while status == True:
		t2 = os.timestamp()
		if touched:
			count += 1
		if t2 >= t + 2:
			status = False
	return count

def	translate_bpm():
	bpm = count * 30


def	action(what, bpm):
	if what == RIGHT_EAR:
		set_volume(1)
	elif what == LEFT_EAR:
		set_volume(0)
	elif what == RIGHT_HAND:
		switch_track(1)
	elif what == LEFT_HAND:
		switch_track(0)
	elif what == ANTENNA:
		play_track(0)
	if bpm:
		index = find_song(bpm)
		play_track(index)

def	play_track(nb):
	pygame.music.play(file_list[nb])

def switch_track(bool):
	if bool == 1:
		pygame.music.load(file_list[number + 1])
		play_track(number + 1)
	else:
		pygame.music.load(file_list[number - 1])
		play_track(number - 1)

def	set_volume(bool):
	valid = False
	if bool == 1:
		volume += 5
	else:
		volume -= 5
	while not valid:
	    try:
	        if (volume <= 100) and (volume >= 0):
	            call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])
	            valid = True
	    except ValueError:
	        pass

#/home/shayn/Work/APIdouExamples

def	init_music():
	global file_list = {}
	pygame.init()
	folder = os.walk("/home/shayn/Work/APIdouExamples/music")
	for track in folder:
		file_list.append(track)
		print track

def	do_all_the_shit(touch):
	# init_music()
	# while True:
	bpm = get_bpm
	action(touch, bpm)


