import os
import subprocess
import sys
import threading
import queue
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, request, jsonify
import webbrowser
import socket

app = Flask(__name__)

DOWNLOAD_DIR = r"D:\sets"
CACHE_DIR = r"D:\sets\cache"
progress_queues = {}

# Remplace par tes identifiants Spotify (optionnel pour spotdl)
SPOTIFY_CLIENT_ID = "ton_client_id"
SPOTIFY_CLIENT_SECRET = "ton_client_secret"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

PYTHON_EXECUTABLE = sys.executable

def run_command(command, progress_queue=None, shell=False, timeout=600):
    try:
        start_time = time.time()
        if progress_queue:
            progress_queue.put(f"[DEBUG {time.strftime('%H:%M:%S')}] Lancement : {' '.join(command)}")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell
        )
        output = ""
        if progress_queue:
            for line in iter(process.stdout.readline, ''):
                timestamp = time.strftime('%H:%M:%S')
                progress_queue.put(f"[DEBUG {timestamp}] stdout: {line.strip()}")
                print(f"[DEBUG {timestamp}] stdout: {line.strip()}")
                output += line
            for line in iter(process.stderr.readline, ''):
                timestamp = time.strftime('%H:%M:%S')
                progress_queue.put(f"[DEBUG {timestamp}] stderr: {line.strip()}")
                print(f"[DEBUG {timestamp}] stderr: {line.strip()}")
                output += line
        stdout, stderr = process.communicate(timeout=timeout)
        output += stdout + stderr
        success = process.returncode == 0
        end_time = time.time()
        duration = end_time - start_time
        if progress_queue:
            progress_queue.put(f"[DEBUG {time.strftime('%H:%M:%S')}] Fin en {duration:.2f}s, succès : {success}")
        print(f"[DEBUG {time.strftime('%H:%M:%S')}] Fin en {duration:.2f}s, succès : {success}")
        return success, output
    except subprocess.TimeoutExpired:
        process.kill()
        if progress_queue:
            progress_queue.put(f"[ERROR {time.strftime('%H:%M:%S')}] Timeout après {timeout}s")
        print(f"[ERROR {time.strftime('%H:%M:%S')}] Timeout après {timeout}s")
        return False, f"Timeout après {timeout}s"
    except Exception as e:
        if progress_queue:
            progress_queue.put(f"[ERROR {time.strftime('%H:%M:%S')}] Exception : {str(e)}")
        print(f"[ERROR {time.strftime('%H:%M:%S')}] Exception : {str(e)}")
        return False, str(e)

def download_spotify_with_spotdl(url, progress_queue):
    os.chdir(DOWNLOAD_DIR)
    command = [
        PYTHON_EXECUTABLE,
        "-m",
        "spotdl",
        url,
        "--audio",
        "youtube",
        "--format",
        "mp3",
        "--bitrate",
        "320k",
        "--threads",
        "4",
        "--overwrite",
        "skip"
    ]
    success, output = run_command(command, progress_queue)
    if success:
        downloaded = sum(1 for line in output.splitlines() if "Downloaded" in line and ".mp3" in line)
        progress_queue.put(f"[INFO {time.strftime('%H:%M:%S')}] Téléchargement terminé : {downloaded} chansons")
        print(f"[INFO {time.strftime('%H:%M:%S')}] Téléchargement terminé : {downloaded} chansons")
    else:
        progress_queue.put(f"[ERROR {time.strftime('%H:%M:%S')}] Échec spotdl : {output}")
        print(f"[ERROR {time.strftime('%H:%M:%S')}] Échec spotdl : {output}")

