from flask import Flask, render_template, request
import pyodbc
import requests
from gevent.pywsgi import WSGIServer
app = Flask(__name__)

# SQL Server database setup
server = 'DESKTOP-361QN81\SQLEXPRESS'
database = 'articles'
username = 'user'
password = '1234567'
driver = 'ODBC Driver 17 for SQL Server'

# Establish a connection to the SQL Server database
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
    CREATE TABLE users (
        id INT PRIMARY KEY IDENTITY(1,1),
        username NVARCHAR(255),
        themes NVARCHAR(MAX)
    )
''')

cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'articles')
    CREATE TABLE articles (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(255),
        content NVARCHAR(MAX),
        themes NVARCHAR(MAX)
    )
''')

conn.commit()

# OpenAI GPT-4 API key
openai_api_key = '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'

# Web scraping or API integration for article sources
article_sources = [
    {'url': 'https://cniasia.news/', 'name': 'News API'},
    # Add more sources as needed
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    themes = request.form.getlist('themes')

    # Store user registration in the database
    cursor.execute('INSERT INTO users (username, themes) VALUES (?, ?)', (username, ','.join(themes)))
    conn.commit()

    return render_template('registration_success.html', username=username, themes=themes)

@app.route('/dashboard/<username>')
def dashboard(username):
    # Retrieve user's themes from the database
    cursor.execute('SELECT themes FROM users WHERE username = ?', (username,))
    user_themes = cursor.fetchone()[0].split(',')

    # Query articles based on user's themes
    suggested_articles = []
    for source in article_sources:
        response = requests.get(source['url'])
        articles = response.json()

        for article in articles:
            article_themes = article['themes'].split(',')
            if any(theme in article_themes for theme in user_themes):
                suggested_articles.append(article)

    # Generate summaries for suggested articles using OpenAI GPT-4
    for article in suggested_articles:
        article['summary'] = generate_summary(article['content'])

    return render_template('dashboard.html', username=username, suggested_articles=suggested_articles)

def generate_summary(content):
    # Use OpenAI GPT-4 for summarization
    headers = {'Authorization': f'Bearer {openai_api_key}'}
    data = {'content': content, 'max_tokens': 140}
    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers, json=data)
    return response.json()['choices'][0]['text']

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()