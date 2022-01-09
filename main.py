import os
from flask import Flask
from api.api import api
from database import create_database

create_database()

app = Flask(__name__)
SERVER_PORT = os.environ.get('SERVER_PORT')

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=SERVER_PORT)