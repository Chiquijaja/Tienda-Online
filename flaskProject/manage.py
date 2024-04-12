from app.views import app
from db import dbhelper


@app.cli.command()
def create_tables():
    dbhelper.create_tables()

@app.cli.command()
def load_data():
    dbhelper.load_data()


if __name__ == '__main__':
    app.run()
