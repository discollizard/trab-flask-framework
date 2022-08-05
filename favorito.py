from build import db

class Favorito(db.Model):

    usuario_id_usuario = db.Column('usuario_id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True)
    anuncio_id_anuncio = db.Column('anuncio_id_anuncio', db.Integer, db.ForeignKey('anuncio.id_anuncio'), primary_key=True)
