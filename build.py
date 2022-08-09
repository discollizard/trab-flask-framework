from flask import (Flask, render_template, request, redirect)
from flask_login import (current_user,
LoginManager, login_user, logout_user, login_required)

from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from sql_config import user, database, server, password 

app = Flask('FastCompra')

# SETTING UP SQLALCHEMY PARAMETERS
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{server}:3306/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'paçoca'

# INSTANTIATING DB HANDLER
db = SQLAlchemy(app)

# INSTANTIATING LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


# IMPORTING MODELS
from usuario import Usuario
from categoria import Categoria
from anuncio import Anuncio
from favorito import Favorito
from compra import Compra
from pergunta import Pergunta
from resposta import Resposta

# PUTTING CATEGORIES INTO DATABASE ONLY FOR THE FIRST TIME RUNNING
queryAllCategoria = Categoria.query.all()
if len(queryAllCategoria) == 0:
    categorias = [
        'Eletronicos',
        'Vestuario',
        'Moveis',
        'Livros'
    ]
    for categoria in categorias:
        categoria = Categoria(categoria)
        db.session.add(categoria)
    db.session.commit()


# CREATING TABLES
db.create_all()



