import typer

from scripts.clean.main import app as clean_app
from scripts.migration.main import app as migration_app

app = typer.Typer()

app.add_typer(clean_app)
app.add_typer(migration_app)


if __name__ == "__main__":
    app()
