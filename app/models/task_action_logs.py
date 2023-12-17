from datetime import datetime
from app.extensions import db

# Decided to use Audit Table style (https://dev.to/zhiyueyi/design-a-table-to-keep-historical-changes-in-database-10fn)
# to keep track of changes in every fields of tasks,
# but tradeoff in terms of database size as the amount of records will be increased with every changes.
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