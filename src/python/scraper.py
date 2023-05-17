import os
import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
import unicodedata
import time

# Define the folder path where the text files are located
folder_path = 'source files/'

# Load the NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Define the regex pattern to match ASCII letters excluding non-ASCII characters
ascii_pattern = re.compile(r'[\x00-\x7F]+')

# Loop through each text file in the folder
for file_name in os.listdir(folder_path):
    # Check if the path is a file and continue only if it is
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
        continue

    # Read the list of URLs from the current text file
    num_links = 10
    with open(file_path, 'r') as f:
        urls = f.readlines()[:num_links]

    # Loop through the URLs and scrape the data
    word_counter = Counter()
    with open('data/' + "data" + file_name, 'a', encoding='UTF-8') as output_file:
        for url in urls:
            try:
        # For limiting redirects and setting a timeout of 7 seconds
                page = requests.get(url.strip(), allow_redirects=False, timeout=7)
                soup = BeautifulSoup(page.content, 'html.parser')
                text = soup.get_text().strip()

        # Remove non-ASCII characters from the text
                text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

                text = re.sub('\s+', ' ', text)
                output_file.write(text)

            # Remove stopwords and non-ASCII words from the text
                words = ascii_pattern.findall(text)
                words = [w for w in words if not w.lower() in stop_words]

            # Count the frequency of each word in the text
                word_counter.update(words)

            except requests.exceptions.Timeout:
                continue

            except requests.exceptions.ConnectionError as e:
            #print(f"Connection error occurred: {e}")
        # Wait for 5 seconds before retrying the connection
                time.sleep(5)
                continue

    # Decrement num_links variable and break out of the loop if it reaches the limit
            num_links -= 1
            if num_links == 0:
                break

