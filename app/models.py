from datetime import datetime
from app import db

CATEGORIES = ["General", "Urgente", "Académico", "Administrativo"]


class Notice(db.Model):
    __tablename__ = "notices"

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(120), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    category   = db.Column(db.String(30), nullable=False, default="General")
    author     = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notice {self.id}: {self.title}>"
