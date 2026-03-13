#playlist.py

from agrupacion import Agrupacion

class Playlist(Agrupacion):
    def __init__(self, creador, nombre, estado):
        super().__init__(creador, nombre)
        self.estado = estado

