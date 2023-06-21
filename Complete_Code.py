# Transcriber
import moviepy.editor
import speech_recognition as sr
from pydub import AudioSegment

# Translator
import googletrans
from googletrans import Translator

# Summariazation
import random
from transformers import pipeline

# Extraction
import yake
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np


# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Textracto")
root.geometry("500x400")

# Global variable for file path
file_path = ""

# Function to upload a file
def upload_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Select File")
    if file_path:
        messagebox.showinfo("File Uploaded", "File uploaded successfully!")
        transcribe_button.config(state="normal")
        translate_button.config(state="normal")
        extract_keywords_button.config(state="normal")
        summarize_button.config(state="normal")
        process_file(file_path)


# Function to process the uploaded file
def process_file(filepath):
    # Converting Video to mp3
    video = moviepy.editor.VideoFileClip(filepath)
    audio = video.audio
    audio.write_audiofile('sample.mp3')

    # Converting mp3 to wav
    sound = AudioSegment.from_mp3("sample.mp3")
    sound.export("transcript.wav", format="wav")
    print('Converted to .wav')



# Function to transcribe the audio
def transcribe_text():
    r = sr.Recognizer()
    with sr.AudioFile("transcript.wav") as source:
        # Adjust the energy threshold to ignore background noise
        r.energy_threshold = 4000 
        
        audio = r.record(source)  
        
    try:
        text = r.recognize_google(audio)
        print("\nTranscription:\n", text)
        with open("Transcribed.txt", "w") as file:
            file.write(str(text))
        file.close()
        messagebox.showinfo("Transcription Successful", "Audio transcribed successfully!")
        
    except sr.UnknownValueError:
        messagebox.showwarning("Transcription Error", "Could not transcribe the audio.")
        
    except sr.RequestError:
        messagebox.showerror("Transcription Error", "Failed to retrieve transcription results.")



def summarize_text():
    summarizer = pipeline('summarization')

    # Read from a file
    with open("Transcribed.txt", "r") as file:
        text = file.read()

    # Generating Formulas
    rdm_num = round(random.uniform(0.5, 0.65), 2)
    max_length = len(text.split()) * rdm_num

    summary = summarizer(text, max_length=80, min_length=30, do_sample=False)
    summary = (summary[0]['summary_text'])


    print(summary)


# Function to extract keywords and show histogram
def extract_keywords():
    # Read the text from the selected file
    with open("Transcribed.txt", "r") as file:
        text = file.read()

    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.9
    numOfKeywords = 20
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    # Extract the words and scores from the extracted keywords
    words = [kw[0] for kw in keywords]
    scores = [kw[1] for kw in keywords]

    # Generate colors for each bar
    colors = plt.cm.get_cmap('viridis', len(words))

    # Plotting the histogram
    fig, ax = plt.subplots()
    bars = ax.barh(words, scores, color=colors(np.arange(len(words))))

    # Set labels and title
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Keywords')
    ax.set_title('Keyword Frequencies')

    # Customize the layout
    plt.tight_layout()

    # Add a colorbar legend
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=min(scores), vmax=max(scores)))
    sm.set_array([])
    cbar = plt.colorbar(sm)

    # Show the plot
    plt.show()

    # Print the final result
    print("\nKeywords extracted from the file:")
    for i, keyword in enumerate(words):
        print(f"{i+1}. {keyword}")
        print('\n')
    


# Function to translate the transcribed text
def translate_text():
    with open("Transcribed.txt", "r") as file:
        text = file.read()
    
    translator = Translator()
    result = translator.translate(text, src='en', dest='ur')
    
    print("\nTranslation:\n", result.text)
    messagebox.showinfo("Translation Successful", "Text translated successfully!")
    

# Create buttons and labels
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=30)

transcribe_button = tk.Button(root, text="Transcribe", command=transcribe_text, state="disabled")
transcribe_button.pack(pady=10)

translate_button = tk.Button(root, text="Translate", command=translate_text, state="disabled")
translate_button.pack(pady=10)

extract_keywords_button = tk.Button(root, text="Extract Keywords", command=extract_keywords, state="disabled")
extract_keywords_button.pack(pady=10)

summarize_button = tk.Button(root, text="Summarize Text", command=summarize_text, state="disabled")
summarize_button.pack(pady=10)

root.mainloop()
