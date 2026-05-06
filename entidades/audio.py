#audio.py

from entidades.multimedia import Multimedia

class Audio(Multimedia):
    def __init__(self, titulo, autor, colaboradores, duracion, portada, bitrate, canales):
        super().__init__(titulo, autor, colaboradores, duracion, portada, )
        self._bitrate= bitrate
        self._canales  = canales

        # ── PROPERTY: bitrate gestionado ──────────────────────────────────────────
    @property
    def bitrate(self):
        """Getter — permite leer el bitrate con objeto.bitrate"""
        return self._bitrate
    @bitrate.setter
    def bitrate(self, nuevo_bitrate):
        """
        Setter — valida antes de asignar.
        El @property convierte objeto.bitrate = x en una llamada aquí,
        así nunca se puede poner un bitrate absurdo desde fuera.
        """
        if not isinstance(nuevo_bitrate, int):
            raise TypeError("El bitrate debe ser un número entero.")
        if nuevo_bitrate < 32:
            raise ValueError(f"Bitrate {nuevo_bitrate}kbps demasiado bajo. Mínimo 32kbps.")
        if nuevo_bitrate > 320:
            raise ValueError(f"Bitrate {nuevo_bitrate}kbps no existe en estándares MP3.")
        self._bitrate = nuevo_bitrate
    # ── MÉTODOS ESPECIALES ────────────────────────────────────────────────────
    def __repr__(self):
        """
            Representación formal para el desarrollador.
            Audio añade bitrate y canales que Multimedia no conoce,
            por eso necesita su propio __repr__ en vez de heredar el de arriba.
            """
        colabs = self._colaboradores if self._colaboradores else []
        return (f"{type(self).__name__}("
                f"titulo={self._titulo!r}, "
                f"autor={self._autor!r}, "
                f"duracion={self._duracion!r}, "
                f"bitrate={self._bitrate!r}, "
                f"canales={self._canales!r}, "
                f"colaboradores={colabs!r})")

    def __iadd__(self, segundos):
        """
        Operador += para sumar duración al audio.
        Permite hacer: cancion += 30  (añade 30 segundos)
        __iadd__ es el operador de asignación aumentada del temario.
        Devuelve self para que la variable siga apuntando al mismo objeto.
        """
        if not isinstance(segundos, (int, float)):
            raise TypeError("Solo puedes sumar segundos (número).")
        self._duracion += segundos
        return self  # <- obligatorio en __iadd__, si no la variable queda como None

    def optimizar_para_movil(self):
        # Si el audio es muy pesado, lo bajamos por software
        if self._bitrate > 128:
            print(f"Bajando calidad de {self._bitrate} a 128kbps para ahorrar datos...")
            self._bitrate = 128

    # Añadir en audio.py
    def __str__(self):
        base = super().__str__()  # reutiliza el de Multimedia
        return f"{base} | {self._bitrate}kbps {self._canales}"