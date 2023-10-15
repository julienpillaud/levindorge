import functools
from enum import Enum
from typing import Any, Callable, ParamSpec, TypeVar

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_bcrypt import Bcrypt
from flask_login import (
    AnonymousUserMixin,
    LoginManager,
    UserMixin,
    current_user,
    login_user,
    logout_user,
)

bcrypt = Bcrypt()
blueprint = Blueprint(name="auth", import_name=__name__)

P = ParamSpec("P")
T = TypeVar("T")


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class User(UserMixin):
    def __init__(
        self,
        name: str,
        username: str,
        email: str,
        password: str,
        role: Role,
        shops: list[str],
    ) -> None:
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password
        self.role = role
        self.shops = shops

    def get_id(self) -> str:
        """Override 'get_id' because User has no 'id' attribute"""
        return self.email

    def check_password(self, password: str) -> str:
        return bcrypt.check_password_hash(self.password_hash, password)


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.name = "Demo"
        self.shops = ["angouleme", "pessac", "sainte-eulalie"]


login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(email: str) -> User:
    repository = current_app.config["repository_provider"]()
    user = repository.get_user_by_email(email)

    return User(**user)


def admin_required(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        if current_user.role not in {"admin", "superuser"}:
            return login_manager.unauthorized()
        return func(*args, **kwargs)

    return wrapper


@blueprint.get("/")
def login_get():
    if current_user.is_authenticated:
        return redirect(
            url_for(
                "articles.get_articles",
                shop=current_user.shops[0],
                list_category="beer",
            )
        )
    return render_template("login.html")


@blueprint.post("/")
def login_post():
    repository = current_app.config["repository_provider"]()
    user_db = repository.get_user_by_email(request.form["email"])
    if user_db is not None:
        user = User(**user_db)
        if not user.check_password(request.form["password"]):
            flash("Email ou mot de passe incorrect")
            return redirect(url_for("auth.login_get"))

        login_user(user)
        return redirect(
            url_for(
                "articles.get_articles",
                list_category="beer",
                shop=current_user.shops[0],
            )
        )

    flash("Email ou mot de passe incorrect")
    return redirect(url_for("auth.login_get"))


@blueprint.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login_get"))
