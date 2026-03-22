#podcast.py

from entidades.audio import Audio

class Podcast(Audio):
    def __init__(self, titulo, autor, colaboradores, duracion, portada, bitrate_archivo, tema):
        bitratef=98 if bitrate_archivo>98 else bitrate_archivo
        self._tema = tema # separacion entre tema y genero por facilitar al buscador
        super().__init__(titulo, autor, colaboradores, duracion, portada, bitrate = bitratef, canales='Mono')
        # Aqui colaboradores influyen en lel titulo por el SEO

    def __str__(self):
        invitados = f" (con {', '.join(self._colaboradores)})" if self._colaboradores else ""
        return (f"🎙️ {self._titulo}{invitados} [PODCAST]\n"
                f"   Tema    : {self._tema}\n"
                f"   Autor   : {self._autor}\n"
                f"   Calidad : {self._bitrate}kbps {self._canales} | {self._duracion} min")

    def reproducir(self):
        # Usamos el título con SEO para el mensaje de reproducción
        print(f"Reproduciendo el podcast de {self._tema}: '{self._titulo}'...")