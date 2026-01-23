import typer

from scripts.clean.main import app as clean_app
from scripts.migration.main import app as migration_app
from scripts.tactill.main import app as tactill_app

app = typer.Typer()

app.add_typer(clean_app)
app.add_typer(migration_app)
app.add_typer(tactill_app, name="tactill")


if __name__ == "__main__":
    app()
