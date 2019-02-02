import os
import threading
import queue
import time
import board
import neopixel
import numpy as np
import random
from gpiozero import LED

motor = LED(5)

NO_LIGHTS = 0
NORMAL_LIGHTS = 1
FAIL_LIGHTS = 2
SUCCSSS_LIGHTS = 3
CONFETTI_LIGHTS = 4

TWINKLE_RATE = 2

pixel_pin = board.D18
num_pixels = 25
layers = [7,6,5,4,3]
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER)

q = queue.Queue()

failSound = "code/audio/incorrect.mp3"
successSound = "code/audio/correct.mp3"

# Team 1
audioFiles = [
'',
'code/audio/intro.mp3',
'code/audio/seeThru.mp3',
'code/audio/vhs.mp3',
'code/audio/comet.mp3',
'code/audio/smell.mp3',
'code/audio/2Attempts.mp3',
'code/audio/1Attempt.mp3',
'',
'code/audio/lyrics.mp3',
'code/audio/motorbike.mp3'
]


answers = [
['securitree'],
['yes', 'y'],
['tinsel'],
['frosty', 'frosty the snowman', 'frostythesnowman', 'frosty the snow man'],
['comet'],
[],
[],
[],
['lie', 'lies'],
['santa claus is coming to town', 'santaclaus is coming to town', 'santa is coming to town'],
[]
]

# Team 2
# audioFiles = [
# '',
# 'code/audio/intro.mp3',
# 'code/audio/braille.mp3',
# 'code/audio/cider.mp3',
# 'code/audio/comet.mp3',
# 'code/audio/puzzleBox.mp3',
# 'code/audio/2Attempts.mp3',
# 'code/audio/1Attempt.mp3',
# '',
# 'code/audio/lyrics.mp3',
# 'code/audio/motorbike.mp3'
# ]


# answers = [
# ['securitree'],
# ['yes', 'y'],
# ['carols'],
# ['meosdr'],
# ['comet'],
# [],
# [],
# [],
# ['lie', 'lies'],
# ['santa claus is coming to town', 'santaclaus is coming to town', 'santa is coming to town'],
# []
# ]


def normalSuccess(level):
	print('Success')
	q.put(SUCCSSS_LIGHTS)
	os.system('mpg123 -b 200 -q ' + successSound)
	return level + 1


def noIncrementSuccess(level):
	# print('Success')
	# q.put(SUCCSSS_LIGHTS)
	# os.system('mpg123 -b 200 -q ' + successSound)
	return level


def normalFailure(level):
	print('Failure')
	q.put(FAIL_LIGHTS)
	os.system('mpg123 -b 200 -q ' + failSound)
	return level


def incrementFailure(level):
	print('Increment Failure')
	q.put(FAIL_LIGHTS)
	os.system('mpg123 -b 200 -q ' + failSound)
	return level + 1


def confettiFailure(level):
	print('Confetti failure')
	q.put(FAIL_LIGHTS)
	os.system('mpg123 -b 200 -q ' + failSound)
	q.put(CONFETTI_LIGHTS)
	os.system('mpg123 -b 200 -q ' + 'code/audio/selfDestruct.mp3')
	q.put(NO_LIGHTS)
	time.sleep(0.2)
	motor.on()
	time.sleep(1)
	motor.off()
	return level + 1


successFunction = [
normalSuccess,
normalSuccess,
normalSuccess,
normalSuccess,
normalSuccess,
None,
None,
None,
normalSuccess,
normalSuccess,
noIncrementSuccess
]

failureFunction = [
normalFailure,
normalFailure,
normalFailure,
normalFailure,
normalFailure,
incrementFailure,
incrementFailure,
confettiFailure,
normalFailure,
normalFailure,
normalFailure
]

def main():
	t = threading.Thread(target=lightController, args=(q,))
	q.put(NORMAL_LIGHTS)
	t.start()

	level = 0
	while True:
		os.system('mpg123 -b 200 -q ' + audioFiles[level])
		while True:
			response = input().lower()
			if response == '':
				break
			if response in answers[level]:
				level = successFunction[level](level)
				break
			else:
				oldLevel = level
				level = failureFunction[level](level)
				if level != oldLevel:
					break


