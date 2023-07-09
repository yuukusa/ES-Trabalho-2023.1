from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column


class School(db.Model):
    __tablename__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    #rating = db.Column(db.String)
    description = db.Column(db.String)
    #professor= db.Column(db.String, db.ForeignKey("user.id"), nullable=False)
    #professor = db.relationship("User", backref="school", lazy=True)
    
    
    #release_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
        )

    def __repr__(self):
        return f"<School id = {self.id}; name = {self.title}>"
    
