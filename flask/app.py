from flask import Flask, render_template, request
import os 
import pandas as pd

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

if __name__ == '__main__':
    app.run(debug=True)
