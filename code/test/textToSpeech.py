from gtts import gTTS
import os

def main():
	filename = "smell.mp3"
	tts = gTTS(text='Music is a part of a good Christmas, it promotes joy and happiness. Why not hit the ivory and see if it works for you?', lang='en')
	tts.save(filename)
	os.system('mpg123 ' + filename)

if __name__ == '__main__':
	main()