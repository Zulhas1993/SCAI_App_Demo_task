from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# SQL Server database setup
server = 'DESKTOP-361QN81\SQLEXPRESS'
database = 'ScaiDb'
username = 'user'
password = '1234567'
driver = 'ODBC Driver 17 for SQL Server'

# Establish a connection to the SQL Server database
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Create ThemeInfo table if not exists
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ThemeInfo')
    CREATE TABLE ThemeInfo (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(MAX),
        request NVARCHAR(MAX),
        user_id INT FOREIGN KEY REFERENCES users(id)
    )
''')

conn.commit()

# Static suggestions
suggestions = [
    "What are your thoughts on this topic?",
    "Can you provide more details about your interest?",
    "Tell us about your experiences with this theme.",
    "Why is this theme important to you?",
    "Any specific aspects of the theme you'd like to explore?"
]

# Sample user data
user_data = {
    "user_id": 1,
    "username": "John Doe",
    "email": "john.doe@example.com"
}

# Define routes
@app.route('/')
def index():
    return jsonify({"suggestions": suggestions})

# API endpoint to save theme
@app.route('/save_theme', methods=['POST'])
def save_theme():
    try:
        data = request.get_json()
        title = data.get('title')
        request_text = data.get('request')
        user_id = data.get('user_id')  # Assuming you pass the user_id from the frontend or another source

        # Insert into ThemeInfo table
        cursor.execute('''
            INSERT INTO ThemeInfo (title, request, user_id)
            VALUES (?, ?, ?)
        ''', title, request_text, user_id)

        conn.commit()

        return jsonify({"message": "Theme saved successfully."})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

# API endpoint to get user information and theme list
@app.route('/user_info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    try:
        # Get user information
        cursor.execute('SELECT * FROM users WHERE id = ?', user_id)
        user_info = cursor.fetchone()

        # Get theme list for the user
        cursor.execute('SELECT * FROM ThemeInfo WHERE user_id = ?', user_id)
        themes = cursor.fetchall()

        return jsonify({"user_info": user_info, "themes": themes})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
