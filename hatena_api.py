from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Dummy data for testing
tasks = [
    {
        'id': 1,
        'title': 'Learn Flask',
        'done': False
    },
    {
        'id': 2,
        'title': 'Build API',
        'done': True
    }
]

# Define routes
@app.route('/')
def index():
    return 'Welcome to the Flask API'

# API endpoint to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# API endpoint to get a specific task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task})

# API endpoint to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Title is required'}), 400

    new_task = {
        'id': len(tasks) + 1,
        'title': request.json['title'],
        'done': False
    }
    tasks.append(new_task)

    return jsonify({'task': new_task}), 201

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
