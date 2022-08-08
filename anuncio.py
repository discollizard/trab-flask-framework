from build import db

class Anuncio(db.Model):
    def __init__ (self, nome_produto, preco_produto, qtd_disponivel, id_categoria):
        self.nome_produto = nome_produto
        self.preco_produto = preco_produto
        self.qtd_disponivel = qtd_disponivel
        self.id_categoria = id_categoria
        self.id_usuario = 1

    id_anuncio = db.Column('id_anuncio', db.Integer, primary_key=True)
    nome_produto = db.Column('nome_produto', db.String(45))
    preco_produto = db.Column('preco_produto', db.Float)
    qtd_disponivel = db.Column('qtd_disponivel', db.Integer)
    id_categoria = db.Column('id_categoria', db.Integer, db.ForeignKey('categoria.id_categoria'))
    id_usuario = db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'))
