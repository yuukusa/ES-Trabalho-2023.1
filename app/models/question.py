from . import db
from sqlalchemy.sql import func
from typing import List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Question(db.Model):

    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)                        # enunciado da questão
    comments = db.Column(db.String)
    type_of = db.Column(db.Integer, default=1)          # 1 - Múltipla escolha, 2 - Verdadeiro ou falso, 3 - Numérica
    qty_alternatives = db.Column(db.Integer, default=4) # Quantidade de alternativas
    alternatives = db.Column(db.String)
    json_alternatives = db.Column(db.JSON, nullable=True,  default=None)
    
    #answer = db.Column(db.Integer)      
    # 1 - alternative1, 2 - alternative2, 3 - alternative3, 4 - alternative4
    # 1 - Verdadeiro, 2 - Falso
    # $ - Numérica
    answer = db.Column(db.JSON, nullable=False, default={""}) 
    
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<question %r>" % self.id
