from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import StringField, SubmitField, SelectField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange

from ..models import Linkage, School, User

bp_name = "linkages"

bp = Blueprint(bp_name, __name__)
from ..webapp import db
import app

properties = {
    "entity_name": "linkage",
    "collection_name": "Vínculos",
    "list_fields": ["id", "student_id", "school_id", "active", "title", "comments", "rating","updated_at"]
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
    linkages = Linkage.query.all()
    return render_template(_j.index, entities=linkages, **properties)


class EditForm(FlaskForm):
    title = StringField("Titulo", validators=[InputRequired()])
    rating = StringField("Avaliação / Feedback")
    description = StringField("Descrição")
    
    school_id = SelectField("school", choices=[], coerce=int)
    #school_id = StringField("ID Escola", validators=[InputRequired()])
    student_id = SelectField("Estudante", choices=[], validators=[InputRequired()])

    active = SelectField("Está ativo?", choices=[(1, 'Sim'), (0, 'Não')])
    comments = StringField("Comentários")
    
    submit = SubmitField("Enviar!")


@bp.route("/new", methods=["GET"])
def new():
    """
    Page to create new Entity
    :return: render create template
    """
    form = EditForm()
    form.student_id.choices = [(user.id, user.name) for user in User.query.filter_by(is_student=True).all()]
    form.school_id.choices = [(school.id, school.title) for school in School.query.all()]
    return render_template(_j.new, form=form, **properties)


@bp.route("/", methods=["POST"])
def create():
    """
    Create new entity
    :return: redirect to view new entity
    """
    form = EditForm(formdata=request.form)
    
    #if form.validate():
    newlinkage = Linkage()
    print("---> form.data: \n",form.data)
    form.populate_obj(newlinkage)
    db.session.add(newlinkage)
    db.session.commit()
    flash(f"'{ newlinkage.title}' created")
    return redirect(_to.show(id=newlinkage.id))
    #else:
        #flash("Error in form validation", "danger")


@bp.route("/<int:id>/show", methods=["GET"])
def show(id):
    """
    Show page.
    :return: The response.
    """
    linkage = db.get_or_404(Linkage, id)
    return render_template(_j.show, entity=linkage, **properties)


@bp.route("/<int:id>/edit", methods=["GET"])
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    linkage = db.get_or_404(Linkage, id)
    userform = EditForm(formdata=request.form, obj=linkage)
    userform.student_id.choices = [(user.id, user.name) for user in User.query.filter_by(is_student=True).all()]
    userform.school_id.choices = [(school.id, school.title) for school in School.query.all()]
    return render_template(_j.edit, form=userform, **properties)


@bp.route("/<int:id>/edit", methods=["POST", "UPDATE"])
@bp.route("/<int:id>", methods=["UPDATE"])
def update(id):
    """
    Save Edited Entity
    :return: redirect to show entity
    """
    linkage = db.get_or_404(Linkage, id)
    form = EditForm(formdata=request.form, obj=linkage)
    #if form.validate_on_submit():
    form.populate_obj(linkage)
    db.session.commit()
    flash(f"'{ linkage.title}' updated")
    return redirect(_to.show(id=id))
    #else:
        #flash("Error in form validation", "danger")


@bp.route("/<int:id>/delete", methods=["POST", "DELETE"])
def destroy(id):
    """
    Delete Entity
    :return: redirect to list
    """
    linkage = db.get_or_404(Linkage, id)
    db.session.delete(linkage)
    db.session.commit()
    flash(f"'{ linkage.title}' deleted")
    return redirect(_to.index())
