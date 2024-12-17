# Entrega_final_LP2
# Flask Music App

Una aplicación web basada en Flask que permite consultar información sobre artistas, géneros musicales y canciones populares utilizando diversas APIs de música como Last.fm, Spotify y Deezer.

## Características

- **Canciones más populares globalmente:** Obtiene las canciones más populares a nivel global desde Last.fm.
- **Artistas más populares:** Muestra una lista de artistas destacados utilizando la API de Deezer.
- **Información de artistas:** Permite buscar información detallada de un artista, como su biografía, oyentes, canciones principales y álbum destacado.
- **Canciones por género:** Proporciona una lista de las canciones más populares para un género específico utilizando Spotify.

## Tecnologías Utilizadas

- **Backend:**
  - Python con el framework Flask.
  - Integración con APIs externas (Last.fm, Spotify y Deezer).

- **Frontend:**
  - Plantillas HTML renderizadas con Flask (`render_template`).

## Requisitos Previos

1. Python 3.8 o superior.
2. Las siguientes dependencias de Python:
   - Flask
3. Credenciales para acceder a las APIs:
   - [Last.fm API](https://www.last.fm/api)
   - [Spotify API](https://developer.spotify.com/)
   - [Deezer API](https://developers.deezer.com/)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/usuario/flask-music-app.git
   cd flask-music-app
2. Ejecuta el archivo app.py y luego dale ctrl + click derecho al link que se proporciona

Aquí tienes el texto del `README.md` completo, listo para copiar y pegar, explicando la funcionalidad de la integración con la API de Spotify:

---

## Spotify API

Esta sección describe cómo se utiliza la API de Spotify en el proyecto para obtener canciones basadas en géneros musicales, mediante la biblioteca [Spotipy](https://spotipy.readthedocs.io/).

### Configuración de Credenciales

Para acceder a la API de Spotify, es necesario configurar las credenciales de acceso:

1. Registra una aplicación en el [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Obtén las claves **`client_id`** y **`client_secret`**.
3. Configura las credenciales en el código, utilizando `SpotifyClientCredentials` de la biblioteca Spotipy:

   ```python
   from spotipy.oauth2 import SpotifyClientCredentials
   import spotipy

   client_id = 'TU_CLIENT_ID'
   client_secret = 'TU_CLIENT_SECRET'

   client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
   sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
   ```

### Función: `get_top_tracks_by_genre`

Esta función permite obtener las 10 canciones más populares de un género musical específico.

#### Descripción

La función utiliza la API de Spotify para buscar canciones en función del género musical. Devuelve una lista con información relevante sobre las canciones encontradas.

#### Definición

```python
def get_top_tracks_by_genre(genre_name):
    """
    Obtiene las 10 canciones más populares de un género específico desde la API de Spotify.
    
    Parámetros:
        genre_name (str): Nombre del género musical a buscar.
        
    Retorna:
        dict: Contiene el nombre del género y una lista de las canciones encontradas, 
              o un mensaje de error si no se encuentran canciones o ocurre un problema.
    """
```

#### Flujo de Trabajo

1. **Realizar una búsqueda:**  
   La función utiliza el parámetro `genre:` para realizar una búsqueda de canciones relacionadas con el género proporcionado.  
   ```python
   resultado_busqueda = sp.search(q='genre:' + genre_name, type='track', limit=10)
   ```

2. **Procesar resultados:**  
   Si se encuentran canciones, la función extrae información relevante:
   - **`name`**: Nombre de la canción.
   - **`artist`**: Nombre del artista principal.
   - **`url`**: Enlace a la canción en Spotify.

   ```python
   canciones = [
       {
           "name": track['name'],
           "artist": track['artists'][0]['name'],
           "url": track['external_urls']['spotify']
       }
       for track in resultado_busqueda['tracks']['items']
   ]
   ```

3. **Manejo de errores:**  
   Si no se encuentran canciones o hay un problema con la API, se devuelve un mensaje de error.

   ```python
   return {"error": "No se encontraron canciones para el género especificado."}
   ```

#### Ejemplo de Respuesta

Cuando se busca el género "rock", la respuesta puede ser:

```json
{
  "genre": "rock",
  "tracks": [
    {
      "name": "Bohemian Rhapsody",
      "artist": "Queen",
      "url": "https://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J"
    },
    {
      "name": "Hotel California",
      "artist": "Eagles",
      "url": "https://open.spotify.com/track/40riOy7x9W7GXjyGp4pjAv"
    }
  ]
}
```

#### Posibles Errores

- **Sin resultados:**  
  Si no hay canciones disponibles para el género solicitado:
  ```json
  {"error": "No se encontraron canciones para el género especificado."}
  ```

- **Errores generales:**  
  En caso de problemas de conexión u otros errores inesperados:
  ```json
  {"error": "Descripción del error."}
  ```
