from flask import Flask, render_template, request
import sqlite3
import requests

app = Flask(__name__)

# SQLite database setup
conn = sqlite3.connect('articles.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        themes TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        themes TEXT
    )
''')
conn.commit()

# OpenAI GPT-4 API key
openai_api_key = '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'

# Web scraping or API integration for article sources
article_sources = [
   # {'url': 'https://example.com/api/news', 'name': 'News API'},
    {'url': 'https://cniasia.news/', 'name': 'News API'},
    #https://cniasia.news/category/70/1
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

if __name__ == '__main__':
    app.run(debug=True)
