from . import db
from sqlalchemy.sql import func
from typing import List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Exam(db.Model):
    #TODO: Add columns, etc, here
    __tablename__ = "exam"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    punctuation = db.Column(db.Integer)
    
    title = db.Column(db.String)
    comments = db.Column(db.String)
    
    
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<solicitation %r>" % self.id