def download_soundcloud_with_ytdlp(url, progress_queue):
    os.chdir(DOWNLOAD_DIR)
    command = [
        PYTHON_EXECUTABLE,
        "-m",
        "yt_dlp",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "--format",
        "bestaudio",
        "--concurrent-fragments",
        "8",
        "--retries",
        "15",
        "--retry-sleep",
        "10",
        "--force-ipv4",
        "--cache-dir",
        CACHE_DIR,
        "--no-check-certificate",
        "--no-cache-dir",
        url
    ]
    success, output = run_command(command, progress_queue)
    if success:
        downloaded = sum(1 for line in output.splitlines() if "Destination" in line and ".mp3" in line)
        progress_queue.put(f"[INFO {time.strftime('%H:%M:%S')}] Téléchargement SoundCloud terminé : {downloaded} fichiers")
        print(f"[INFO {time.strftime('%H:%M:%S')}] Téléchargement SoundCloud terminé : {downloaded} fichiers")
    else:
        progress_queue.put(f"[ERROR {time.strftime('%H:%M:%S')}] Échec SoundCloud : {output}")
        print(f"[ERROR {time.strftime('%H:%M:%S')}] Échec SoundCloud : {output}")

def download_youtube_music_with_ytdlp(url, progress_queue):
    os.chdir(DOWNLOAD_DIR)
    command = [
        PYTHON_EXECUTABLE,
        "-m",
        "yt_dlp",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "--format",
        "bestaudio",
        "--yes-playlist",
        "--concurrent-fragments",
        "8",
        "--retries",
        "15",
        "--retry-sleep",
        "10",
        "--force-ipv4",
        "--cache-dir",
        CACHE_DIR,
        "--no-check-certificate",
        "--no-cache-dir",
        url
    ]
    success, output = run_command(command, progress_queue)
    if success:
        downloaded = sum(1 for line in output.splitlines() if "Destination" in line and ".mp3" in line)
        progress_queue.put(f"[INFO {time.strftime('%H:%M:%S')}] Téléchargement YouTube Music terminé : {downloaded} fichiers")
        print(f"[INFO {time.strftime('%H:%M:%S')}] Téléchargement YouTube Music terminé : {downloaded} fichiers")
    else:
        progress_queue.put(f"[ERROR {time.strftime('%H:%M:%S')}] Échec YouTube Music : {output}")
        print(f"[ERROR {time.strftime('%H:%M:%S')}] Échec YouTube Music : {output}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_spotify', methods=['POST'])
def download_spotify():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL vide'}), 400

    progress_queue = queue.Queue()
    progress_queues['spotify'] = progress_queue
    
    threading.Thread(target=download_spotify_with_spotdl, args=(url, progress_queue)).start()
    return jsonify({'message': 'Téléchargement Spotify démarré avec spotdl'})

@app.route('/download_soundcloud', methods=['POST'])
def download_soundcloud():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL vide'}), 400

    progress_queue = queue.Queue()
    progress_queues['soundcloud'] = progress_queue
    
    threading.Thread(target=download_soundcloud_with_ytdlp, args=(url, progress_queue)).start()
    return jsonify({'message': 'Téléchargement SoundCloud démarré avec yt-dlp'})

@app.route('/download_youtube_music', methods=['POST'])
def download_youtube_music():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL vide'}), 400

    progress_queue = queue.Queue()
    progress_queues['youtube_music'] = progress_queue
    
    threading.Thread(target=download_youtube_music_with_ytdlp, args=(url, progress_queue)).start()
    return jsonify({'message': 'Téléchargement YouTube Music démarré avec yt-dlp'})

@app.route('/progress/<service_type>', methods=['GET'])
def get_progress(service_type):
    if service_type not in progress_queues:
        return jsonify({'progress': 'Aucun téléchargement en cours'})
    
    progress_queue = progress_queues[service_type]
    updates = []
    while not progress_queue.empty():
        updates.append(progress_queue.get())
    return jsonify({'progress': updates[-1] if updates else 'En cours...'})

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 5000))
        sock.close()
        webbrowser.open('http://127.0.0.1:5000')
    except socket.error:
        pass
    
    app.run(debug=True, use_reloader=False)