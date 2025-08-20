from datetime import datetime

from flask import (
    Flask,
    send_file,
    redirect,
    render_template,
    request,
    Response,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

import auth
from config import configure
from pictures import download_picture

app = Flask(__name__, template_folder="./")
configure(app)
db = SQLAlchemy(app)


###########
# Models #
##########
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text())
    email = db.Column(db.String(80), unique=True, nullable=False)
    limited = db.Column(db.Boolean())
    name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(60))
    picture = db.Column(db.String(128))

    @classmethod
    def create(cls, *args, **kwargs) -> "User":
        user = cls(*args, **kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, **attrs) -> "User":
        for attr, value in attrs.items():
            setattr(self, attr, value)
        db.session.commit()
        return self


##########
# Routes #
##########
@app.route("/")
def index():
    user = User.query.filter_by(id=auth.get_user_id()).first()
    users = User.query.all()
    if user:
        return render_template(
            "directory.jinja2",
            title="Directory",
            current_user=user,
            users=users,
        )
    else:
        return redirect("/signin")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    user = None
    if request.method == "POST":
        # Check user
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user:
            if auth.check_password(
                password,
                user.password_hash,
                app.config.get("BCRYPT_SALT"),
            ):
                auth.set_user(user.id)
            else:
                flash(f"Incorrect password")
                user = None
        else:
            flash(f"User with {email} does not exist")

    if user:
        return redirect("/")
    return render_template(
        "./signin.jinja2",
        title="Sign In",
        alt_action="signup",
        alt_label="Sign Up",
    )


@app.route("/signout", methods=["GET"])
def signout():
    auth.set_user(None)
    flash("Successfully signed out")
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    user = None
    if request.method == "POST":
        # Create user first
        try:
            user = User.create(
                email=request.form.get("email"),
                bio=request.form.get("bio"),
                name=request.form.get("name"),
                password_hash=auth.hash_password(
                    request.form.get("password"),
                    app.config.get("BCRYPT_SALT"),
                ),
            )
        except IntegrityError:
            flash("Email already exists")
        else:
            # Run longer operations next
            user.update(
                limited=auth.check_limited(
                    user.email,
                    lookup_url=app.config.get("EMPLOYEE_API_URL"),
                ),
                picture=download_picture(
                    request.form.get("picture"),
                    pictures_dir=app.config.get("PICTURES_DIR"),
                ),
            )

            # Set user
            auth.set_user(user.id)

    if user:
        return redirect("/")
    else:
        return render_template(
            "./signup.jinja2",
            title="Sign Up",
            alt_action="signin",
            alt_label="Sign In",
        )


@app.route("/<path:path>")
def catch_all(path: str):
    """
    Serve static assets like favicion.ico

    :param path: asset path
    :return: file
    """
    return send_file(path)


##############
# Middleware #
##############
@app.context_processor
def set_context() -> dict:
    """Provide context for templates"""
    return {"now": datetime.utcnow()}


@app.after_request
def debug(response: Response) -> Response:
    """Trigger logic after a request"""
    app.logger.debug(
        "%s %s %s",
        request.remote_addr,
        request.url,
        request.values,
    )
    return response


db.create_all()
