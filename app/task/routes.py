from flask import request, jsonify
from marshmallow import ValidationError
from flasgger_marshmallow import swagger_decorator

from app.models.task import Task
from app.schemas.task import CreateTaskFormSchema, CreateTaskJsonSchema, CreateTaskResponseSchema, DeleteTaskPathSchema, DeleteTaskResponseSchema, GetTaskPathSchema, GetTaskResponseSchema, GetTasksQuerySchema, UndoTaskActionFormSchema, UndoTaskActionJsonSchema, UndoTaskActionPathSchema, UndoTaskActionResponseSchema, UpdateTaskFormSchema, UpdateTaskJsonSchema, UpdateTaskPathSchema, UpdateTaskResponseSchema
from app.task import bp

SWAGGER_DECORATOR_OPTIONS = {
    'tags': ['Task']
}

@swagger_decorator(json_schema=CreateTaskJsonSchema, response_schema={201: CreateTaskResponseSchema}, tags=SWAGGER_DECORATOR_OPTIONS['tags'])
@bp.route('', methods=['POST'])
def create_task():
    data = request.get_json()
    schema = CreateTaskFormSchema()
    
    try:
        # Validate request body against schema data types
        result = schema.load(data)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    
    Task.create_task(data)
    
    return jsonify({'message': 'Task created successfully'}), 201

@swagger_decorator(query_schema=GetTasksQuerySchema, response_schema={200: CreateTaskFormSchema}, tags=SWAGGER_DECORATOR_OPTIONS['tags'])
@bp.route('', methods=['GET'])
def get_tasks():
    due_date = request.args.get('due_date')
    status = request.args.get('status')
    created_by = request.args.get('created_by')
    
    tasks_list = Task.get_tasks(due_date, status, created_by)
    
    return jsonify(tasks_list)

@swagger_decorator(path_schema=GetTaskPathSchema, response_schema={200: GetTaskResponseSchema}, tags=SWAGGER_DECORATOR_OPTIONS['tags'])
@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task_data = Task.get_task(task_id)
    return jsonify(task_data)

@swagger_decorator(path_schema=UpdateTaskPathSchema, json_schema=UpdateTaskJsonSchema, response_schema={200: UpdateTaskResponseSchema}, tags=SWAGGER_DECORATOR_OPTIONS['tags'])
@bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    request_body = request.get_json()
    schema = UpdateTaskFormSchema()
    
    try:
        # Validate request body against schema data types
        result = schema.load(request_body)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    
    Task.update_task(task_id, request_body)
    
    return jsonify({'message': 'Task updated successfully'})

@swagger_decorator(path_schema=UndoTaskActionPathSchema, json_schema=UndoTaskActionJsonSchema, response_schema={200: UndoTaskActionResponseSchema}, tags=SWAGGER_DECORATOR_OPTIONS['tags'])
@bp.route('/<int:task_id>/undo', methods=['POST'])
def undo_task_action(task_id):
    request_body = request.get_json()
    schema = UndoTaskActionFormSchema()
    
    try:
        # Validate request body against schema data types
        result = schema.load(request_body)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    
    Task.undo_task_action(task_id, request_body)
    
    return jsonify({'message': 'Task undid successfully'})

@swagger_decorator(path_schema=DeleteTaskPathSchema, response_schema={200: DeleteTaskResponseSchema}, tags=SWAGGER_DECORATOR_OPTIONS['tags'])
@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    Task.delete_task(task_id)
    
    return jsonify({'message': 'Task deleted successfully'})