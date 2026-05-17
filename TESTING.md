
## Guía de prueba paso a paso

Sigue este orden exacto. Copia y pega los datos cuando te pida algo.

### Arrancar el programa

```bash
python main.py
```

Deberías ver:
```
════════════════════════════════════════════
   🎵  SPOTIFY CLONE  —  Artur & Pepe
   Catálogo cargado: 65 canciones
════════════════════════════════════════════
```

---

### Paso 1 — Cuenta (opción 8)

```
Elige: 8
Elige: 2      ← Registrarse
Nuevo usuario: artur
Contraseña: 1234
```

Deberías ver `✅ Usuario registrado`. Luego inicia sesión:

```
Elige: 1      ← Iniciar sesión
Usuario: artur
Contraseña: 1234
```

El menú debe mostrar `[artur]` en vez de `[Invitado]`.

```
Elige: 0      ← volver al menú principal
```

---

### Paso 2 — Biblioteca (opción 1)

```
Elige: 1
```

Deberías ver las 65 canciones del catálogo con iconos 👑 PRO. Pulsa Enter para volver.

---

### Paso 3 — Añadir canción correcta (opción 2)

```
Elige: 2
Género: Rock
Título: Thunderstruck
Autor: AC/DC
Colaboradores: (Enter — ninguno)
Portada: thunder.jpg
Duración: 292
Bitrate: 320
```

Deberías ver `✅ 'Thunderstruck' añadida a la biblioteca.`

---

### Paso 4 — Añadir canción con bitrate CUTRE (opción 2)

```
Elige: 2
Género: Pop
Título: Canción Cutre
Autor: DJ Malo
Colaboradores: (Enter)
Portada: (Enter)
Duración: 180
Bitrate: 100
```

Deberías ver `⚠️ 'Canción Cutre' tiene un bitrate de 100. Es calidad cutre.` y luego `✅ añadida`.

---

### Paso 5 — Añadir canción que FALLA (opción 2)

Prueba `CalidadInsuficienteError` y escritura en `persistencia/errores.txt`.

```
Elige: 2
Género: Trap
Título: Canción Rota
Autor: Nadie
Colaboradores: (Enter)
Portada: (Enter)
Duración: 120
Bitrate: 32
```

Deberías ver `❌ No se pudo añadir: Bitrate 32kbps insuficiente.` Comprueba el fichero:

```bash
cat persistencia/errores.txt
```

---

### Paso 6 — Añadir podcast (opción 3)

```
Elige: 3
Tema: Tecnología
Título: Python para todos
Autor: Guido van Rossum
Colaboradores: Artur, Pepe
Portada: (Enter)
Duración: 3600
Bitrate: 256
```

Deberías ver `✅ Podcast 'Python para todos' añadido.` El bitrate se capará a 98kbps automáticamente.

---

### Paso 7 — Buscador (opción 4)

**Búsqueda aproximada — opción 1:**
```
Elige: 4 → 1
Buscar: blnding ligh
```
Debe encontrar `Blinding Lights` aunque esté mal escrito.

**Por género — opción 2:**
```
Elige: 2
Género: pop
```
Debe salir todo lo que contenga "pop": Pop, Indie Pop, Electropop, etc.

**Por artista — opción 3:**
```
Elige: 3
Artista: Ariana Grande
```
Debe mostrar también canciones donde Ariana es colaboradora, no solo autora.

**Por duración — opción 4:**
```
Elige: 4
Duración mínima: 200
Duración máxima: 240
```

**Solo canciones — opción 5:** no debe aparecer el podcast.

**Solo podcasts — opción 6:** solo debe aparecer `Python para todos`.

```
Elige: 0
```

---

### Paso 8 — Playlists (opción 5)

```
Elige: 5 → 1
Nombre: Mi Primera Playlist
Visibilidad: (Enter — publica)
```

Añade 3 canciones distintas con la opción 2. Luego intenta añadir la misma dos veces — debe avisar de duplicado.

```
Elige: 3      ← Ver playlist (debe mostrar canciones y duración total)
Elige: 4      ← Cambiar visibilidad (debe pasar a privada)
```

Crea una segunda playlist con 2 canciones distintas y fusiónalas:

```
Elige: 1      ← Nueva playlist: "Segunda Playlist"
Elige: 5      ← Fusionar → selecciona playlist 1 y playlist 2
```

Debe crear una tercera playlist con todas las canciones combinadas.

```
Elige: 0
```

---

### Paso 9 — Álbumes (opción 6)

```
Elige: 6 → 1
Artista: The Weeknd
Nombre: After Hours
Año: 2020
```

```
Elige: 2      ← Añadir canción
```

Solo aparecerán canciones de `The Weeknd`. Selecciona una. Comprueba que no puedes añadir canciones de otro artista.

```
Elige: 3      ← Ver álbum
Elige: 0
```

---

### Paso 10 — Reproductor (opción 7)

```
Elige: 7 → 1
(selecciona cualquier canción)
```

Debe reproducir y registrar en `data/historial.txt`.

```
Elige: 2      ← Añade 3 canciones a la cola
Elige: 6      ← Ver cola (deben aparecer las 3)
Elige: 3      ← Siguiente (repite un par de veces)
Elige: 4      ← Cargar playlist en cola
Elige: 7      ← Vaciar cola
Elige: 6      ← Ver cola (debe estar vacía)
Elige: 0
```

---

### Paso 11 — Historial (opción 9)

```
Elige: 9
```

Debe mostrar todas las reproducciones con fecha y hora. Comprueba también el fichero directamente:

```bash
cat data/historial.txt
```

---

### Paso 12 — Validación de robustez

Vuelve a añadir una canción (opción 2) y cuando pida duración escribe:

```
Duración: hola
```

Debe responder `Introduce un número` sin petar. Escribe `200` y continúa normal.

---

### Paso 13 — Salir (opción 0)

```
Elige: 0
```

Debe mostrar `👋 ¡Hasta luego!` y cerrar limpio.

---

### Comprobación final de ficheros

```bash
cat data/historial.txt
cat persistencia/errores.txt
```

`historial.txt` debe tener una línea por cada reproducción del paso 10.  
`errores.txt` debe tener la línea del bitrate 32 kbps del paso 5.  
Si los dos tienen contenido, la persistencia funciona correctamente.
