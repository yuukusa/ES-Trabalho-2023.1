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
    "list_fields": ["id","title", "type_of", "answer", "json_alternatives"],
    
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




@bp.route("/<int:id>/json", methods=["GET"])
def viewJson(id):
    # query alternatives and jsonify to send to frontend
    alternatives =  [(question.alternatives) for question in Question.query.filter_by(id=id).all()]
    #alternatives =  [(question.alternatives) for question in Question.query.all()]
    print("query return type:", type(alternatives))
    print("query length: ", len(alternatives))
    print(f"\n\n\n\n ")
        
    print(f"\n\nTestando json.loads:\n\n ")
    print("(query): \n", alternatives)
    print( "\n:END\n\n")
    
    print("query \"elem[0]\" : ", alternatives[0])
    print(type(alternatives[0]))
    print(f"\n\n\n ")
    
    #alternatives = json.loads(alternatives[0])
    #print(type(alternatives))
    #print(alternatives)
    jsnfy = (jsonify(alternatives))
    print(type(jsnfy))
    print(jsnfy)
    
    # alternatives = json.loads(alternatives) 
    
    return jsnfy

class AlternativesForm(FlaskForm):
    alternative = StringField("alternative", validators=[InputRequired()])
    answer = IntegerField("answer", validators=[InputRequired()])
    nextfield = SubmitField("Next")

class EditForm(FlaskForm):
    title = TextAreaField("Question Statement", validators=[InputRequired()])
    s1 = "1 - Múltipla escolha, 2 - Verdadeiro ou falso, 3 - Numérica"
    type_of = SelectField("type of Question", choices=[(1, "Múltipla escolha (a, b, c, d, ...)"), (2, "Verdadeiro ou falso (V ou F)"), (3, "Numérica")], coerce=int, validators=[InputRequired()], description=s1, render_kw=dict(placeholder=s1))
    qty_alternatives = IntegerField("number of alternatives", default=4, description="# of alternatives. default: 4", 
                                    validators=[InputRequired()], render_kw=dict(placeholder="optional"))
    s2 = "in json format, like: {\"a\": \"alternative1\", \"b\": \"alternative2\", \"c\": \"alternative3\", \"d\": \"alternative4\"}"
    if type_of == 1:
        json_alternatives = FormField(AlternativesForm, "alternatives: ", validators=[InputRequired()], description=s2, render_kw=dict(placeholder=s1))
    else:
        json_alternatives = StringField("alternatives: ", validators=[InputRequired()], description=s2, render_kw=dict(placeholder=s1))
        s3 ="in json format, like: 1, 2, 3, 4, ... for multiple choice; 1 for true and 0 for false; literal number (#) for numeric answer"
        s4 = "type the answer here"
        answer = IntegerField("answer", validators=[InputRequired()], description=s3, render_kw=dict(placeholder=s4), default=None)
        
    comments = StringField("comments?", description="", render_kw=dict(placeholder="optional"))
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
    alternatives_query =  [(question.json_alternatives) for question in Question.query.filter_by(id=id).all()]
    print("query return type:", type(alternatives_query))
    print("query length: ", len(alternatives_query))
    print(f"query: {alternatives_query} \n\n\n\n ")
    json_alternatives = str(alternatives_query[0])
    alternatives = json.loads(json_alternatives)
    list1 = []
    # for i in alternatives:
    #     list1 += [(i, alternatives[i])]
    
    print(f"tuples: {list1} \n\n\n\n ")
    question = db.get_or_404(Question, id)
    return render_template(_j.show, entity=question, alternatives=alternatives, **properties)




@bp.route("/<int:id>/edit", methods=["GET"])
def edit(id):
    """
    Edit page.
    :return: The response.
    """
    print("edit")
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
    print("update")
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

