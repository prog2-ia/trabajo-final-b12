# cancion.py

from entidades.audio import Audio


# ── EXCEPCIÓN PERSONALIZADA ───────────────────────────────────────────────────
class CalidadInsuficienteError(ValueError):
    """
    Excepción propia del dominio Spotify — hereda de ValueError porque
    es un error de valor (el bitrate), pero con un nombre específico
    que identifica exactamente qué ha fallado en nuestro negocio.
    Temario T07: excepciones personalizadas heredando de Exception.
    """

    def __init__(self, bitrate, minimo=64):
        # Llamamos al constructor del padre con un mensaje descriptivo
        super().__init__(
            f"Bitrate {bitrate}kbps insuficiente. "
            f"Mínimo aceptado por Spotify: {minimo}kbps."
        )
        self.bitrate = bitrate  # guardamos el valor para quien capture el error


# ── clase principal───────────────────────────────────────────────────
class Cancion(Audio):
    """
    Representa una canción en el sistema.
    Hereda de Audio (que hereda de Multimedia) — tercer nivel de la jerarquía.
    Añade concepto de calidad PRO/CUTRE y género musical.
    """

    # Atributo de CLASE — compartido por todas las instancias
    # Temario T03: diferencia entre atributo de clase y de instancia
    BITRATE_MINIMO = 64
    BITRATE_PRO = 192

    def __init__(self, titulo, autor, colaboradores, duracion, portada, bitrate_archivo, genero):
        # Asignamos antes del super() porque queremos que existan
        # aunque el super() falle (orden defensivo)
        self._genero = genero
        self._es_pro = True  # optimista por defecto, se corrige abajo

        # ── Validaciones de negocio ───────────────────────────────────────────
        # Usamos nuestro @staticmethod para no duplicar la lógica de validación
        if not Cancion.es_bitrate_valido(bitrate_archivo):
            # Lanzamos nuestra excepción personalizada en vez de ValueError genérico
            raise CalidadInsuficienteError(bitrate_archivo, Cancion.BITRATE_MINIMO)

        if bitrate_archivo < Cancion.BITRATE_PRO:
            # Aviso sin bloquear — la canción entra pero marcada como cutre
            print(f"⚠️  '{titulo}' tiene {bitrate_archivo}kbps. Calidad cutre.")
            self._es_pro = False

        # Llamamos al constructor de Audio pasando los parámetros que él necesita
        # canales siempre es Estéreo en canciones (a diferencia de Podcast que es Mono)
        super().__init__(titulo, autor, colaboradores, duracion, portada,
                         bitrate=bitrate_archivo, canales='Estéreo')

    # ── CONSTRUCTOR ALTERNATIVO ───────────────────────────────────────────────
    @classmethod
    def desde_dict(cls, datos):
        """
        Constructor alternativo — crea una Cancion desde un diccionario.
        Temario T04: @classmethod con cls como primer parámetro.
        Útil para instanciar desde catalogo.py sin desempaquetar a mano.

        Uso:
            datos = {"titulo": "Blinding Lights", "autor": "The Weeknd", ...}
            cancion = Cancion.desde_dict(datos)
        """
        return cls(
            titulo=datos["titulo"],
            autor=datos["autor"],
            colaboradores=datos.get("colaboradores", []),  # .get() evita KeyError
            duracion=datos["duracion"],
            portada=datos.get("portada", "default.jpg"),
            bitrate_archivo=datos["bitrate"],
            genero=datos["genero"]
        )

    # ── MÉT ESTÁTICO ───────────────────────────────────────────────────────
    @staticmethod
    def es_bitrate_valido(bitrate):
        """
        Valida si un bitrate es suficiente para ser procesado.
        Temario T04: @staticmethod — no necesita self ni cls porque
        es lógica pura que no depende del estado del objeto.
        Se puede llamar sin instanciar: Cancion.es_bitrate_valido(128)
        """
        return isinstance(bitrate, int) and bitrate >= Cancion.BITRATE_MINIMO

    # ── MÉTODOS ESPECIALES ────────────────────────────────────────────────────
    def __len__(self):
        """
        Protocolo de secuencia — Temario T06: __len__ para len().
        len(cancion) devuelve la duración en segundos.
        Tiene sentido semántico: 'cuánto ocupa/dura este objeto'.
        """
        return int(self._duracion)

    def __repr__(self):
        """
        Representación formal para el desarrollador — Temario T04.
        Diferente de __str__: esta debería permitir recrear el objeto.
        Se ve en la consola interactiva o en listas de objetos.
        """
        return (f"Cancion("
                f"titulo={self._titulo!r}, "
                f"autor={self._autor!r}, "
                f"genero={self._genero!r}, "
                f"duracion={self._duracion!r}, "
                f"bitrate={self._bitrate!r}, "
                f"es_pro={self._es_pro!r})")

    def __str__(self):
        """
        Representación informal para el usuario — lo que ve en pantalla.
        Llama a los atributos protegidos heredados de Audio y Multimedia.
        """
        icono = "👑 PRO" if self._es_pro else "💩 CUTRE"
        colabs = f" feat. {', '.join(self._colaboradores)}" if self._colaboradores else ""
        return (f"🎵 {self._titulo}{colabs}\n"
                f"   Artista : {self._autor}\n"
                f"   Género  : {self._genero}\n"
                f"   Calidad : {self._bitrate}kbps {self._canales} [{icono}] | {self._duracion} min")

    # ── MÉTODOS DE INSTANCIA ──────────────────────────────────────────────────
    def reproducir(self):
        """
        Implementación concreta del métod abstracto de Multimedia.
        Polimorfismo: Cancion reproduce distinto a Podcast aunque
        el reproductor llame a reproducir() sin saber el tipo.
        """
        print(f"▶  Reproduciendo MP3: {self._titulo} — {self._autor}  [{self._bitrate}kbps]")
