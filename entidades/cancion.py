#cancion.py
from jinja2.nodes import Mul

from multimedia import Multimedia

class Cancion(Multimedia):
    def __init__(self, autor, colaboradores, duracion, portada, genero):
        super().__init__(autor, colaboradores, duracion, portada, genero)