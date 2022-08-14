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

import hashlib

# -- PÁGINAS INICIAL E DE ERRO --
@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("not_found.html")

# -- LOGIN E OPERAÇÕES DE USUÁRIO -- 
@app.route("/login")
def pag_login():
    return render_template("login.html")

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/login/submit", methods=['POST'])
def login():
    email = request.form.get('email')
    hash = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
    user = Usuario.query.filter_by(email=email, senha=hash).first()

    if(user):
        login_user(user)
        return redirect(url_for('pag_home'))
    else:
        return redirect(url_for('pag_login'))

    return request.form

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/cad/usuario")
def pag_cad_usuario():
    return  render_template('cad_usuario.html')

@app.route("/opcoes-usuario")
@login_required
def opcoes_usuario():
    user = current_user
    return  render_template('opt_usuario.html', user=user)

@app.route("/alt/usuario", methods=['POST'])
def alt_usuario():
    user = current_user
    hash = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
    user.nome = request.form.get('nome')
    user.email = request.form.get('email')
    user.senha = hash
    db.session.commit()
    return redirect(url_for('pag_home', mensagem_sucesso='Dados cadastrais alterados.'))

@app.route("/del/usuario")
def del_usuario():
    todos_anuncios_deste_usuario = Anuncio.query.filter_by(id_usuario=current_user.id_usuario)
    todos_favoritos_deste_usuario = Favorito.__table__.delete().where(Favorito.usuario_id_usuario==current_user.id_usuario)
    user = current_user
    for anuncio in todos_anuncios_deste_usuario:
        deletar_anuncio(anuncio.id_anuncio)
    todas_perguntas_deste_usuario = Pergunta.query.filter_by(usuario_id_usuario=current_user.id_usuario)
    for pergunta in todas_perguntas_deste_usuario:
        respostas_desta_pergunta = Resposta.__table__.delete().where(Resposta.pergunta_id_pergunta==pergunta.id_pergunta)
        db.session.execute(respostas_desta_pergunta)
    perguntas_para_deletar = Pergunta.__table__.delete().where(Pergunta.usuario_id_usuario == current_user.id_usuario)
    db.session.execute(perguntas_para_deletar)
    anuncio_para_deletar = Anuncio.__table__.delete().where(Anuncio.id_usuario==current_user.id_usuario)
    db.session.execute(anuncio_para_deletar)
    db.session.execute(todos_favoritos_deste_usuario)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
    

@app.route("/cad/usuario/submit", methods=['POST'])
def cad_usuario():
    hash = hashlib.sha512(str(request.form.get('senha')).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get('nome'), request.form.get('email'), hash)
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('pag_login'))

# -- HOME --
@app.route("/home")
@login_required
def pag_home():
    todos_anuncios = Anuncio.query\
    .join(Categoria, Anuncio.id_categoria == Categoria.id_categoria)\
    .add_columns(Categoria.nome_categoria)\
    .group_by(Anuncio.id_anuncio)\
    .all()
    if 'mensagem_sucesso' in request.args:
        return render_template("home.html", mensagem_sucesso=request.args['mensagem_sucesso'], id_usuario=1, anuncios=todos_anuncios)
    return render_template("home.html", id_usuario=1, anuncios=todos_anuncios)

# -- ANUNCIOS --

@app.route("/cad/anuncios")
@login_required
def pag_anunciar():
    categorias = Categoria.query.all()
    return render_template("cad_anuncio.html", categorias=categorias)

@app.route("/alt/anuncio/<id_anuncio>")
@login_required
def pag_alterar_anuncio(id_anuncio):
    categorias = Categoria.query.all()
    anuncio_para_alterar = Anuncio.query.filter_by(id_anuncio=id_anuncio).first()
    return render_template("alt_anuncio.html", categorias=categorias, anuncio=anuncio_para_alterar)

