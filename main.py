import os
import subprocess
import sys
from flask import Flask, render_template, request, jsonify
import webbrowser
import socket

app = Flask(__name__)

# Dossier de téléchargement
DOWNLOAD_DIR = r"D:\sets"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Chemin vers l’exécutable Python (pour appeler spotdl et yt-dlp)
PYTHON_EXECUTABLE = sys.executable

def run_command(command, shell=True):
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            # Afficher les erreurs dans la console pour déboguer
            print(f"Erreur lors de l'exécution de la commande : {command}")
            print(f"Sortie standard : {stdout}")
            print(f"Sortie d'erreur : {stderr}")
            return False, stderr or stdout or "Erreur inconnue"
        print(f"Sortie standard : {stdout}")
        return True, stdout
    except Exception as e:
        print(f"Exception lors de l'exécution de la commande : {str(e)}")
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_soundcloud', methods=['POST'])
def download_soundcloud():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL manquante'})

    os.chdir(DOWNLOAD_DIR)
    # Appeler yt-dlp via Python avec la meilleure qualité
    command = [
        PYTHON_EXECUTABLE,
        "-m",
        "yt_dlp",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",  # Meilleure qualité possible
        url
    ]
    success, output = run_command(command, shell=False)

    if success:
        return jsonify({'message': 'Téléchargement SoundCloud terminé'})
    else:
        return jsonify({'error': output})

@app.route('/download_spotify', methods=['POST'])
def download_spotify():
    """Lance le téléchargement Spotify."""
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL vide'}), 400
    
    try:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        os.chdir(DOWNLOAD_DIR)
        command = [sys.executable, "-m", "spotdl", url, "--bitrate", "320k", "--format", "mp3"]
        subprocess.Popen(command)  # Lance en arrière-plan, pas de logs ici
        return jsonify({'message': 'Téléchargement Spotify démarré'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Vérifier si le port est déjà utilisé pour éviter les doubles ouvertures
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 5000))
        sock.close()
        # Si le port est libre, ouvrir le navigateur
        webbrowser.open('http://127.0.0.1:5000')
    except socket.error:
        # Si le port est déjà utilisé, ne pas ouvrir le navigateur
        print("Une instance de l'application est déjà en cours. Le navigateur ne sera pas ouvert à nouveau.")
    
    # Lancer Flask sans reloader
    app.run(debug=True, use_reloader=False)