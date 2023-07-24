from flask.cli import AppGroup
from .webapp import db
from .models import User, Question, Exam
from .seed import users, questions, exams

seed_cli = AppGroup("seed")


@seed_cli.command("questions")
def seed_questions():
    "Add seed data to the database."
    for question in questions:
        db.session.add(Question(**question))
    db.session.commit()


@seed_cli.command("exams")
def seed_exams():
    "Add seed data to the database."
    for exam in exams:
        db.session.add(Exam(**exam))
    db.session.commit()


@seed_cli.command("users")
def seed_users():
    "Add seed data to the database."
    for user in users:
        db.session.add(User(**user))
    db.session.commit()

