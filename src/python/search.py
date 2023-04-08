import requests
from bs4 import BeautifulSoup

# Read query strings from text file
with open('../../go/files/required_trends.txt', 'r') as f:
    queries = f.read().splitlines()

for query in queries:
    url = "https://www.google.com/search?q=" + query

    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    counter = 0

    for link in soup.find_all('a'):
        url = link.get('href')
        urls.append("https://" + url[7:])
        counter += 1
        if counter >= 10:
            break
    
    with open('files/{}_urls.txt'.format(query.replace(" ", "_")), 'w', encoding = "UTF-8") as file:
        for url in urls:
            file.write(url + '\n')
        file.close()




