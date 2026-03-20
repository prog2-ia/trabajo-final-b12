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
        icono = "👑 PRO" if self._es_pro else "💩 CUTRE"
        colabs = f" feat. {', '.join(self._colaboradores)}" if self._colaboradores else ""
        return (f"🎵 {self._titulo}{colabs} \n"
                f"   Artista : {self._autor}\n"
                f"   Género  : {self._genero}\n"
                f"   Calidad : {self._bitrate}kbps {self._canales} [{icono}]| {self._duracion} min")
