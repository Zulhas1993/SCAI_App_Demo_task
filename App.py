from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://user:1234567@DESKTOP-361QN81\\SQLEXPRESS/articles?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    interests = db.Column(db.String(255))

class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keywords = db.Column(db.String(255))
    related_info = db.Column(db.Text)

# Routes
@app.route('/')
def index():
    # Fetch user interests and display news articles
    # Implement logic to retrieve and display news articles
    return render_template('index.html')

@app.route('/theme-setting', methods=['GET', 'POST'])
def theme_setting():
    if request.method == 'POST':
        # Handle form submission
        keywords = request.form.getlist('keywords')
        # Call ChatGPT API to get related information based on keywords
        related_info = "Example related information from ChatGPT"
        
        # Save theme to the database
        theme = Theme(keywords=','.join(keywords), related_info=related_info)
        db.session.add(theme)
        db.session.commit()

    # Fetch keywords for rendering the form
    keywords = ['Technology', 'Science', 'Art', 'Music']  # Replace with actual keywords
    return render_template('theme_setting.html', keywords=keywords)

@app.route('/my-page')
def my_page():
    # Fetch user profile and saved themes from the database
    user = User.query.filter_by(username='example_user').first()
    themes = Theme.query.all()
    return render_template('my_page.html', user=user, themes=themes)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()