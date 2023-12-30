from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# SQL Server database setup
server = 'DESKTOP-6HRHA4U\SQLEXPRESS'
database = 'ScaiDb'
username = 'Zulhas'
password = '1234567'
driver = 'ODBC Driver 17 for SQL Server'

# Establish a connection to the SQL Server database
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

@app.route('/get_users', methods=['GET'])
def get_users():
    cursor.execute('SELECT id, username, themes FROM users')
    users = cursor.fetchall()
    users_list = [{'id': user.id, 'username': user.username, 'themes': user.themes} for user in users]
    return jsonify(users_list)

@app.route('/post_user', methods=['POST'])
def post_user():
    data = request.get_json()
    username = data.get('username')
    themes = data.get('themes')

    # Insert user into the users table
    cursor.execute('INSERT INTO users (username, themes) VALUES (?, ?)', (username, themes))
    conn.commit()

    return jsonify({"message": "User added successfully."})

## Rout for Keyword master data get & post

@app.route('/get_KeywordMaster', methods=['GET'])
def get_KeywordMaster():
    cursor.execute('SELECT id, name FROM KeywordMaster')
    KeywordMaster = cursor.fetchall()
    KeywordMaster_list = [{'id': Keyword.id, 'name': Keyword.name} for Keyword in KeywordMaster]
    return jsonify(KeywordMaster_list)

@app.route('/post_Keywordmaster', methods=['POST'])
def post_Keywordmaster():
    data = request.get_json()
    KeywordMaster = data.get('name')

    # Insert user into the users table
    cursor.execute('INSERT INTO KeywordsMaster  (name) VALUES ( ?)', (KeywordMaster))
    conn.commit()

    return jsonify({"message": "Keyword  added successfully."})

@app.route('/get_KeywordDetails', methods=['GET'])
def get_KeywordDetails():
    cursor.execute('SELECT id, Name, keyword_master_id FROM KeywordDetails')
    KeywordDetails = cursor.fetchall()
    KeywordDetail_list = [{'id': Keyword.id, 'name': Keyword.Name, 'keyword_master_id': Keyword.keyword_master_id} for Keyword in KeywordDetails]
    return jsonify(KeywordDetail_list)



@app.route('/post_KeywordDetails', methods=['POST'])
def post_KeywordDetails():
    try:
        data = request.get_json()
        name = data.get('name')
        keyword_master_id = data.get('keyword_master_id')

        # Insert keyword details into the KeywordDetails table
        cursor.execute('INSERT INTO KeywordDetails (Name, keyword_master_id) VALUES (?, ?)', (name, keyword_master_id))
        conn.commit()

        return jsonify({"message": "Keyword details added successfully."})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    
# Similar routes for articles, KeywordsMaster, and keywordDetails can be added here...

if __name__ == '__main__':
    app.run(debug=True)
