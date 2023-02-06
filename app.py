"""
A simple Flask application that communicates with the OpenAI API and stores
the generated text in a SQLite database.
"""

import sqlite3
from flask import Flask, request, render_template, redirect
import requests


app = Flask(__name__)

# API endpoint and headers
API_URL = 'https://api.openai.com/v1/models/text-davinci-003'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <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>'
}

@app.route('/')
def index():
    """
    The main page of the digital notebook.
    """
    # Connect to the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Query the data from the database
    cursor.execute('SELECT * FROM data')
    data = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    # Render the data in the template
    return render_template('index.html', data=data)

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("localhost", 3000, app, use_reloader=True)

@app.route('/send_request', methods=['GET', 'POST'])
def send_request():
    """
    Sends a request to the OpenAI API and stores the generated text in the database.
    :param text: The text to be sent to the OpenAI API
    :return: A redirect to the index page
    """
    # Get the text to send to the OpenAI API
    text = request.form['text']

    # Prepare the request data
    request_data = {
        'prompt': text,
        'temperature': 0.5
    }

    # Send a request to the OpenAI API with a timeout of 5 seconds
    response = requests.post(API_URL, json=request_data, headers=HEADERS, timeout=5)

    # Get the generated text from the response
    generated_text = response.json()['choices'][0]['text']

    # Store the generated text in the database
    store_data(generated_text)

    # Redirect back to the index page
    return redirect('/')


def store_data(data):
    """
    Stores the generated text in the database.
    """
    # Connect to the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY,
            content TEXT
        )
    ''')

    # Insert the data into the table
    cursor.execute('INSERT INTO data (content) VALUES (?)', (data,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run()
