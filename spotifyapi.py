import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configuración de las credenciales
# Se define el client_id y client_secret necesarios para autenticar con la API de Spotify.
client_id = 'b415dbb34fcc444090fcb5f8d80b035f'
client_secret = '5e94387d48cf4f2e9ffe88bb0859cb2b'

# Se crea un gestor de credenciales utilizando SpotifyClientCredentials de Spotipy.
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

# Se inicializa la instancia de Spotipy con las credenciales configuradas.
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Función para obtener las 10 canciones más populares de un género, incluyendo las rutas
def get_top_tracks_by_genre(genre_name):
    """
    Obtiene las 10 canciones más populares de un género específico desde la API de Spotify.
    
    Parámetros:
        genre_name (str): Nombre del género musical a buscar.
        
    Retorna:
        dict: Contiene el nombre del género y una lista de las canciones encontradas, 
              o un mensaje de error si no se encuentran canciones o ocurre un problema.
    """
    try:
        # Realiza una búsqueda en la API de Spotify con el género especificado.
        resultado_busqueda = sp.search(q='genre:' + genre_name, type='track', limit=10)
        
        # Verifica si se encontraron canciones en los resultados.
        if resultado_busqueda['tracks']['items']:
            # Extrae la información relevante de cada canción: nombre, artista y URL de Spotify.
            canciones = [
                {
                    "name": track['name'],                 # Nombre de la canción
                    "artist": track['artists'][0]['name'], # Nombre del primer artista
                    "url": track['external_urls']['spotify'] # URL de la canción en Spotify
                }
                for track in resultado_busqueda['tracks']['items']
            ]
            # Devuelve el género y la lista de canciones.
            return {"genre": genre_name, "tracks": canciones}
        else:
            # Devuelve un mensaje de error si no se encontraron canciones para el género.
            return {"error": "No se encontraron canciones para el género especificado."}
    except Exception as e:
        # Captura y devuelve cualquier excepción ocurrida como mensaje de error.
        return {"error": str(e)}