@app.route("/alt/anuncio/submit", methods=['POST'])
@login_required
def alterar_anuncio():
    anuncio_para_alterar = Anuncio.query.filter_by(
        id_anuncio=request.form.get('id_anuncio')
    ).first()
    anuncio_para_alterar.nome_produto=request.form.get('nome')
    anuncio_para_alterar.qtd_disponivel=request.form.get('qtd')
    anuncio_para_alterar.preco_produto=request.form.get('preco')
    anuncio_para_alterar.id_categoria = request.form.get('categoria')
    db.session.commit()
    return redirect(url_for("pag_home", mensagem_sucesso="Anúncio alterado com sucesso"))

@app.route("/cad/anuncios/submit", methods=['POST'])
@login_required
def anunciar():
    anuncio = Anuncio(
        request.form.get('nome'),
        request.form.get('preco'),
        request.form.get('qtd'),
        request.form.get('categoria'),
        current_user.id_usuario
    )
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for("pag_home", mensagem_sucesso="Anúncio cadastrado com sucesso"))

@app.route("/del/anuncio/<id_anuncio>")
@login_required
def deletar_anuncio(id_anuncio):
    todos_favoritos_deste_anuncio = Favorito.__table__.delete().where(Favorito.anuncio_id_anuncio==id_anuncio)
    todas_perguntas_deste_anuncio = Pergunta.query.filter_by(anuncio_id_anuncio=id_anuncio)
    for pergunta in todas_perguntas_deste_anuncio:
        respostas_desta_pergunta = Resposta.__table__.delete().where(Resposta.pergunta_id_pergunta==pergunta.id_pergunta)
        db.session.execute(respostas_desta_pergunta)
    perguntas_para_deletar = Pergunta.__table__.delete().where(Pergunta.anuncio_id_anuncio == id_anuncio)
    db.session.execute(perguntas_para_deletar)
    anuncio_para_deletar = Anuncio.query.filter_by(id_anuncio=id_anuncio).first()
    db.session.execute(todos_favoritos_deste_anuncio)
    db.session.delete(anuncio_para_deletar)
    db.session.commit()
    return redirect(url_for("pag_home", mensagem_sucesso="Anúncio deletado com sucesso"))

@app.route("/anuncio/<anuncio_id>")
@login_required
def pag_anuncio_por_id(anuncio_id):
    anuncio_para_mostrar = Anuncio.query.filter_by(id_anuncio=anuncio_id).first()
    perguntas_do_anuncio = Pergunta.query.filter_by(anuncio_id_anuncio=anuncio_id)\
    .join(Usuario, Pergunta.usuario_id_usuario == Usuario.id_usuario)\
    .add_columns(Usuario.nome)
    for pergunta in perguntas_do_anuncio:
        pergunta[0].respostas = Resposta.query.filter_by(pergunta_id_pergunta=pergunta[0].id_pergunta)
    mostrar_opcoes_do_dono = current_user.id_usuario == anuncio_para_mostrar.id_usuario
    return render_template("anuncio.html", anuncio=anuncio_para_mostrar, perguntas=perguntas_do_anuncio, mostrar_opcoes_do_dono=mostrar_opcoes_do_dono)

@app.route("/perguntar", methods=['POST'])
@login_required
def perguntar():
    pergunta = request.form.get('pergunta') 
    id_anuncio = request.form.get('id_anuncio') 
    nova_pergunta = Pergunta(current_user.id_usuario, id_anuncio, pergunta)
    db.session.add(nova_pergunta)
    db.session.commit()
    return redirect(url_for("pag_anuncio_por_id", anuncio_id = id_anuncio))

@app.route("/deletar/<id_anuncio>/pergunta/<id_pergunta>")
@login_required
def deletar_pergunta(id_anuncio, id_pergunta):
    respostas_para_deletar = Resposta.__table__.delete().where(Resposta.pergunta_id_pergunta==id_pergunta)
    pergunta_para_deletar = Pergunta.query.filter_by(id_pergunta=id_pergunta).first()
    db.session.execute(respostas_para_deletar)
    db.session.delete(pergunta_para_deletar)
    db.session.commit()
    return redirect(url_for("pag_anuncio_por_id", anuncio_id = id_anuncio))


