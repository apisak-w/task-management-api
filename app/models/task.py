from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db

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
