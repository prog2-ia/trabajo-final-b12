#album.py

from agrupacion import Agrupacion

class Album(Agrupacion):
    def __init__(self, creador, nombre):
        super().__init__(creador, nombre)