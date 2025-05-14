from datetime import datetime
from app import db


class Data(db.Model):
    __tablename__ = "data_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=None, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Data id={self.id}>"
