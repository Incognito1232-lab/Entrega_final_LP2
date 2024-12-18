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
## Last.fm API

Esta sección describe cómo se utiliza la API de Last.fm en el proyecto para obtener información sobre artistas, canciones y álbumes, mediante la biblioteca [requests](https://requests.readthedocs.io/).

### Configuración de Credenciales

Para acceder a la API de Last.fm, es necesario configurar una clave de API:

1. Registra una cuenta en [Last.fm](https://www.last.fm/).
2. Obtén tu clave **`API_KEY`** desde el [Last.fm API portal](https://www.last.fm/api).
3. Configura las credenciales en el código, utilizando la biblioteca `requests` para realizar solicitudes a la API.

   ```python
   import requests

   API_KEY = 'TU_API_KEY'
   BASE_URL = "http://ws.audioscrobbler.com/2.0/"
   ```

### Función: `get_artist_info`

Esta función permite obtener la biografía y el número de oyentes de un artista específico.

#### Descripción

La función utiliza la API de Last.fm para obtener información sobre un artista. Devuelve una tupla con la biografía resumida y el número de oyentes del artista.

#### Definición

```python
def get_artist_info(artist_name):
    """
    Obtiene la biografía y el número de oyentes de un artista desde Last.fm.
    
    Parámetros:
        artist_name (str): Nombre del artista a consultar.
        
    Retorna:
        tuple: Un par que contiene:
            - biography (str): Resumen de la biografía del artista en español.
            - listeners (str): Número de oyentes del artista en Last.fm.
            Si no se encuentra información, retorna (None, None).
    """
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json",
        "lang": "es"  # Idioma de la biografía
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if 'artist' in data:
        biography = data['artist']['bio']['summary']
        listeners = data['artist']['stats']['listeners']
        return biography, listeners
    else:
        return None, None
```

#### Flujo de Trabajo

1. **Realizar la solicitud a la API:**  
   La función hace una solicitud HTTP a la API de Last.fm con el nombre del artista. Utiliza la clave API, el nombre del artista y el idioma de la biografía.

   ```python
   params = {
       "method": "artist.getinfo",
       "artist": artist_name,
       "api_key": API_KEY,
       "format": "json",
       "lang": "es"  # Idioma de la biografía
   }
   response = requests.get(BASE_URL, params=params)
   data = response.json()
   ```
2. **Procesar la respuesta:**
   Si la respuesta contiene información del artista, se extraen dos campos: la biografía resumida y el número de oyentes. En caso contrario, se retorna (None, None).
   ```python
   if 'artist' in data:
    biography = data['artist']['bio']['summary']  # Biografía resumida
    listeners = data['artist']['stats']['listeners']  # Número de oyentes
    return biography, listeners
   else:
    return None, None
   ```
3. **Manejo de errores:**
   Si la solicitud falla o no se encuentra información del artista, se retorna una tupla (None, None).
   ```python
   return None, None
   ```
#### Ejemplo de Respuesta

Cuando se consulta el artista "Queen", la respuesta JSON podría verse así:

```json
{
  "artist": {
    "bio": {
      "summary": "Queen es una banda de rock británica formada en 1970. Es conocida por su estilo musical innovador y sus icónicas presentaciones en vivo."
    },
    "stats": {
      "listeners": 12345678
    }
  }
}
```
### Función: `get_top_tracks`

Esta función permite obtener las canciones más populares de un artista específico.

#### Descripción

La función utiliza la API de Last.fm para obtener las canciones más escuchadas de un artista determinado. Devuelve una lista con los nombres de las canciones más populares del artista, o un mensaje de error si no se encuentran canciones.

#### Definición

```python
def get_top_tracks(artist_name, limit=10):
    """
    Obtiene las canciones más populares de un artista en Last.fm.
    
    Parámetros:
        artist_name (str): Nombre del artista a consultar.
        limit (int): Número máximo de canciones a devolver (por defecto, 10).
        
    Retorna:
        list: Lista de nombres de las canciones más escuchadas del artista.
              Si no se encuentra información, retorna None.
    """
```
#### Flujo de Trabajo

1. **Realizar una solicitud a la API:**  
   Se realiza una solicitud HTTP GET para obtener las canciones más escuchadas del artista.  
   
   ```python
   params = {
       "method": "artist.gettoptracks",
       "artist": artist_name,
       "api_key": API_KEY,
       "format": "json",
       "limit": limit
   }
   response = requests.get(BASE_URL, params=params)
   data = response.json()
   ```
2. **Procesar la Respuesta:**
   Si la respuesta contiene canciones, la función extrae los nombres de las canciones más populares del artista.
   ```python
   if 'toptracks' in data and data['toptracks']['track']:
    top_tracks = [track['name'] for track in data['toptracks']['track']]
    return top_tracks
   ```
3. **Manejo de Errores:**
   Si no se encuentran canciones o hay un error, la función retorna `None`.
   ```python
   else:
       return None
   ```
#### Ejemplo de Respuesta

Cuando se consulta el artista "Queen", la respuesta JSON podría verse así:

```json
{
  "toptracks": {
    "track": [
      {
        "name": "Bohemian Rhapsody"
      },
      {
        "name": "We Will Rock You"
      }
    ]
  }
}
```
#### Posibles Errores

- **Sin resultados:**  
  Si no hay canciones disponibles para el artista solicitado:
  
  ```json
  {"error": "No se encontraron canciones para el artista especificado."}
  
- **Errores Generales:**
  En caso de problemas de conexión u otros errores inesperados, la respuesta podría contener un mensaje general de error.
  ```json
  {
  "error": "Descripción del error."
  }
  ```
### Función: `get_top_album`

Esta función permite obtener el álbum más popular de un artista específico.

#### Descripción

La función utiliza la API de Last.fm para obtener el álbum más escuchado del artista. Devuelve el nombre del álbum más popular o `None` si no se encuentra información.

#### Definición

```python
def get_top_album(artist_name):
    """
    Obtiene el álbum más popular de un artista en Last.fm.
    
    Parámetros:
        artist_name (str): Nombre del artista a consultar.
        
    Retorna:
        str: Nombre del álbum más famoso del artista.
             Si no se encuentra información, retorna None.
    """
    params = {
        "method": "artist.gettopalbums",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if 'topalbums' in data and data['topalbums']['album']:
        top_album = data['topalbums']['album'][0]['name']
        return top_album
    else:
        return None
```
#### Flujo de Trabajo

1. **Realizar una solicitud a la API:**  
   La función realiza una solicitud HTTP GET a la API de Last.fm para obtener los álbumes más populares del artista.
   
   ```python
   params = {
       "method": "artist.gettopalbums",
       "artist": artist_name,
       "api_key": API_KEY,
       "format": "json"
   }
   response = requests.get(BASE_URL, params=params)
   data = response.json()
   ```
2. **Procesar la respuesta:**
   Si la respuesta contiene información sobre los álbumes más populares, la función extrae el nombre del álbum más popular del artista.
   ```python
   if 'topalbums' in data and data['topalbums']['album']:
       top_album = data['topalbums']['album'][0]['name']
       return top_album
   ```
3. **Manejo de errores:**
   Si no se encuentra información sobre los álbumes o ocurre un error, la función retorna `None`.
   ```python
   else:
       return None
   ```
#### Ejemplo de Respuesta

Cuando se consulta el artista "Queen", la respuesta JSON podría verse así:

```json
{
  "topalbums": {
    "album": [
      {
        "name": "A Night at the Opera",
        "url": "https://www.last.fm/music/Queen/A+Night+at+the+Opera"
      }
    ]
  }
}
```
#### Posibles Errores

- **Sin resultados:**  
  Si no se encuentran álbumes populares para el artista solicitado, la respuesta podría ser:

```json
{"error": "No se encontraron álbumes para el artista especificado."}
```

- **Errores Generales:**
  En caso de problemas de conexión u otros errores inesperados, la respuesta podría ser:

```json
{"error": "Descripción del error."}
```
### Función: `get_global_top_tracks_html`

Esta función obtiene las canciones más populares a nivel global en Last.fm.

#### Descripción

La función utiliza la API de Last.fm para obtener las canciones más populares a nivel global. Devuelve una lista con información relevante sobre las canciones más escuchadas.

#### Definición

```python
def get_global_top_tracks_html(limit=4):
    """
    Obtiene las canciones más populares a nivel global en Last.fm.
    
    Parámetros:
        limit (int): Número máximo de canciones a devolver (por defecto, 4).
        
    Retorna:
        list: Lista de diccionarios con información de cada canción:
              - name (str): Nombre de la canción.
              - artist (str): Nombre del artista.
              - url (str): URL de la canción en Last.fm.
              Si no se encuentra información, retorna None.
    """
```
#### Flujo de Trabajo

1. **Realizar una solicitud a la API:**  
   Se realiza una solicitud HTTP GET para obtener las canciones más populares globalmente.  
   Los parámetros de la solicitud incluyen el método `chart.getTopTracks`, la clave de la API y el límite de canciones a obtener.  
   ```python
   params = {
       "method": "chart.getTopTracks",
       "api_key": API_KEY,
       "format": "json",
       "limit": limit
   }
   response = requests.get(BASE_URL, params=params)
   data = response.json()
   ```
2. **Procesar la Respuesta:**
   Si la respuesta contiene canciones, la función extrae los siguientes datos de cada canción:

- **`name`**: El nombre de la canción.
- **`artist`**: El nombre del artista.
- **`url`**: El enlace a la canción en Last.fm.

Los datos extraídos se almacenan en una lista de diccionarios:

```python
global_top_tracks = []
for track in data['tracks']['track']:
    name = track['name']
    artist = track['artist']['name']
    url = track['url']
    global_top_tracks.append({"name": name, "artist": artist, "url": url})
```
3. **Manejo de Errores:**
   Si no se encuentran canciones o hay algún problema con la respuesta de la API, se devuelve `None`. Si la respuesta de la API no contiene la información esperada o hay algún fallo en
   la solicitud, se maneja el error de la siguiente manera:
```python
if 'tracks' not in data or not data['tracks']['track']:
    return None
```
   En caso de error en la conexión o problemas con la API, también se puede capturar una excepción:
```python
except Exception as e:
    return {"error": str(e)}
```   
#### Ejemplo de Respuesta

Cuando se consulta las canciones más populares a nivel global, la respuesta JSON podría verse así:

```json
{
  "tracks": {
    "track": [
      {
        "name": "Blinding Lights",
        "artist": {
          "name": "The Weeknd"
        },
        "url": "https://www.last.fm/music/The+Weeknd/_/Blinding+Lights"
      },
      {
        "name": "Levitating",
        "artist": {
          "name": "Dua Lipa"
        },
        "url": "https://www.last.fm/music/Dua+Lipa/_/Levitating"
      }
    ]
  }
}
```
#### Posibles Errores

- **Sin resultados:**  
  Si no se encuentran canciones en la respuesta, se puede devolver un mensaje de error en formato JSON indicando que no hay canciones disponibles:

  ```json
  {"error": "No se encontraron canciones para la consulta."}
  ```
#### Errores Generales

- **Error de conexión:**  
  Si hay un problema con la red o la conexión a la API, puede producirse un error de conexión. Esto puede ocurrir si el servidor de Last.fm está inactivo o si hay un problema de red.

  ```json
  {"error": "No se pudo establecer conexión con el servidor de Last.fm."}
  ```

## Deezer API

Esta sección describe cómo se utiliza la API de Spotify en el proyecto para obtener canciones basadas en géneros musicales, mediante la biblioteca [Spotipy](https://spotipy.readthedocs.io/).

### Función: `get_top_artists`

Esta función permite obtener información sobre los artistas más populares de Deezer.

### Configuración Previa

No se requiere autenticación ni claves de API para acceder al endpoint utilizado en este proyecto. Sin embargo, asegúrate de que tu entorno tenga acceso a internet y que la biblioteca requests esté instalada.

#### Descripción

La función realiza una solicitud HTTP al endpoint público de Deezer y procesa los datos para devolver una lista de los 6 artistas más escuchados, incluyendo su nombre y la URL de su imagen.

#### Definición

```python
def get_top_artists():
    """
    Obtiene los 6 artistas más populares desde la API de Deezer.

    Returns:
        list: Una lista de diccionarios con los siguientes datos:
            - "name": (str) Nombre del artista.
            - "picture": (str) URL de la imagen del artista.
        Si la solicitud falla, devuelve una lista vacía.
    """

```

#### Flujo de Trabajo

1. **Solicitar datos:**  
   La función realiza una solicitud HTTP al endpoint https://api.deezer.com/chart/0/artists utilizando la biblioteca requests.
   ```python
   response = requests.get("https://api.deezer.com/chart/0/artists")
   ```

2. **Procesar la respuesta:**  
   Si la solicitud es exitosa (status_code 200), se procesan los datos para extraer el nombre y la URL de la imagen de los primeros 6 artistas.
   ```python
   data = response.json()
   top_artists = data.get("data", [])[:6]
   artists_info = [
      {"name": artist.get("name"), "picture": artist.get("picture")}
      for artist in top_artists
   ]
   ```

3. **Manejo de errores:**  
   Si la solicitud falla, la función imprime el código de estado HTTP correspondiente y devuelve una lista vacía.

   ```python
   if response.status_code != 200:
    print(f"Error al obtener los datos: {response.status_code}")
    return []
   ```

#### Ejemplo de uso

   ```python
   # Llamar a la función para obtener los 6 artistas más populares
   artistas = get_top_artists()

   # Imprimir los resultados
   if artistas:
      print("Artistas más populares:")
      for artista in artistas:
          print(f"Nombre: {artista['name']}, Imagen: {artista['picture']}")
   else:
      print("No se pudieron obtener los artistas.")

   ```

#### Ejemplo de Respuesta

Cuando se obtiene la lista de los 6 artistas más populares, la respuesta de la API será algo como esto:

```json
{
  "data": [
    {
      "name": "Bad Bunny",
      "picture": "https://api.deezer.com/artist/10583405/image"
    },
    {
      "name": "J Balvin",
      "picture": "https://api.deezer.com/artist/4860761/image"
    },
    {
      "name": "Rauw Alejandro",
      "picture": "https://api.deezer.com/artist/11289472/image"
    },
    {
      "name": "Myke Towers",
      "picture": "https://api.deezer.com/artist/12029862/image"
    },
    {
      "name": "Farruko",
      "picture": "https://api.deezer.com/artist/614223/image"
    },
    {
      "name": "Maluma",
      "picture": "https://api.deezer.com/artist/1424602/image"
    }
  ]
}

```

#### Posibles Errores

- **Conexión fallida o API inaccesible::**  
  Si no se puede establecer conexión con la API, se imprime el mensaje:
  ```json
  {
    "error": "No se pudo obtener los datos de la API.",
  }
  ```

- **Respuesta vacía:**
  Si la respuesta no contiene datos esperados, la lista devuelta estará vacía.










