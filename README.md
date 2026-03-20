# Spotify Clone - Artur y Pepe
Un gestor de música y podcasts desarrollado en python que recrea una de las aplicaciones de música más famosa

## Descripción
En este proyecto se recrean algunas de las funcionalidades de la aplicación, como crear listas, añadir canciones, gestionar tu contenido ...

# Estructura del proyecto
```text
spotify_clone/
│
├── main.py                    ← punto de entrada, menú principal
│
├── models/                    ← todas las clases (POO puro)
│   ├── __init__.py
│   ├── contenido.py           ← clase abstracta base
│   ├── musica.py
│   ├── podcast.py
│   ├── agrupacion.py          ← clase base para Album y Playlist
│   ├── album.py
│   ├── playlist.py
│   ├── usuario.py
│   ├── biblioteca.py
│   └── audio.py
│
├── services/                  ← lógica de negocio (SRP)
│   ├── __init__.py
│   ├── reproductor.py
│   └── buscador.py
│
├── auth/                      ← autenticación separada
│   ├── __init__.py
│   └── gestor_auth.py         ← login + registro en una clase
│
├── data/                      ← datos simulados (diccionarios/listas)
│   └── catalogo.py
│
├── README.md
├── requirements.txt
└── .gitignore
```
## Instalación y Ejecución
### 1: Clonamos el repositorio

git clone [https://github.com/tu-usuario/spotify-clone.git](https://github.com/tu-usuario/spotify-clone.git)
cd spotify-clone

### 2: Instalar las dependencias

pip install -r requirements.txt

### 3: Iniciar la aplicación

python main.py

## Ejemplo de uso de la terminal
