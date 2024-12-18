import requests

# Configuración de la API
# Se define la clave de API y la URL base necesarias para interactuar con la API de Last.fm.
API_KEY = "05284d5e90ad5ad116c3b2e50916d0c3"  
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# Función para obtener información de un artista
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
    # Parámetros de la solicitud a la API para obtener información del artista.
    params = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json",
        "lang": "es"  # Idioma de la biografía
    }
    # Realiza la solicitud HTTP GET y procesa la respuesta.
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # Verifica si se obtuvo información válida del artista.
    if 'artist' in data:
        biography = data['artist']['bio']['summary']  # Biografía resumida
        listeners = data['artist']['stats']['listeners']  # Número de oyentes
        return biography, listeners
    else:
        return None, None

# Función para obtener las canciones más escuchadas de un artista
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
    # Parámetros de la solicitud a la API para obtener las canciones más populares.
    params = {
        "method": "artist.gettoptracks",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }
    # Realiza la solicitud HTTP GET y procesa la respuesta.
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # Verifica si se obtuvo una lista de canciones.
    if 'toptracks' in data and data['toptracks']['track']:
        top_tracks = [track['name'] for track in data['toptracks']['track']]  # Lista de canciones
        return top_tracks
    else:
        return None

# Función para obtener el álbum más famoso de un artista
def get_top_album(artist_name):
    """
    Obtiene el álbum más popular de un artista en Last.fm.
    
    Parámetros:
        artist_name (str): Nombre del artista a consultar.
        
    Retorna:
        str: Nombre del álbum más famoso del artista.
             Si no se encuentra información, retorna None.
    """
    # Parámetros de la solicitud a la API para obtener los álbumes más populares.
    params = {
        "method": "artist.gettopalbums",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json"
    }
    # Realiza la solicitud HTTP GET y procesa la respuesta.
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # Verifica si se obtuvo una lista de álbumes.
    if 'topalbums' in data and data['topalbums']['album']:
        top_album = data['topalbums']['album'][0]['name']  # Nombre del álbum más popular
        return top_album
    else:
        return None

# Función para obtener las canciones más escuchadas globalmente
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
    # Parámetros de la solicitud a la API para obtener las canciones globales más populares.
    params = {
        "method": "chart.getTopTracks",
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }
    # Realiza la solicitud HTTP GET y procesa la respuesta.
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # Verifica si se obtuvo una lista de canciones globales.
    if 'tracks' in data and data['tracks']['track']:
        global_top_tracks = []
        for track in data['tracks']['track']:
            # Extrae el nombre, artista y URL de cada canción.
            name = track['name']
            artist = track['artist']['name']
            url = track['url']
            global_top_tracks.append({"name": name, "artist": artist, "url": url})
        return global_top_tracks
    else:
        return None
    
