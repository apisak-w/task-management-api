from flask import request, jsonify
from marshmallow import ValidationError
from datetime import datetime

from app.models.task import Task
from app.models.task_action_logs import TaskActionLogs

from app.schemas.task import CreateTaskSchema, UndoTaskActionSchema, UpdateTaskSchema

from app.task import bp
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
    
    Task.create_task(data)
    
    return jsonify({'message': 'Task created successfully'}), 201

@bp.route('', methods=['GET'])
def get_tasks():
    due_date = request.args.get('due_date')
    status = request.args.get('status')
    created_by = request.args.get('created_by')
    
    tasks_list = Task.get_tasks(due_date, status, created_by)
    
    return jsonify({'tasks': tasks_list})

@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task_data = Task.get_task(task_id)
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
    
    Task.update_task(task_id, request_body)
    
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
    
    Task.undo_task_action(task_id, request_body)
    
    return jsonify({'message': 'Task undid successfully'})

@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    Task.delete_task(task_id)
    
    return jsonify({'message': 'Task deleted successfully'})