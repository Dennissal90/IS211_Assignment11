from flask import Flask, render_template, request, redirect, url_for
import pickle
import os

app = Flask(__name__)

try:
    with open('todos.pkl', 'rb') as f:
        todos = pickle.load(f)
except (EOFError, FileNotFoundError):
    todos = []

@app.route('/')
def home():
    return render_template('index.html', todos=todos)

@app.route('/submit', methods=['POST'])
def submit_todo():
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')
    
    if task and email and priority in ['Low', 'Medium', 'High']:
        todos.append({'task': task, 'email': email, 'priority': priority})
    return redirect(url_for('home'))

@app.route('/clear', methods=['POST'])
def clear_todos():
    todos.clear()
    return redirect(url_for('home'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_todo(index):
    try:
        todos.pop(index)
    except IndexError:
        pass
    return redirect(url_for('home'))

@app.route('/save', methods=['POST'])
def save_todos():
    with open('todos.pkl', 'wb') as f:
        pickle.dump(todos, f)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)