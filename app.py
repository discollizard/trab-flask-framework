from build import app, db, login_manager
from flask import (Flask, render_template, request, redirect, url_for)
from flask_login import (current_user,
LoginManager, login_user, logout_user, login_required)

# IMPORTING MODELS
from usuario import Usuario
from categoria import Categoria
from anuncio import Anuncio
from favorito import Favorito
from compra import Compra
from pergunta import Pergunta
from resposta import Resposta

# -- PÁGINAS INICIAL E DE ERRO --
@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("not_found.html")

# -- LOGIN E CADASTRO -- 
@app.route("/login")
def pag_login():
    return render_template("login.html")

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/login/submit", methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    user = Usuario.query.filter_by(email=email, senha=senha).first()

    if(user):
        login_user(user)
        return redirect(url_for('pag_home'))
    else:
        return redirect(url_for('pag_login'))

    return request.form

@app.route("/logout/<id_usuario>")
def logout(id_usuario):
    print(id_usuario)
    return "123"

@app.route("/cad/usuario")
def pag_cad_usuario():
    return  render_template('cad_usuario.html')

@app.route("/cad/usuario/submit", methods=['POST'])
def cad_usuario():
    usuario = Usuario(request.form.get('nome'), request.form.get('email'), request.form.get('senha'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('pag_login'))

# -- HOME --
@app.route("/home")
def pag_home():
    if 'mensagem_sucesso' in request.args:
        return render_template("home.html", mensagem_sucesso=request.args['mensagem_sucesso'], id_usuario=1)
    return render_template("home.html", id_usuario=1)

# -- ANUNCIOS --

@app.route("/cad/anuncios")
def pag_anunciar():
    categorias = Categoria.query.all()
    return render_template("cad_anuncio.html", categorias=categorias)

@app.route("/cad/anuncios/submit", methods=['POST'])
def anunciar():
    anuncio = Anuncio(
        request.form.get('nome'),
        request.form.get('preco'),
        request.form.get('qtd'),
        request.form.get('categoria')
    )
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for("pag_home", mensagem_sucesso="Anúncio cadastrado com sucesso"))

@app.route("/anuncios")
def pag_anuncios_por_categoria():
    return render_template("anuncios_por_categoria.html")

@app.route("/anuncio/<anuncio_id>")
def pag_anuncio_por_id():
    return render_template("anuncio.html")

@app.route("/anuncios/<anuncio_id>/perguntar")
def perguntar():
    print("perguntado")
    return render_template("anuncio.html")

@app.route("/anuncios/<anuncio_id>/responder")
def responder():
    print("respondido")
    return render_template("anuncio.html")

@app.route("/anuncios/<anuncio_id>/favoritos")
def favoritar():
    print("produto adicionado aos favoritos")
    return ""

@app.route("/anuncios/compra")
def comprar():
    print("produto comprado")
    return ""

@app.route("/favoritos")
def favoritos():
   return render_template("favoritos.html") 

@app.route("/relatorios/vendas")
def pag_relatorios_venda():
    return render_template("relatorio_venda.html")

@app.route("/relatorios/compras")
def pag_relatorios_compra():
    return render_template("relatorio_compra.html")
