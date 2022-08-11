from build import db

class Favorito(db.Model):

    def __init__ (self, usuario_id_usuario, anuncio_id_anuncio):
        self.usuario_id_usuario = usuario_id_usuario
        self.anuncio_id_anuncio = anuncio_id_anuncio

    usuario_id_usuario = db.Column('usuario_id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True)
    anuncio_id_anuncio = db.Column('anuncio_id_anuncio', db.Integer, db.ForeignKey('anuncio.id_anuncio'), primary_key=True)
