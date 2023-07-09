from flask import Blueprint, render_template, request, redirect, url_for, flash
from wtforms import StringField, SubmitField, SelectField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, InputRequired, NumberRange

from ..models import Solicitation, School, User

bp_name = "solicitations"

bp = Blueprint(bp_name, __name__)
from ..webapp import db
import app

properties = {
    "entity_name": "solicitation",
    "collection_name": "Solicitações",
    "list_fields": ["id", "student_id", "school_id", "approval", "title", "comments", "created_at", "updated_at"],
}


class _to:
    def __to(method):
        return lambda **kwargs: url_for(f"{bp_name}.{method}", **kwargs)

    index = __to("index")
    show = __to("show")
    edit = __to("edit")
    delete = __to("delete")
    new = __to("new")


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
    solicitations = Solicitation.query.all()
    return render_template(_j.index, entities=solicitations, **properties)


class EditForm(FlaskForm):
    title = StringField("Descrição Pedido", validators=[InputRequired()])
    # rating = StringField("Avaliação")
    description = StringField("Data Pedido")
    
    school_id = SelectField("Escola",choices=[], validators=[InputRequired()])
    student_id = SelectField("Estudante",choices=[], validators=[InputRequired()])
    # school_id = StringField("ID Escola", validators=[InputRequired()])
    # student_id = StringField("ID Estudante", validators=[InputRequired()])
    approval = SelectField("Status", choices=[(1, 'Aceito'), (2, 'Rejeitado'), (3, 'Documentos pendentes')])   
    comments = StringField("Informações Adicionais")

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
    #if form.validate_on_submit():
    newsolicitation = Solicitation()
    form.populate_obj(newsolicitation)
    db.session.add(newsolicitation)
    db.session.commit()
    flash(f"'{ newsolicitation.title}' created")
    return redirect(_to.show(id=newsolicitation.id))
    #else:
        #print("saida 2")
        #flash("Error in form validation", "danger")
        #return redirect(_to.index())


@bp.route("/<int:id>/show", methods=["GET"])
def show(id):
    """
    Show page.
    :return: The response.
    """
    solicitation = db.get_or_404(Solicitation, id)
    return render_template(_j.show, entity=solicitation, **properties)


@bp.route("/<int:id>/edit", methods=["GET"])
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    solicitation = db.get_or_404(Solicitation, id)
    userform = EditForm(formdata=request.form, obj=solicitation)
    userform.student_id.choices = [(user.id, user.username) for user in User.query.filter_by(is_student=True).all()]
    userform.school_id.choices = [(school.id, school.title) for school in School.query.all()]
    return render_template(_j.edit, form=userform, **properties)


@bp.route("/<int:id>/edit", methods=["POST", "UPDATE"])
@bp.route("/<int:id>", methods=["UPDATE"])
def update(id):
    """
    Save Edited Entity
    :return: redirect to show entity
    """
    solicitation = db.get_or_404(Solicitation, id)
    form = EditForm(formdata=request.form, obj=solicitation)
    #if form.validate_on_submit():
    form.populate_obj(solicitation) 
    db.session.commit()
    flash(f"'{ solicitation.title}' updated")
    return redirect(_to.show(id=id))
    #else:
        #flash("Error in form validation", "danger")
        #return redirect(_to.index())


@bp.route("/<int:id>/delete", methods=["POST", "DELETE"])
def destroy(id):
    """
    Delete Entity
    :return: redirect to list
    """
    solicitation = db.get_or_404(Solicitation, id)
    db.session.delete(solicitation)
    db.session.commit()
    flash(f"'{ solicitation.title}' deleted")
    return redirect(_to.index())
