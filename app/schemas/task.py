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
  
class UpdateTaskFormSchema(Schema):
  title = fields.String()
  description = fields.String()
  due_date = fields.Date()
  status = fields.Str(validate=OneOf(ACCEPTED_TASK_STATUS))
  created_by = fields.String()
  updated_by = fields.String(required=True)

class UndoTaskActionFormSchema(Schema):
  field = fields.String(required=True)

class GetTaskPathSchema(Schema):
  task_id = fields.Int(required=True)
  
class GetTasksQuerySchema(Schema):
  due_date = fields.Date()
  status = fields.Str(validate=OneOf(ACCEPTED_TASK_STATUS))
  created_by = fields.String()