from flask import Flask, render_template

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
    return '<br>'.join(data)

if __name__ == '__main__':
    app.run(debug=True)
