from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from app.constants.task_status import TaskStatusConstant

ACCEPTED_TASK_STATUS = [TaskStatusConstant.PENDING, TaskStatusConstant.IN_PROGRESS, TaskStatusConstant.COMPLETED]

class CreateTaskFormSchema(Schema):
  title = fields.String(required=True)
  description = fields.String(required=True)
  due_date = fields.Date(required=True)
  status = fields.Str(validate=OneOf(ACCEPTED_TASK_STATUS), required=True)
  created_by = fields.String(required=True)
  updated_by = fields.String(required=True)

class CreateTaskJsonSchema(CreateTaskFormSchema):
    pass

    class Meta:
        strict = True

class CreateTaskResponseSchema(Schema):
  message = fields.String()
  
class UpdateTaskFormSchema(Schema):
  title = fields.String()
  description = fields.String()
  due_date = fields.Date()
  status = fields.Str(validate=OneOf(ACCEPTED_TASK_STATUS))
  created_by = fields.String()
  updated_by = fields.String(required=True)

class UpdateTaskJsonSchema(UpdateTaskFormSchema):
    pass

    class Meta:
        strict = True

class UpdateTaskPathSchema(Schema):
  task_id = fields.Int(required=True)

class UpdateTaskResponseSchema(Schema):
  message = fields.String()

class UndoTaskActionPathSchema(Schema):
  task_id = fields.Int(required=True)
  
class UndoTaskActionResponseSchema(Schema):
  message = fields.String()

class UndoTaskActionFormSchema(Schema):
  field = fields.String(required=True)

class UndoTaskActionJsonSchema(UndoTaskActionFormSchema):
    pass

    class Meta:
        strict = True

class GetTaskPathSchema(Schema):
  task_id = fields.Int(required=True)

class GetTaskResponseSchema(Schema):
  created_at = fields.String()
  created_by = fields.String()
  description = fields.String()
  due_date = fields.String()
  id = fields.Int()
  is_deleted = fields.Boolean()
  status = fields.String()
  title = fields.String()
  updated_at = fields.String()
  updated_by = fields.String()
  
class GetTasksQuerySchema(Schema):
  due_date = fields.Date()
  status = fields.Str(validate=OneOf(ACCEPTED_TASK_STATUS))
  created_by = fields.String()

class GetTasksResponseSchema(Schema):
  tasks = fields.List(fields.Nested(GetTaskResponseSchema))
  
class DeleteTaskPathSchema(Schema):
  task_id = fields.Int(required=True)
  
class DeleteTaskResponseSchema(Schema):
  message = fields.String()