from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()  # remove script and style tags

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

with open("files/#stayhome_urls.txt", 'r', encoding="UTF-8") as input_file:
    urls = input_file.readlines()

for url in urls:
    url = url.strip()  # remove leading/trailing whitespaces
    html = urllib.request.urlopen(url).read()
    text = text_from_html(html.decode('utf-8'))
    output_file_name = f"{url.split('/')[-1]}.txt"

    with open("outsputs.txt", 'w', encoding="UTF-8") as output_file:
        output_file.write(text)



