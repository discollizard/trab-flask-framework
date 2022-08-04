from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# -- LOGIN E CADASTRO -- 
@app.route("/login")
def pag_login():
    return render_template("login.html")

@app.route("/login/submit")
def login():
    print("logar")
    return ""

@app.route("/cad/usuario")
def pag_cad_usuario():
    return render_template("cad_usuario.html")

@app.route("/cad/usuario/submit")
def cad_usuario():
    print("usuario cadastrado")
    return ""

# -- ANUNCIOS --

@app.route("/cad/anuncios")
def pag_anunciar():
    return render_template("cad_anuncio.html")

@app.route("/cad/anuncios/criar")
def anunciar():
    print("anuncio criado")
    return ""

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
