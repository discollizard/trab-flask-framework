from build import db

class Pergunta(db.Model):
    def __init__ (self, usuario_id_usuario, anuncio_id_anuncio, texto):
        self.texto = texto
        self.usuario_id_usuario = usuario_id_usuario
        self.anuncio_id_anuncio = anuncio_id_anuncio
        
    id_pergunta = db.Column('id_pergunta', db.Integer, primary_key=True)
    usuario_id_usuario = db.Column('usuario_id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'))
    anuncio_id_anuncio = db.Column('anuncio_id_anuncio', db.Integer, db.ForeignKey('anuncio.id_anuncio'))
    texto = db.Column('texto', db.String(255))
