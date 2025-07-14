import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine

from app.infrastructure import Repository
from app.presentation import Controller

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


app = Flask(__name__)

load_dotenv()
engine = create_engine(os.getenv("DB_DSN"))
repository = Repository(engine)
controller = Controller(repository)

app.register_blueprint(controller.blueprint)


if __name__ == "__main__":
    app.run()
