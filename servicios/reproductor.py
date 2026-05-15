# reproductor.py

class Reproductor:
    """
    Servicio de reproducción con cola.
    Sigue SRP: sólo gestiona qué suena y en qué orden.
    """

    def __init__(self):
        self.cola_reproduccion = []
        self.pista_actual = None
        self._reproduciendo = False

    # ── CARGA Y REPRODUCCIÓN ──────────────────────────────────────────────────

    def cargar_pista(self, contenido):
        """Carga y reproduce inmediatamente una pista."""
        self.pista_actual = contenido
        self._reproduciendo = True
        contenido.reproducir()
        return self

    def agregar_a_cola(self, contenido):
        self.cola_reproduccion.append(contenido)
        print(f"➕ Añadido a la cola: {contenido._titulo}")
        return self

    def siguiente(self):
        """Avanza a la siguiente pista de la cola."""
        if self.cola_reproduccion:
            self.pista_actual = self.cola_reproduccion.pop(0)
            self._reproduciendo = True
            self.pista_actual.reproducir()
            return self.pista_actual
        print("⏹️  Fin de la cola de reproducción.")
        self._reproduciendo = False
        self.pista_actual = None
        return None

    def ver_cola(self):
        """Muestra el estado actual del reproductor."""
        print("\n" + "=" * 40)
        print("  🎧 REPRODUCTOR")
        print("=" * 40)
        if self.pista_actual:
            print(f"  ▶  Ahora: {self.pista_actual._titulo} — {self.pista_actual._autor}")
        else:
            print("  ⏹️  Sin pista activa")
        if self.cola_reproduccion:
            print(f"\n  Cola ({len(self.cola_reproduccion)} pista(s)):")
            for i, item in enumerate(self.cola_reproduccion, 1):
                print(f"    {i}. {item._titulo} — {item._autor}")
        else:
            print("  Cola vacía")
        print("=" * 40)

    def vaciar_cola(self):
        self.cola_reproduccion.clear()
        print("🗑️  Cola vaciada.")
        return self

    def cargar_agrupacion(self, agrupacion):
        """Carga todos los elementos de un Album o Playlist en la cola."""
        for item in agrupacion:
            self.cola_reproduccion.append(item)
        print(f"📋 '{agrupacion.nombre}' cargada en cola ({len(agrupacion)} pistas).")
        return self