import speech_recognition as speech
import telebot
import os
import requests
import subprocess
# from pydub import AudioSegment
# s = os.sep
# AudioSegment.converter = f"{os.getcwd()}{s}FFmpeg{s}bin{s}ffmpeg.exe"
# AudioSegment.ffmpeg = f"{os.getcwd()}{s}ffmpeg{s}bin{s}ffmpeg.exe"
# AudioSegment.ffprobe = f"{os.getcwd()}{s}ffmpeg{s}bin{s}ffprobe.exe"


token = "2121965523:AAGC8Wep-94MqaRGOqYjWvVu3RZkUQNXQaY"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Пришли любое голосовое сообщение")

@bot.message_handler(content_types=["voice"])
def get_audio(message):
	f = bot.get_file(message.voice.file_id)
	path = f.file_path

	fname = os.path.basename(path)

	doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, path))
	fname = fname[:-4]
	with open(fname + ".ogg", "wb") as f:
		f.write(doc.content)

	
	# AudioSegment.from_ogg(fname + ".ogg").export(fname + ".wav", format="wav")
	subprocess.run(["ffmpeg", "-i", fname+".ogg", fname+".wav"])

	res = audio_to_text(fname+".wav")
	os.remove(fname + ".ogg")
	os.remove(fname + ".wav")
	bot.send_message(message.chat.id, res)
	

def audio_to_text(name):
	sample_audio = speech.AudioFile(name)
	recog = speech.Recognizer()
	
	with sample_audio as audio_file:
		audio_content = recog.record(audio_file)

	return recog.recognize_google(audio_content) #, language="ru-RU")

bot.polling()

