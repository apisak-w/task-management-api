import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'tasks.sqlite')
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
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.due_date}', '{self.status}', '{self.created_by}', '{self.updated_by}', '{self.is_deleted}')"

class TaskActionLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    field = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.String(255), nullable=False)
    new_value = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"TaskActionLogs('{self.task_id}', '{self.field}', '{self.old_value}', '{self.new_value}', '{self.created_by}')"

db.create_all()

def create_action_log(task_id, field, old_value, new_value, created_by):
    if str(old_value) != str(new_value):
        new_action_log = TaskActionLogs(
            task_id=task_id,
            field=field,
            old_value=str(old_value),
            new_value=str(new_value),
            created_by=created_by
        )
        db.session.add(new_action_log)

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
    query = query.filter(Task.is_deleted == False)
    
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
            'updated_at': task.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': task.is_deleted
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
    current_task_data = Task.query.get_or_404(task_id)
    request_body = request.get_json()
    
    if 'updated_by' not in request_body:
        return jsonify({'message': 'Missing updated_by parameter'}), 400

    if 'title' in request_body:
        create_action_log(task_id, 'title', current_task_data.title, request_body['title'], request_body['updated_by'])
        current_task_data.title = request_body['title']
    
    if 'description' in request_body:
        create_action_log(task_id, 'title', current_task_data.description, request_body.get('description', current_task_data.description), request_body['updated_by'])
        current_task_data.description = request_body.get('description', current_task_data.description)
        
    if 'due_date' in request_body:
        create_action_log(task_id, 'due_date', current_task_data.due_date.strftime('%Y-%m-%d'), request_body['due_date'], request_body['updated_by'])
        current_task_data.due_date = datetime.strptime(request_body['due_date'], '%Y-%m-%d')
    
    if 'status' in request_body:
        create_action_log(task_id, 'status', current_task_data.status, request_body['status'], request_body['updated_by'])
        current_task_data.status = request_body['status']
    
    if 'updated_by' in request_body:
        create_action_log(task_id, 'updated_by', current_task_data.updated_by, request_body['updated_by'], request_body['updated_by'])
        current_task_data.updated_by = request_body['updated_by']

    current_task_data.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    current_task_data = Task.query.get_or_404(task_id)
    
    current_task_data.is_deleted = True
    
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
