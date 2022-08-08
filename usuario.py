from build import db

class Usuario(db.Model):
    def __init__ (self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String(45))
    senha = db.Column('senha', db.String(255))
    email = db.Column('email', db.String(90))

    def is_authenticated(self):
        return true
    def is_active(self):
        return true
    def is_anonymous(self):
        return true
    def get_id(self):
        return str(self.id_usuario)
