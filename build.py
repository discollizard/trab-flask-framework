from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from sql_config import user, database, server, password 

app = Flask(__name__)

# SETTING UP SQLALCHEMY PARAMETERS
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{server}:3306/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# INSTANTIATING DB HANDLER
db = SQLAlchemy(app)


# IMPORTING MODELS
import usuario
import categoria
import anuncio
import favorito
import compra
import pergunta
import resposta

# CREATING TABLES
db.create_all()



