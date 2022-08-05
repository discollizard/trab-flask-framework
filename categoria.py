from build import db

class Categoria(db.Model):
    def __init__ (self, nome_categoria):
        self.nome_categoria = nome_categoria

    id_categoria = db.Column('id_categoria', db.Integer, primary_key=True)
    nome_categoria = db.Column('nome_categoria', db.String(45))
        
