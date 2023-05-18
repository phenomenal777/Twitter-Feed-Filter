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
        data = f.read().splitlines()
    return render_template('data.html', data=data)

@app.route('/redirect_page/<item>')
def redirect_page(item):
    return f"data needs to be added"

if __name__ == '__main__':
    app.run(debug=True)
