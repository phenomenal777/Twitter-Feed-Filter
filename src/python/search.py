from googlesearch import search

with open('../../go/files/required_trends.txt', 'r') as f:
    queries = f.read().splitlines()

for query in queries:
    
    urls = []
    counter = 0
   
    for result in search(query, num_results=10, lang='en'):
        urls.append(result)

    with open('source files/{}_urls.txt'.format(query.replace(" ", "_")), 'w', encoding = "UTF-8") as file:
        for url in urls:
            file.write(url + '\n')
        file.close()

