import os
from googlesearch import search

def perform_search():
    file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'go', 'files', 'required_trends.txt')

    with open(file_path, 'r') as f:
        queries = f.read().splitlines()

    for query in queries:
        urls = []

        for result in search(query, num_results=10, lang='en'):
            urls.append(result)

        output_file_path = os.path.join('source files', f'{query.replace(" ", "_")}_urls.txt')

        with open(output_file_path, 'w', encoding="UTF-8") as file:
            for url in urls:
                file.write(url + '\n')

# Call the function to perform the search
#perform_search()
