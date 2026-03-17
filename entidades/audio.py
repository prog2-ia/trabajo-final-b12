#audio.py

from multimedia import Multimedia

class Audio(Multimedia):
    def __init__(self, titulo, autor, colaboradores, duracion, portada, bitrate, canales):
        super().__init__(titulo, autor, colaboradores, duracion, portada, )
        self._bitrate= bitrate
        self._canales  = canales

    def optimizar_para_movil(self):
        # Si el audio es muy pesado, lo bajamos por software
        if self._bitrate > 128:
            print(f"Bajando calidad de {self._bitrate} a 128kbps para ahorrar datos...")
            self._bitrate = 128