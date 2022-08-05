from build import db

class Compra(db.Model):
    def __init__ (self, data_e_hora, qtd_comprada):
        self.data_e_hora = data_e_hora
        self.qtd_comprada = qtd_comprada
        
    usuario_id_usuario = db.Column('usuario_id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True)
    anuncio_id_anuncio = db.Column('anuncio_id_anuncio', db.Integer, db.ForeignKey('anuncio.id_anuncio'), primary_key=True)
    data_e_hora = db.Column('data_e_hora', db.DateTime)
    qtd_comprada = db.Column('qtd_comprada', db.Integer)
