class Exam_answered(db.Model):
    __tablename__ = "exam_answered"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    exam_mounted_id = db.Column(db.Integer, db.ForeignKey("exam_mounted.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    
    question_worth = db.Column(
        db.Integer, models.ForeignKey("exam_mounted.question_worth"))               # valor da questão
    
    student_answer = db.Column(db.json, default={})                                 # resposta do aluno
    correct_answer = db.Column(db.json, db.models.ForeignKey("question.answer"))    # resposta correta
    comments = db.Column(db.String)
    finished = db.Column(db.Boolean, default=False)                                 # prova finalizada     
    start_date = db.Column(db.DateTime, nullable=False, default=func.now())
    end_date = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<exam_answered %r>" % self.id
