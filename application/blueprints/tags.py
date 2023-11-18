from datetime import datetime
from operator import attrgetter
from pathlib import Path

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import login_required

from application.entities.tag import TagFile
from application.use_cases.tags import TagManager

blueprint = Blueprint(name="tags", import_name=__name__, url_prefix="/tags")

application_path = Path(__file__).resolve().parent.parent
tags_path = application_path / "templates" / "tags"
fonts_path = application_path / "static" / "fonts"


@blueprint.get("/create")
@login_required
def create_tags_view() -> str:
    repository = current_app.config["repository_provider"]()

    request_shop = request.args["shop"]
    current_shop = repository.get_shop_by_username(username=request_shop)

    articles = repository.get_articles()

    return render_template(
        "article_list_glob.html",
        current_shop=current_shop,
        articles=articles,
    )


@blueprint.post("/create")
@login_required
def create_tags():
    repository = current_app.config["repository_provider"]()

    shop_username = request.args["shop"]
    shop = repository.get_shop_by_username(username=shop_username)
    request_form = request.form.to_dict()

    TagManager.create(
        repository=repository,
        request_form=request_form,
        shop=shop,
        tags_path=tags_path,
        fonts_path=fonts_path,
    )

    return redirect(url_for("tags.create_tags_view", shop=shop.username))


@blueprint.get("/files")
@login_required
def list_tag_files() -> str:
    files_path = tags_path.glob("etiquette*.html")

    files = []
    for file in files_path:
        file_split = file.name.split("_")
        time = file_split[5].replace(".html", "").replace("-", ":")
        files.append(
            TagFile(
                id=file_split[2],
                type=file_split[1],
                shop=file_split[3],
                date=datetime.fromisoformat(f"{file_split[4]} {time}"),
                file=file.name,
            )
        )

    files = sorted(files, key=attrgetter("date", "id"))
    return render_template("tag_files_list.html", files=files)


@blueprint.get("/files/delete/<file>")
@login_required
def delete_tag_file(file: str):
    Path.unlink(tags_path / file)
    return redirect(request.referrer)


@blueprint.get("/files/<file>")
@login_required
def get_tag_file(file: str) -> str:
    return render_template(f"tags/{file}")
