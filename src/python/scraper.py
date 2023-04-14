import os
import requests
import re
from bs4 import BeautifulSoup

# Define the folder path where the text files are located
folder_path = 'source files/'

# Loop through each text file in the folder
for file_name in os.listdir(folder_path):
    # Read the list of URLs from the current text file
    with open(folder_path + file_name, 'r') as f:
        urls = f.readlines()

    # Loop through the URLs and scrape the data
    with open('outputs ' + file_name, 'a', encoding='UTF-8') as output_file:
        for url in urls:
            page = requests.get(url.strip())
            soup = BeautifulSoup(page.content, 'html.parser')
            text = soup.get_text().strip()
            text = re.sub('\s+', ' ', text)
            text = re.sub('(.{140})', '\\1\n', text)
            output_file.write(text)
