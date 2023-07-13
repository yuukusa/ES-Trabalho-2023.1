from . import db
from sqlalchemy.sql import func
from typing import List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Question(db.Model):
    #TODO: Add columns, etc, here
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    type_of = db.Column(db.String)
    content = db.Column(db.String)
    answer = db.Column(db.String)
    
    comments = db.Column(db.String)
    title = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<solicitation %r>" % self.id
