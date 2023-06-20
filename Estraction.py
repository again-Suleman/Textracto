import yake
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np  # Import the NumPy library

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()

# Prompt the user to select a file
file_path = filedialog.askopenfilename()

# Read the text from the selected file
with open(file_path, "r") as file:
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
print("Keywords extracted from the file:")
for i, keyword in enumerate(words):
    print(f"{i+1}. {keyword}")

