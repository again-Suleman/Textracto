import random
from transformers import pipeline

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