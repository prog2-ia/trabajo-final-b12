#cancion.py
from jinja2.nodes import Mul

from audio import Audio

class Cancion(Audio):
    def __init__(self, titulo, autor, colaboradores, duracion, portada, bitrate_archivo, genero):
        self._genero = genero
        # Aqui colaboradores influyen en los Royalties
        self._es_pro = True

        if bitrate_archivo < 64:
            raise ValueError("Calidad insuficiente para ser procesada en Spotify.")

        if bitrate_archivo < 192:
            print(f"⚠️ ¡Aviso! '{titulo}' tiene un bitrate de {bitrate_archivo}. Es calidad cutre.")
            self._es_pro = False

        super().__init__(titulo, autor, colaboradores, duracion, portada, bitrate=bitrate_archivo, canales='Estéreo')

    def reproducir(self):
        # Aquí escribimos el "CÓMO reproducir" específico para canciones
        # A una mayor calidad de audio que un podcast por eficiencia
        print(f'Reproduciendo MP3: {self._titulo} de {self._autor}...')

    def __str__(self):
        # Si es pro, le ponemos una corona, si no, nada.
        icono = "👑 PRO" if self._es_pro else "💩 CUTRE"
        return f"{self._titulo} {icono} - {self._bitrate}kbps"
