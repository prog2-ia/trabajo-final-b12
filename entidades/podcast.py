#podcast.py
from jinja2.nodes import Mul

from multimedia import Multimedia

class Podcast(Audio):
    def __init__(self, autor, colaboradores, duracion, portada, bitrate_archivo, tema):
        bitratef=98 if bitrate_archivo>98 else bitrate_archivo
        self._tema = tema # separacion entre tema y genero por facilitar al buscador
        super().__init__(autor, colaboradores, duracion, portada, bitrate = bitratef, canales='Mono')
        # Aqui colaboradores influyen en lel titulo por el SEO

    def __str__(self):
        # Lógica de SEO: Si hay colaboradores, los ponemos en el nombre
        invitados = f" (con {', '.join(self._colaboradores)})" if self._colaboradores else ""

        return (f"🎙️ PODCAST [{self._tema}]\n"
                f"Episodio: {self._titulo}{invitados}\n"
                f"Autor: {self._autor}\n"
                f"Calidad: {self._bitrate}kbps (Optimizado)")

    def reproducir(self):
        # Usamos el título con SEO para el mensaje de reproducción
        print(f"Reproduciendo el podcast de {self._tema}: '{self._titulo}'...")