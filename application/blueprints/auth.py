from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

from utils import mongo_db

login_manager = LoginManager()
bcrypt = Bcrypt()
blueprint = Blueprint(name="auth", import_name=__name__)


class User(UserMixin):
    def __init__(
        self, name: str, username: str, email: str, password: str, shops: list[str]
    ) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password
        self.shops = shops

    def get_id(self) -> str:
        """Override 'get_id' because User has no 'id' attribute"""
        return self.email

    def check_password(self, password: str) -> str:
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(email: str) -> User:
    user = mongo_db.get_user_by_email(email)
    return User(**user)


@blueprint.get("/")
def login_get():
    if current_user.is_authenticated:
        return redirect(
            url_for("get_articles", shop=current_user.shops[0], list_category="beer")
        )
    return render_template("login.html")


@blueprint.post("/")
def login_post():
    user_db = mongo_db.get_user_by_email(request.form["email"])
    if user_db is not None:
        user = User(**user_db)
        if not user.check_password(request.form["password"]):
            flash("Email ou mot de passe incorrect")
            return redirect(url_for("auth.login_get"))

        login_user(user)
        return redirect(
            url_for("get_articles", shop=current_user.shops[0], list_category="beer")
        )

    flash("Email ou mot de passe incorrect")
    return redirect(url_for("auth.login_get"))


@blueprint.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login_get"))
