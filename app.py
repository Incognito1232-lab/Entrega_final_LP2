from flask import Flask, render_template, request, jsonify
from spotifyapi import get_top_tracks_by_genre
from lastfmapi import get_artist_info, get_top_tracks, get_top_album, get_global_top_tracks_html
import dezzerapi  # Importamos el archivo para interactuar con la API de Deezer

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Ruta principal que renderiza la página de inicio
@app.route("/")
def home():
    """
    Renderiza la página de inicio.
    Obtiene las canciones más populares globalmente desde Last.fm y los artistas más populares desde Deezer.
    """
    # Obtener las canciones más populares globalmente desde Last.fm (limite de 4)
    global_top_tracks = get_global_top_tracks_html(limit=4)
    
    # Obtener los artistas más populares desde Deezer
    top_artists = dezzerapi.get_top_artists()
    
    # Renderizar la plantilla HTML con los datos obtenidos
    return render_template("index.html", global_top_tracks=global_top_tracks, top_artists=top_artists)

# Ruta para manejar las solicitudes relacionadas con un artista
@app.route("/artist", methods=["POST"])
def artist():
    """
    Maneja las solicitudes POST para buscar información sobre un artista.
    Recibe el nombre del artista desde un formulario y devuelve información en formato JSON.
    """
    # Obtener el nombre del artista desde el formulario
    artist_name = request.form.get("artist_name")
    
    if not artist_name:
        # Responder con un error si no se proporciona el nombre del artista
        return jsonify({"error": "Debe ingresar un nombre de artista."})

    # Obtener información del artista desde la API de Last.fm
    biography, listeners = get_artist_info(artist_name)
    top_tracks = get_top_tracks(artist_name)
    top_album = get_top_album(artist_name)

    # Enviar los datos del artista como respuesta JSON
    return jsonify({
        "artist": artist_name,
        "biography": biography,
        "listeners": listeners,
        "top_tracks": top_tracks,
        "top_album": top_album
    })

# Ruta para manejar las solicitudes relacionadas con un género musical
@app.route("/genre", methods=["POST"])
def genre():
    """
    Maneja las solicitudes POST para buscar canciones principales de un género.
    Recibe el nombre del género desde un formulario y devuelve información en formato JSON.
    """
    # Obtener el nombre del género desde el formulario
    genre_name = request.form.get("genre_name")
    
    if not genre_name:
        # Responder con un error si no se proporciona el nombre del género
        return jsonify({"error": "Debe ingresar un género."})

    # Obtener las canciones principales del género desde la API de Spotify
    genre_data = get_top_tracks_by_genre(genre_name)

    # Enviar los datos del género como respuesta JSON
    return jsonify(genre_data)

# Ejecutar la aplicación en modo de depuración
if __name__ == "__main__":
    app.run(debug=True)
