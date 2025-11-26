import typer

from .clean.main import app as clean_app
from .migration.main import app as migration_app

app = typer.Typer()

app.add_typer(clean_app)
app.add_typer(migration_app)


if __name__ == "__main__":
    app()
