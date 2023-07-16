from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from wtforms import StringField, SubmitField, SelectField, IntegerField, BooleanField, RadioField, TextAreaField, HiddenField, SelectMultipleField, fields, FileField, FormField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

import json
from flask_login import current_user


from ..models import Question, User, Exam, Exam_mounted #, Exam_answered

bp_name = "questions"

bp = Blueprint(bp_name, __name__)
from ..webapp import db




properties = {
    "entity_name": "question",
    "collection_name": "questions",
    "list_fields": ["id","title", "type_of", "answer", "alternatives"],
    
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
    # curr_user = User.query.filter_by(id=current_user.id).first()
    # print(curr_user.username)
    
    
    
    questions = Question.query.all()
    return render_template(_j.index, entities=questions, **properties)




@bp.route("/json", methods=["GET"])
def test():
    # query alternatives and jsonify to send to frontend
    alternatives =  [(question.alternatives) for question in Question.query.all()]
    print("query return type:", type(alternatives))
         
    print("len: ", len(alternatives))
    print(f"\n\n:\n\n ")
        
    print(f"\n\nTestando json.loads:\n\n ")
    print("ALL: \n", alternatives)
    print( "\n:END\n\n")
    
    print("for loop: ")
    for i in alternatives:
        print(i)
        print(type(i))
    print(f"\n:fim for loop\n\n ")
        
    
    alternatives = json.loads(alternatives[0])
    #print(type(alternatives))
    #print(alternatives)
    jsnfy = (jsonify(alternatives))
    print(type(jsnfy))
    print(jsnfy)
    
    # alternatives = json.loads(alternatives) 
    
    return jsnfy

# class alternativesForm(FlaskForm):
#     alternative = StringField("alternative", validators=[InputRequired()])
#     answer = IntegerField("answer")
    
class EditForm(FlaskForm):
    title = TextAreaField("Question Statement", validators=[InputRequired()])
    comments = StringField("comments")
    type_of = SelectField("type of Question", choices=[(1, "Múltipla escolha (a, b, c, d, ...)"), (2, "Verdadeiro ou falso (V ou F)"), (3, "Numérica")])
    number_of_alternatives = IntegerField("number of alternatives")
    #alternatives = FormField(alternativesForm)
    alternatives = StringField("alternatives")
    answer = IntegerField("answer")
    
    submit = SubmitField("Submit")
    #nextfield = SubmitField("Next")
    


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
        newquestion = Question()
        form.populate_obj(newquestion)
        db.session.add(newquestion)
        db.session.commit()
        flash(f"'{ newquestion.title}' created")
        return redirect(_to.show(id=newquestion.id))
    else:
        flash("Error in form validation", "danger")


@bp.route("/<int:id>/show", methods=["GET"])
def show(id):
    """
    Show page.
    :return: The response.
    """
    alternative =  [(question.alternatives) for question in Question.query.filter_by(id=id).all()]
    
    question = db.get_or_404(Question, id)
    return render_template(_j.show, entity=question, **properties)




@bp.route("/<int:id>/edit", methods=["GET"])
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    question = db.get_or_404(Question, id)
    userform = EditForm(formdata=request.form, obj=question)
    return render_template(_j.edit, form=userform, **properties)


@bp.route("/<int:id>/edit", methods=["POST", "UPDATE"])
@bp.route("/<int:id>", methods=["UPDATE"])
def update(id):
    """
    Save Edited Entity
    :return: redirect to show entity
    """
    question = db.get_or_404(Question, id)
    form = EditForm(formdata=request.form, obj=question)
    # for _ in range(form.number_of_alternatives.data):
    #     form.alternatives.append_entry()
    # if form.validate_on_submit():
    form.populate_obj(question)
    db.session.commit()
    flash(f"'{ question.title}' updated")
    return redirect(_to.show(id=id))
    # else:
    #     flash("Error in form validation", "danger")


@bp.route("/<int:id>/delete", methods=["POST", "DELETE"])
def destroy(id):
    """
    Delete Entity
    :return: redirect to list
    """
    question = db.get_or_404(Question, id)
    db.session.delete(question)
    db.session.commit()
    flash(f"'{ question.title}' deleted")
    return redirect(_to.index())
