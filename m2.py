import subprocess
import speech_recognition as speech
import telebot
import os
import requests

token = "2121965523:AAGC8Wep-94MqaRGOqYjWvVu3RZkUQNXQaY"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Пришли любое голосовое сообщение")

@bot.message_handler(content_types=["voice"])
def get_audio(message):
	print(dir(message))
	f = bot.get_file(message.voice.file_id)
	path = f.file_path

	fname = os.path.basename(path)

	doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, path))

	with open(fname+".oga", "wb") as f:
		f.write(doc.content)

	process = subprocess.run(["ffmpeg", "-i", fname+".oga", fname+".wav"])

	res = audio_to_text(fname+".wav")
	bot.send_message(message.chat.id, res)

def audio_to_text(name):
	sample_audio = speech.AudioFile("rec.wav")
	recog = speech.Recognizer()
	with sample_audio as audio_file:
		audio_content = recog.record(audio_file)

	return recog.recognize_google(audio_content)

bot.polling()

