from marshmallow import Schema, fields

class CreateTaskSchema(Schema):
  title = fields.String(required=True)
  description = fields.String(required=True)
  due_date = fields.String(required=True)
  status = fields.String(required=True)
  created_by = fields.String(required=True)
  updated_by = fields.String(required=True)
  
class UpdateTaskSchema(Schema):
  title = fields.String()
  description = fields.String()
  due_date = fields.String()
  status = fields.String()
  created_by = fields.String()
  updated_by = fields.String(required=True)

class UndoTaskActionSchema(Schema):
  field = fields.String(required=True)