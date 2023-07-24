from . import db
from sqlalchemy.sql import func
from typing import List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Exam_mounted(db.Model):
    #TODO: Add columns, etc, here
    __tablename__ = "exam_mounted"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String)
    
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    
    question_worth = db.Column(db.Integer)
    
    comments = db.Column(db.String)
    
    
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<exam_mounted %r>" % self.id
