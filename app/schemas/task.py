from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from app.constants.task_status import TaskStatusConstant

ACCEPTED_TASK_STATUS = [TaskStatusConstant.PENDING, TaskStatusConstant.IN_PROGRESS, TaskStatusConstant.COMPLETED]


class CreateTaskSchema(Schema):
  title = fields.String(required=True)
  description = fields.String(required=True)
  due_date = fields.Date(required=True)
  status = fields.Str(validate=OneOf(ACCEPTED_TASK_STATUS), required=True)
  created_by = fields.String(required=True)
  updated_by = fields.String(required=True)
  
class UpdateTaskSchema(Schema):
  title = fields.String()
  description = fields.String()
  due_date = fields.Date()
  status = fields.Str(validate=OneOf(ACCEPTED_TASK_STATUS), required=True)
  created_by = fields.String()
  updated_by = fields.String(required=True)

class UndoTaskActionSchema(Schema):
  field = fields.String(required=True)