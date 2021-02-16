import speech_recognition as sr
from keyboard import *

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:    
            print("Say that again please...")
            return "None"
    return query

def start():
	while True:
		query = takeCommand()
		if query != "none" and query != "None":

			write(query)

print("Welcome to Voice Type!")
print("Just speak into the microphone to start typing with your voice.")
start()