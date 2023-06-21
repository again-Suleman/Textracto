# pip install googletrans==3.1.0a0
import googletrans

#print(googletrans.LANGUAGES)

from googletrans import Translator
translator = Translator()

# Read from a file
with open("Transcribed.txt", "r") as file:
    text = file.read()

result = translator.translate(text, src='en', dest='ur')

print(result.text)

