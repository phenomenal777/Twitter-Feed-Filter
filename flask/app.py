from flask import Flask, render_template, request
import pandas as pd
import sys

sys.path.append("..")
from src.python.search import perform_search
from src.python.scraper import scraper
from src.python.embeddings import embeddings

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return 'templates/bird.png', 404

@app.route('/data')
def get_data():
    with open('../go/files/required_trends.txt', 'r') as f:
        data = [line.replace('#', '') for line in f.read().splitlines()]
    return render_template('data.html', data=data)

@app.route('/tweets/<item>')
def get_tweets(item):
    filepath = f'../go/files/{item}_tweets.csv'
    df = pd.read_csv(filepath)
    headers = df.columns.tolist()
    rows = df.values.tolist()
    return render_template('tweets.html', headers=headers, rows=rows, item=item)

@app.route('/test')
def exec_search():
    perform_search()
    scraper()
    embeddings()
    return "200: OK"

@app.route('/results/<item>')
def get_results(item):
    filepath = f'answers/answer_{item}.csv'
    df = pd.read_csv(filepath)
    headers = df.columns.tolist()
    rows = df.values.tolist()
    return render_template('results.html', headers=headers, rows=rows, item=item)

if __name__ == '__main__':
    app.run(debug=True)
