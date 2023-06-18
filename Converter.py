import moviepy.editor                   # pip install moviepy
from tkinter.filedialog import *
import speech_recognition as sr         # pip install SpeechRecognition 
from pydub import AudioSegment          # pip install pydub

# Convertnig Video to mp3
video = askopenfilename()
video = moviepy.editor.VideoFileClip(video)
audio = video.audio

audio.write_audiofile('sample.mp3')

# Converting mp3 to wav
sound = AudioSegment.from_mp3("sample.mp3")
sound.export("transcript.wav", format="wav")
print('Converted to .wav')

# Converting wav to text
r = sr.Recognizer()

with sr.AudioFile("transcript.wav") as source:
    audio1 = r.record(source)
    try:
        text = r.recognize_google(audio1)
        print("Working on it.....")
        
        # Throwing in a file        
        with open("Transcribed.txt", "w") as file:
            file.write(str(text))
        file.close()
        
        print(text)
    except:
        print('Sorry...Run again!')
        
        
