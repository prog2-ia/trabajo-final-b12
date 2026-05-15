# buscador.py

class Buscador:
    """
    Servicio de búsqueda sobre cualquier lista de objetos Multimedia.
    Principio de responsabilidad única (SRP): sólo sabe buscar.
    Recibe la biblioteca por parámetro → bajo acoplamiento.
    """

    def __init__(self, biblioteca):
        self._biblioteca = biblioteca  # referencia a la lista compartida

    # ── BÚSQUEDA GENERAL ─────────────────────────────────────────────────────

    def buscar(self, texto):
        """Busca por título o autor (insensible a mayúsculas)."""
        texto = texto.lower().strip()
        return [
            item for item in self._biblioteca
            if texto in item._titulo.lower() or texto in item._autor.lower()
        ]

    # ── BÚSQUEDA POR TIPO ────────────────────────────────────────────────────

    def buscar_por_tipo(self, tipo):
        """Filtra por clase. Uso: buscador.buscar_por_tipo(Cancion)"""
        return [item for item in self._biblioteca if isinstance(item, tipo)]

    # ── BÚSQUEDA POR GÉNERO / TEMA ────────────────────────────────────────────

    def buscar_por_genero(self, genero):
        """Busca canciones por género musical."""
        genero = genero.lower()
        return [
            item for item in self._biblioteca
            if hasattr(item, '_genero') and genero in item._genero.lower()
        ]

    def buscar_por_tema(self, tema):
        """Busca podcasts por tema."""
        tema = tema.lower()
        return [
            item for item in self._biblioteca
            if hasattr(item, '_tema') and tema in item._tema.lower()
        ]

    # ── BÚSQUEDA POR ARTISTA ──────────────────────────────────────────────────

    def buscar_por_artista(self, artista):
        """Busca por autor principal o colaborador."""
        artista = artista.lower()
        return [
            item for item in self._biblioteca
            if artista in item._autor.lower()
            or any(artista in c.lower() for c in item._colaboradores)
        ]

    # ── BÚSQUEDA POR DURACIÓN ─────────────────────────────────────────────────

    def buscar_por_duracion(self, min_seg=0, max_seg=float('inf')):
        """Devuelve elementos cuya duración está en [min_seg, max_seg] segundos."""
        return [
            item for item in self._biblioteca
            if min_seg <= item._duracion <= max_seg
        ]

    # ── UTILIDAD ──────────────────────────────────────────────────────────────

    def mostrar_resultados(self, resultados, etiqueta="Resultados"):
        if not resultados:
            print(f"\n🔍 No se encontraron resultados para '{etiqueta}'.")
            return
        print(f"\n🔍 {etiqueta} — {len(resultados)} encontrado(s):")
        print("-" * 40)
        for i, item in enumerate(resultados, 1):
            print(f"  {i}. {item._titulo} — {item._autor}")
        print("-" * 40)