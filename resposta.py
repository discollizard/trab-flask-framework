from build import db

class Resposta(db.Model):
    def __init__ (self, pergunta_id_pergunta, texto):
        self.pergunta_id_pergunta = pergunta_id_pergunta
        self.texto = texto
        
    id_resposta = db.Column('id_resposta', db.Integer, primary_key=True)
    pergunta_id_pergunta = db.Column('pergunta_id_pergunta', db.Integer, db.ForeignKey('pergunta.id_pergunta'))
    texto = db.Column('texto', db.Integer)