@app.route("/responder", methods=['POST'])
@login_required
def responder():
    id_pergunta = request.form.get('id_pergunta')
    resposta = request.form.get('resposta')
    id_anuncio = request.form.get('id_anuncio') 
    nova_resposta = Resposta(id_pergunta, resposta)
    db.session.add(nova_resposta)
    db.session.commit()
    return redirect(url_for("pag_anuncio_por_id", anuncio_id = id_anuncio))

@app.route("/deletar/<id_anuncio>/resposta/<id_resposta>")
@login_required
def deletar_resposta(id_anuncio, id_resposta):
    resposta_para_deletar = Resposta.query.filter_by(id_resposta=id_resposta).first()
    db.session.delete(resposta_para_deletar)
    db.session.commit()
    return redirect(url_for("pag_anuncio_por_id", anuncio_id = id_anuncio))



@app.route("/comprar/<id_anuncio>")
@login_required
def comprar(id_anuncio):
    anuncio_para_remover_qtd = Anuncio.query.filter_by(id_anuncio=id_anuncio).first()
    anuncio_para_remover_qtd.qtd_disponivel = anuncio_para_remover_qtd.qtd_disponivel - 1 
    nova_compra = Compra(current_user.id_usuario, id_anuncio)
    db.session.add(nova_compra)
    db.session.commit()
    return redirect(url_for("pag_home", mensagem_sucesso="Compra efetuada com sucesso"))

@app.route("/favoritar/<id_anuncio>")
@login_required
def favoritar(id_anuncio):
    try:
        novo_favorito = Favorito(current_user.id_usuario, id_anuncio)
        db.session.add(novo_favorito)
        db.session.commit()
    finally:
        return redirect(url_for('favoritos'))

@app.route("/favoritos")
@login_required
def favoritos():
    anuncios_favoritos = Anuncio.query\
    .join(Categoria, Categoria.id_categoria == Categoria.id_categoria)\
    .join(Favorito, Favorito.anuncio_id_anuncio == Anuncio.id_anuncio)\
    .filter(Favorito.usuario_id_usuario == current_user.id_usuario)\
    .add_columns(Categoria.nome_categoria)\
    .group_by(Anuncio.id_anuncio)\
    .all()
    return render_template("favoritos.html", anuncios=anuncios_favoritos) 

@app.route("/favoritos/<id_anuncio>/deletar")
@login_required
def deletar_favorito(id_anuncio):
    favorito_para_deletar = Favorito.query.filter_by(usuario_id_usuario=current_user.id_usuario, anuncio_id_anuncio=id_anuncio).first()
    db.session.delete(favorito_para_deletar)
    db.session.commit()
    return redirect(url_for('favoritos'))

@app.route("/relatorios/vendas")
@login_required
def pag_relatorios_venda():
    vendas = Compra.query\
    .join(Anuncio, Anuncio.id_anuncio == Compra.anuncio_id_anuncio)\
    .join(Usuario, Usuario.id_usuario == Compra.usuario_id_usuario)\
    .filter(Anuncio.id_usuario == current_user.id_usuario)\
    .add_columns(Usuario.nome, Anuncio.nome_produto)\
    .all()

    return render_template("relatorio_venda.html", dados=vendas)

@app.route("/relatorios/compras")
@login_required
def pag_relatorios_compra():
    compras = Compra.query\
    .join(Anuncio, Anuncio.id_anuncio == Compra.anuncio_id_anuncio)\
    .join(Usuario, Usuario.id_usuario == Anuncio.id_usuario)\
    .filter(Compra.usuario_id_usuario == current_user.id_usuario)\
    .add_columns(Usuario.nome, Anuncio.nome_produto)\
    .all()
    return render_template("relatorio_compra.html", compras=compras)
