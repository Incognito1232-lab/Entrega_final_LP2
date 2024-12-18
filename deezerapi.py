import requests

def get_top_artists():
    
    """
    Obtiene los 6 artistas más populares desde la API de Deezer.

    Realiza una solicitud HTTP al endpoint público de Deezer para recuperar
    los artistas más escuchados, extrayendo solo los nombres y las imágenes
    de los primeros 6 artistas.

    Returns:
        list: Una lista de diccionarios con los siguientes datos:
            - "name": (str) Nombre del artista.
            - "picture": (str) URL de la imagen del artista.
        Si la solicitud falla, devuelve una lista vacía.
    """
    
    # Endpoint de la API de Deezer para obtener los artistas más escuchados
    url = "https://api.deezer.com/chart/0/artists"

    # Hacer la solicitud
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Obtener la lista de los 6 artistas más escuchados
        top_artists = data.get("data", [])[:6]
        
        # Devolver solo el nombre y la imagen de cada artista
        artists_info = [
            {"name": artist.get("name"), "picture": artist.get("picture")}
            for artist in top_artists
        ]
        return artists_info
    else:
        print(f"Error al obtener los datos: {response.status_code}")
        return []

# Probar la función get_top_artists
artistas = get_top_artists()

if artistas:
    print("Artistas más populares:")
    for artista in artistas:
        print(f"Nombre: {artista['name']}, Imagen: {artista['picture']}")
else:
    print("No se pudieron obtener los artistas.")
