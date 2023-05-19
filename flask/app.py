from flask import Flask, render_template, request
import pandas as pd
import sys
import os
sys.path.append("..")
from src.python.search import perform_search
from src.python.scraper import scraper

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
    return render_template('tweets.html', headers=headers, rows=rows)

def exec_search():
    script_path = os.path.abspath(__file__) # Gives us the absolute path to the file
    script_dir = os.path.dirname(script_path) # Gives us the directory in this path
    source_files_dir = os.path.join(script_dir, 'source files') # construct the path to source files directory
    os.makedirs(source_files_dir, exist_ok=True) # create it if it doesn't exist
    perform_search()

if __name__ == '__main__':
    app.run(debug=True)
