from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

from ..models import School, User

bp_name = "schools"

bp = Blueprint(bp_name, __name__)
from ..webapp import db

properties = {
    "entity_name": "school",
    "collection_name": "Escolas",
    "list_fields": ["id","title", "Professor", "rating", "updated_at"],
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
    schools = School.query.all()
    return render_template(_j.index, entities=schools, **properties)


class EditForm(FlaskForm):
    title = StringField("Nome", validators=[InputRequired()])
    #rating = StringField("rating")
    description = StringField("Descrição")
    #release_date = StringField("release_date")
    submit = SubmitField("Enviar")
    


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
        newschool = School()
        form.populate_obj(newschool)
        db.session.add(newschool)
        db.session.commit()
        flash(f"'{ newschool.title}' created")
        return redirect(_to.show(id=newschool.id))
    else:
        flash("Error in form validation", "danger")


@bp.route("/<int:id>/show", methods=["GET"])
def show(id):
    """
    Show page.
    :return: The response.
    """
    school = db.get_or_404(School, id)
    return render_template(_j.show, entity=school, **properties)


@bp.route("/<int:id>/edit", methods=["GET"])
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    school = db.get_or_404(School, id)
    userform = EditForm(formdata=request.form, obj=school)
    return render_template(_j.edit, form=userform, **properties)


@bp.route("/<int:id>/edit", methods=["POST", "UPDATE"])
@bp.route("/<int:id>", methods=["UPDATE"])
def update(id):
    """
    Save Edited Entity
    :return: redirect to show entity
    """
    school = db.get_or_404(School, id)
    form = EditForm(formdata=request.form, obj=school)
    if form.validate_on_submit():
        form.populate_obj(school)
        db.session.commit()
        flash(f"'{ school.title}' updated")
        return redirect(_to.show(id=id))
    else:
        flash("Error in form validation", "danger")


@bp.route("/<int:id>/delete", methods=["POST", "DELETE"])
def destroy(id):
    """
    Delete Entity
    :return: redirect to list
    """
    school = db.get_or_404(School, id)
    db.session.delete(school)
    db.session.commit()
    flash(f"'{ school.title}' deleted")
    return redirect(_to.index())
