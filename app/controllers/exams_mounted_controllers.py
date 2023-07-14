from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField, RadioField, TextAreaField, HiddenField, SelectMultipleField, fields, FileField 
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

from ..models import Exam_mounted

bp_name = "exams_mounted"

bp = Blueprint(bp_name, __name__)
from ..webapp import db

properties = {
    "entity_name": "exam_mounted",
    "collection_name": "exams_mounted",
    "list_fields": ["id","title", "exam_id", "question_id", "question_worth", "status", "comments"],
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
    exams_mounted = Exam_mounted.query.all()
    return render_template(_j.index, entities=exams_mounted, **properties)


class EditForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    description = StringField("description")
    release_date = StringField("release_date")
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
        newexam_mounted = Exam_mounted()
        form.populate_obj(newexam_mounted)
        db.session.add(newexam_mounted)
        db.session.commit()
        flash(f"'{ newexam_mounted.title}' created")
        return redirect(_to.show(id=newexam_mounted.id))
    else:
        flash("Error in form validation", "danger")


@bp.route("/<int:id>/show", methods=["GET"])
def show(id):
    """
    Show page.
    :return: The response.
    """
    exam_mounted = db.get_or_404(Exam_mounted, id)
    return render_template(_j.show, entity=exam_mounted, **properties)


@bp.route("/<int:id>/edit", methods=["GET"])
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    exam_mounted = db.get_or_404(Exam_mounted, id)
    userform = EditForm(formdata=request.form, obj=exam_mounted)
    return render_template(_j.edit, form=userform, **properties)


@bp.route("/<int:id>/edit", methods=["POST", "UPDATE"])
@bp.route("/<int:id>", methods=["UPDATE"])
def update(id):
    """
    Save Edited Entity
    :return: redirect to show entity
    """
    exam_mounted = db.get_or_404(Exam_mounted, id)
    form = EditForm(formdata=request.form, obj=exam_mounted)
    if form.validate_on_submit():
        form.populate_obj(exam_mounted)
        db.session.commit()
        flash(f"'{ exam_mounted.title}' updated")
        return redirect(_to.show(id=id))
    else:
        flash("Error in form validation", "danger")


@bp.route("/<int:id>/delete", methods=["POST", "DELETE"])
def destroy(id):
    """
    Delete Entity
    :return: redirect to list
    """
    exam_mounted = db.get_or_404(Exam_mounted, id)
    db.session.delete(exam_mounted)
    db.session.commit()
    flash(f"'{ exam_mounted.title}' deleted")
    return redirect(_to.index())
