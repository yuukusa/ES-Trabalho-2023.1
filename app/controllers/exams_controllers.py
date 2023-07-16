from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField, RadioField, TextAreaField, HiddenField, SelectMultipleField, fields, FileField 
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

from ..models import Exam

bp_name = "exams"

bp = Blueprint(bp_name, __name__)
from ..webapp import db

properties = {
    "entity_name": "exam",
    "collection_name": "exams",
    "list_fields": ["id","title", "qntityOfQuestions", "punctuation", "updated_at"],
}


class _to:
    def __to(method):
        return lambda **kwargs: url_for(f"{bp_name}.{method}", **kwargs)

    index = __to("index")
    show = __to("show")
    edit = __to("edit")
    delete = __to("delete")


class _j:
    index = f"{bp_name}/index.jinja2"
    edit = f"{bp_name}/edit.jinja2"
    show = f"{bp_name}/show.jinja2"
    new = f"{bp_name}/new.jinja2"
    create = f"{bp_name}/create.jinja2"
    search_tmdb = f"{bp_name}/search_tmdb.jinja2"


@bp.route("/", methods=["GET"])
def index():
    """
    Index page.
    :return: The response.
    """
    exams = Exam.query.all()
    return render_template(_j.index, entities=exams, **properties)


class EditForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    comments = StringField("comments, description")
    qntityOfQuestions = IntegerField("quantity of questions")
    punctuation = IntegerField("overall punctuation")
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    submit = SubmitField("Submit")
 


@bp.route("/new", methods=["GET"])
def new():
    """
    Page to create new Entity
    :return: render create template
    """
    form = EditForm()
    return render_template(_j.new, form=form, **properties)


@bp.route("/", methods=["POST"])
def create():
    """
    Create new entity
    :return: redirect to view new entity
    """
    form = EditForm(formdata=request.form)
    if form.validate_on_submit():
        newexam = Exam()
        form.populate_obj(newexam)
        db.session.add(newexam)
        db.session.commit()
        flash(f"'{ newexam.title}' created")
        return redirect(_to.show(id=newexam.id))
    else:
        flash("Error in form validation", "danger")


@bp.route("/<int:id>/show", methods=["GET"])
def show(id):
    """
    Show page.
    :return: The response.
    """
    exam = db.get_or_404(Exam, id)
    return render_template(_j.show, entity=exam, **properties)


@bp.route("/<int:id>/edit", methods=["GET"])
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    exam = db.get_or_404(Exam, id)
    userform = EditForm(formdata=request.form, obj=exam)
    return render_template(_j.edit, form=userform, **properties)


@bp.route("/<int:id>/edit", methods=["POST", "UPDATE"])
@bp.route("/<int:id>", methods=["UPDATE"])
def update(id):
    """
    Save Edited Entity
    :return: redirect to show entity
    """
    exam = db.get_or_404(Exam, id)
    form = EditForm(formdata=request.form, obj=exam)
    if form.validate_on_submit():
        form.populate_obj(exam)
        db.session.commit()
        flash(f"'{ exam.title}' updated")
        return redirect(_to.show(id=id))
    else:
        flash("Error in form validation", "danger")


@bp.route("/<int:id>/delete", methods=["POST", "DELETE"])
def destroy(id):
    """
    Delete Entity
    :return: redirect to list
    """
    exam = db.get_or_404(Exam, id)
    db.session.delete(exam)
    db.session.commit()
    flash(f"'{ exam.title}' deleted")
    return redirect(_to.index())


