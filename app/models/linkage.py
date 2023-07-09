from . import db
from sqlalchemy.sql import func
from typing import List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Linkage(db.Model):
    #TODO: Add columns, etc, here
    __tablename__ = "linkage"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    rating = db.Column(db.String(6))
    comments = db.Column(db.String)
    active = db.Column(db.Integer)

    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student = db.relationship("User", backref="linkage", foreign_keys=[student_id], lazy=True)
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=False)
    school = db.relationship("School", backref="linkage", foreign_keys=[school_id])
    #professor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #professor = db.relationship("User", backref="linkage", lazy=True, foreign_keys=[professor_id])
    presence = db.Column(db.Boolean)
       
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<Linkage %r>" % self.id
