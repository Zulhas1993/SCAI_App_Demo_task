from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# SQL Server database setup
server = 'DESKTOP-6HRHA4U\SQLEXPRESS'
database = 'ScaiDb'
username = 'Zulhas'
password = '1234567'
driver = 'ODBC Driver 17 for SQL Server'

# Establish a connection to the SQL Server database
#conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
# Modify the connection string
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes'

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
    CREATE TABLE users (
        id INT PRIMARY KEY IDENTITY(1,1),
        username NVARCHAR(255),
        themes NVARCHAR(MAX) NULL
    )
''')

cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'articles')
    CREATE TABLE articles (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(255) NULL,
        content NVARCHAR(MAX) NULL,
        themes NVARCHAR(MAX) NULL
    )
''')

cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'KeywordMaster')
    CREATE TABLE KeywordMaster (
        id INT PRIMARY KEY IDENTITY(1,1),     
        Name NVARCHAR(255)
    )
''')

cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'KeywordDetails')
    CREATE TABLE KeywordDetails (
        id INT PRIMARY KEY IDENTITY(1,1),
        Name NVARCHAR(255),
        keyword_master_id INT FOREIGN KEY REFERENCES KeywordMaster(id),
        Themes NVARCHAR(MAX) NULL
    )
''')

cursor.execute('''
   IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Themes')
    CREATE TABLE Themes (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(255),
        request NVARCHAR(255),
        keyword_master_id INT FOREIGN KEY REFERENCES KeywordMaster(id)
    )
''')

cursor.execute('''
   IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ThemeDetails')
    CREATE TABLE ThemeDetails (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(255),
        request NVARCHAR(255),
        Theme_id INT FOREIGN KEY REFERENCES Themes(id)
    )
''')


conn.commit()
# Define routes
@app.route('/')
def index():
    return 'Welcome to the Flask API'

# API endpoint to save themes
@app.route('/save_theme', methods=['POST'])
def save_theme():
    try:
        data = request.get_json()
        title = data.get('title')
        request_text = data.get('request')
        master_name = data.get('master_name')

        # Perform theme saving operations using raw SQL queries here
        # For example, insert into Themes table

        return jsonify({"message": "Theme saved successfully."})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
