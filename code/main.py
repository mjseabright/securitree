import os
import threading
import queue
import time

NO_LIGHTS = 0
NORMAL_LIGHTS = 1
FAIL_LIGHTS = 2
SUCCSSS_LIGHTS = 3
CONFETTI_LIGHTS = 4

q = queue.Queue()

# Team 1
audioFiles = [
'',
'audio/intro.mp3',
'audio/seeThru.mp3',
'audio/vhs.mp3',
'audio/comet.mp3',
'audio/smell.mp3',
'audio/2Attempts.mp3',
'audio/1Attempt.mp3',
'',
'audio/lyrics.mp3',
'audio/motorbike.mp3'
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
['santa claus is coming to town', 'santaclaus is coming to town', 'santa is coming to town']
]

# Team 2
# audioFiles = [
# 'audio/intro.mp3',
# 'audio/braille.mp3',
# 'audio/cider.mp3',
# 'audio/comet.mp3',
# 'audio/puzzleBox.mp3',
# 'audio/2Attemps.mp3'
# 'audio/1Attempt.mp3'
# 'audio/selfDestruct.mp3',
# 'audio/lyrics.mp3',
# 'audio/motorbike.mp3'
# ]

# answers = [
# ['yes', 'y'],
# ['carols'],
# ['meosdr'],
# ['comet'],
# [],
# [],
# ['lie', 'lies'],
# ['santa claus is coming to town', 'santaclaus is coming to town', 'santa is coming to town']
# ]

def normalSuccess(level):
	print('Success')
	# Success lights
	# Success sound
	return level + 1

def normalFailure(level):
	print('Failure')
	# Failure lights
	# Failure sound
	return level

def incrementFailure(level):
	print('Increment Failure')
	# Failure lights
	# Failure sound
	return level + 1

def confettiFailure(level):
	print('Confetti failure')
	# Failure lights
	# Failure sound
	# Confetti lights
	os.system('mpg123 ' + 'audio/selfDestruct.mp3')
	# No lights
	# Activate motor
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
normalSuccess
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
normalFailure
]

def main():
	t = threading.Thread(target=lightController, args=(q,))
	q.put(NOAMAL_LIGHTS)
	t.start()
	level = 0
	# Normal lights
	while True:
		os.system('mpg123 ' + audioFiles[level])
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
	mode = 0
	while True:
		if not q.empty():
			mode = q.get_nowait()
			q.task_done()
			if mode == FAIL_LIGHTS:
				failLights()
				mode = NORMAL_LIGHTS
			else if mode == SUCCSSS_LIGHTS:
				sucessLights()
				mode = NORMAL_LIGHTS
		if mode == NORMAL_LIGHTS:
			normalLightsUpdate()
		if mode == CONFETTI_LIGHTS:
			confettiLightsUpdate()



def failLights():


def sucessLights():


if __name__ == '__main__':
	main()