from app.models.task import Task
from app.models.task_action_logs import TaskActionLogs
from app.schemas.task import CreateTaskSchema, UndoTaskActionSchema, UpdateTaskSchema
from app.task import bp
from flask import request, jsonify
from marshmallow import ValidationError
from datetime import datetime
from app.extensions import db

@bp.route('', methods=['POST'])
def create_task():
    data = request.get_json()
    schema = CreateTaskSchema()
    
    try:
        # Validate request body against schema data types
        result = schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    
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

@bp.route('', methods=['GET'])
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

@bp.route('/<int:task_id>', methods=['GET'])
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

@bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    request_body = request.get_json()
    schema = UpdateTaskSchema()
    
    try:
        # Validate request body against schema data types
        result = schema.load(request_body)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    
    current_task_data = Task.query.get_or_404(task_id)

    if 'title' in request_body:
        TaskActionLogs.create_action_log(task_id, 'title', current_task_data.title, request_body['title'], request_body['updated_by'])
        current_task_data.title = request_body['title']
    
    if 'description' in request_body:
        TaskActionLogs.create_action_log(task_id, 'title', current_task_data.description, request_body.get('description', current_task_data.description), request_body['updated_by'])
        current_task_data.description = request_body.get('description', current_task_data.description)
        
    if 'due_date' in request_body:
        TaskActionLogs.create_action_log(task_id, 'due_date', current_task_data.due_date.strftime('%Y-%m-%d'), request_body['due_date'], request_body['updated_by'])
        current_task_data.due_date = datetime.strptime(request_body['due_date'], '%Y-%m-%d')
    
    if 'status' in request_body:
        TaskActionLogs.create_action_log(task_id, 'status', current_task_data.status, request_body['status'], request_body['updated_by'])
        current_task_data.status = request_body['status']
    
    if 'updated_by' in request_body:
        TaskActionLogs.create_action_log(task_id, 'updated_by', current_task_data.updated_by, request_body['updated_by'], request_body['updated_by'])
        current_task_data.updated_by = request_body['updated_by']

    current_task_data.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@bp.route('/<int:task_id>/undo', methods=['POST'])
def undo_task_action(task_id):
    request_body = request.get_json()
    schema = UndoTaskActionSchema()
    
    try:
        # Validate request body against schema data types
        result = schema.load(request_body)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    
    current_task_data = Task.query.get_or_404(task_id)
    previous_field_value = TaskActionLogs.query.filter_by(
        task_id=task_id,
        field=request_body['field']
    ).order_by(TaskActionLogs.id.desc()).first()
    
    if previous_field_value:
        if previous_field_value.field == 'title':
            current_task_data.title = previous_field_value.old_value
        if previous_field_value.field == 'description':
            current_task_data.description = previous_field_value.old_value
        if previous_field_value.field == 'due_date':
            current_task_data.due_date = datetime.strptime(previous_field_value.old_value, '%Y-%m-%d')
        if previous_field_value.field == 'status':
            current_task_data.status = previous_field_value.old_value
        if previous_field_value.field == 'updated_by':
            current_task_data.updated_by = previous_field_value.old_value
        
        db.session.delete(previous_field_value)
        db.session.commit()
    
    return jsonify({'message': 'Task undid successfully'})

@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    current_task_data = Task.query.get_or_404(task_id)
    
    current_task_data.is_deleted = True
    
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})