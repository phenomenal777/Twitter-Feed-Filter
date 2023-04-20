import os
import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
from prettytable import PrettyTable
import nltk
from nltk.corpus import stopwords

# Define the folder path where the text files are located
folder_path = 'source files/'

# Define the number of links to scrape from each file
num_links = 10

# Load the NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Loop through each text file in the folder
for file_name in os.listdir(folder_path):
    # Read the list of URLs from the current text file
    with open(folder_path + file_name, 'r') as f:
        urls = f.readlines()[:num_links]

    # Loop through the URLs and scrape the data
    word_counter = Counter()
    with open('raw data/outputs ' + file_name, 'a', encoding='UTF-8') as output_file:
        for url in urls:
            # For limiting redirects
            page = requests.get(url.strip(), allow_redirects=False)
            soup = BeautifulSoup(page.content, 'html.parser')
            text = soup.get_text().strip()
            text = re.sub('\s+', ' ', text)
            output_file.write(text)

            # Remove stopwords from the text
            words = re.findall('\w+', text)
            words = [w for w in words if not w.lower() in stop_words]

            # Count the frequency of each word in the text
            word_counter.update(words)

            # Decrement num_links variable and break out of the loop if it reaches the limit
            num_links -= 1
            if num_links == 0:
                break

    # Create a table to display the word frequency
    table = PrettyTable()
    table.field_names = ['Word', 'Frequency']
    for word, count in word_counter.items():
        table.add_row([word, count])

    # Write the word frequency table to a separate file
    with open('data/frequency ' + file_name, 'w', encoding='UTF-8') as freq_file:
        freq_file.write(str(table))