def lightController(q):
	twinkle_state = np.zeros((num_pixels,3), dtype=np.int16)
	mode = NO_LIGHTS
	while True:
		if not q.empty():
			mode = q.get_nowait()
			q.task_done()
			if mode == FAIL_LIGHTS:
				failLights()
				mode = NORMAL_LIGHTS
			elif mode == SUCCSSS_LIGHTS:
				sucessLights()
				mode = NORMAL_LIGHTS
			elif mode == NO_LIGHTS:
				pixels.fill((0,0,0))
				pixels.show()
		if mode == NORMAL_LIGHTS:
			normalLightsUpdate(twinkle_state)
			pixels.show()
			time.sleep(0.002)

		if mode == CONFETTI_LIGHTS:
			confettiLightsUpdate(twinkle_state)

			pixels.show()
			time.sleep(0.002)


def normalLightsUpdate(twinkle_state):
	for pixel in range(num_pixels):
		if twinkle_state[pixel,0] == 0:
			if random.randint(0,50) == 3:
				twinkle_state[pixel,0] = TWINKLE_RATE
				twinkle_state[pixel,1] = random.randint(0,255)
				twinkle_state[pixel,2] = 1
				pixels[pixel] = hsv_to_rgb(twinkle_state[pixel,1], 255, twinkle_state[pixel,0])
		else:
			if twinkle_state[pixel,2] == 1:
				twinkle_state[pixel,0] += TWINKLE_RATE
				if twinkle_state[pixel,0] >= 200:
					twinkle_state[pixel,2] = 0
			else:
				twinkle_state[pixel,0] -= TWINKLE_RATE
				if twinkle_state[pixel,0] <= 0:
					twinkle_state[pixel,0] = 0
					twinkle_state[pixel,1] = 0
					twinkle_state[pixel,2] = 0
			pixels[pixel] = hsv_to_rgb(twinkle_state[pixel,1], 255, twinkle_state[pixel,0])


def confettiLightsUpdate(twinkle_state):
	for pixel in range(num_pixels):
		if twinkle_state[pixel,0] == 0:
			if random.randint(0,50) == 3:
				twinkle_state[pixel,0] = TWINKLE_RATE * 4
				twinkle_state[pixel,1] = 80
				twinkle_state[pixel,2] = 1
				pixels[pixel] = hsv_to_rgb(twinkle_state[pixel,1], 255, twinkle_state[pixel,0])
		else:
			if twinkle_state[pixel,2] == 1:
				twinkle_state[pixel,0] += TWINKLE_RATE * 4
				if twinkle_state[pixel,0] >= 200:
					twinkle_state[pixel,2] = 0
			else:
				twinkle_state[pixel,0] -= TWINKLE_RATE * 4
				if twinkle_state[pixel,0] <= 0:
					twinkle_state[pixel,0] = 0
					twinkle_state[pixel,1] = 0
					twinkle_state[pixel,2] = 0
			pixels[pixel] = hsv_to_rgb(twinkle_state[pixel,1], 255, twinkle_state[pixel,0])


def failLights():
	wait = 0.1
	for repeat in range(2):
		offset = num_pixels - 1
		for i in reversed(layers):
			pixels.fill((0,0,0))
			for led in range(i):
				pixels[offset - led] = (0,200,0)
			offset -= i
			pixels.show()
			time.sleep(wait)


def sucessLights():
	wait = 0.1
	for repeat in range(2):
		offset = 0
		for i in layers:
			pixels.fill((0,0,0))
			for led in range(i):
				pixels[offset + led] = (200,0,0)
			offset += i
			pixels.show()
			time.sleep(wait)


def wheel(pos):
	# Input a value 0 to 255 to get a color value.
	# The colours are a transition r - g - b - back to r.
	if pos < 0 or pos > 255:
		r = g = b = 0
	elif pos < 85:
		r = int(pos * 3)
		g = int(255 - pos*3)
		b = 0
	elif pos < 170:
		pos -= 85
		r = int(255 - pos*3)
		g = 0
		b = int(pos*3)
	else:
		pos -= 170
		r = 0
		g = int(pos*3)
		b = int(255 - pos*3)
	return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def hsv_to_rgb(h, s, v):
	h = h / 255.0
	s = s / 255.0
	v = v / 255.0
	i = int(h*6.) # XXX assume int() truncates!
	f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
	if s == 0.0: rgb = (v, v, v)
	elif i == 0: rgb = (v, t, p)
	elif i == 1: rgb = (q, v, p)
	elif i == 2: rgb = (p, v, t)
	elif i == 3: rgb = (p, q, v)
	elif i == 4: rgb = (t, p, v)
	elif i == 5: rgb = (v, p, q)
	out = [int(i * 255) for i in rgb]
	return (out[0], out[1], out[2])


if __name__ == '__main__':
	main()
