from flask import render_template, redirect, flash, url_for, session, request


from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import check_password_hash

from flask_login import (
    login_user,
    logout_user,
    login_required,
)

from ..webapp import db, bcrypt
from ..models import User
from .forms import login_form, register_form


from . import bp

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

from wtforms import StringField, SubmitField, SelectField, IntegerField


@bp.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.jinja2", title="Home")


@bp.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                # In production, it is recommended to use a generic message
                flash("User not found", "danger")
            elif check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for("main.index"))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth/login.jinja2", form=form)


@bp.route("/profile/", methods=("GET", "POST"), strict_slashes=False)
def profile():
    return render_template("auth/profile.jinja2")


# Register route
@bp.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template(
        "auth/register.jinja2",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account",
    )


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))



# docs&Upload route/controllers ######################################################################

properties = {                                          # TODO: finish this
    "entity_name": "documento",
    "collection_name": "documentos",
    "list_fields": ["id", "student_id", "status", "title", "comments", "created_at", "updated_at"],
}


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])

@bp.route('/docs/', methods=['GET', 'POST'], strict_slashes=False)      # TODO: fix renderization to upload docs
def upload():
    form = PhotoForm()
    if request.method == 'POST' and 'photo' in request.files:
        print('form validated', request.form.get('photos'))

    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'photo', filename
        ))
        submit = SubmitField('Upload')
        return redirect(url_for('main'))

    docs_sent = db.session.query(User).filter(User.id == 1).first()
    
    return render_template("users/docs.jinja2", form=form, **properties) #, entities=docs_sent) #, docs_sent=docs_sent) ???


@bp.route("/test", methods=("GET", "POST"), strict_slashes=False)
def test_():
    """
    Test page.
    :return: test page.
    """
    print("url reachable: ok")
    
    return render_template("test_mfa.jinja2")
