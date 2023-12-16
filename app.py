from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.due_date}', '{self.status}', '{self.created_by}', '{self.updated_by}')"

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'),
        status=data['status'],
        created_by=data['created_by'],
        updated_by=data['created_by']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    due_date = request.args.get('due_date')
    status = request.args.get('status')
    created_by = request.args.get('created_by')
    
    query = Task.query
    if due_date:
        query = query.filter(Task.due_date == datetime.strptime(due_date, '%Y-%m-%d'))
    if status:
        query = query.filter(Task.status == status)
    if created_by:
        query = query.filter(Task.created_by == created_by)

    tasks = query.all()
    tasks_list = [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'status': task.status,
            'created_by': task.created_by,
            'updated_by': task.updated_by,
            'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        for task in tasks
    ]
    return jsonify({'tasks': tasks_list})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.strftime('%Y-%m-%d'),
        'status': task.status,
        'created_by': task.created_by,
        'updated_by': task.updated_by,
        'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify({'task': task_data})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    task.title = data['title']
    task.description = data.get('description', task.description)
    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    task.status = data['status']
    task.updated_by = data['updated_by']
    task.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
