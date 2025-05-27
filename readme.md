# 🎵 EveryDL

Une application web en Python (Flask) pour télécharger rapidement des musiques en MP3 depuis **SoundCloud** et **Spotify** via une interface simple.

## 🚀 Fonctionnalités

- Téléchargement MP3 depuis **SoundCloud** (via `yt-dlp`)
- Téléchargement MP3 depuis **Spotify** (via `spotdl`)
- Téléchargement MP3 depuis **YouTube Music** (chansons et playlists, via `yt-dlp`)
- Interface web claire 
- Lancement automatique dans le navigateur

## 🛠️ Technologies utilisées

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [spotdl](https://github.com/spotDL/spotify-downloader)

## ⚙️ Configuration

1. **Installe les dépendances** :
   `pip install flask spotdl yt-dlp`

2. **Assure-toi que `ffmpeg` est installé** (nécessaire pour `yt-dlp`) :
   - Télécharge-le depuis [ffmpeg.org](https://ffmpeg.org/download.html).
   - Ajoute-le à ton PATH (par exemple, sous Windows, mets le dossier contenant `ffmpeg.exe` dans la variable d’environnement PATH).

3. **Vérifie ou modifie le dossier de destination** dans `everyDL.py` :
   `DOWNLOAD_DIR = r"D:\sets"  # Remplace par ton chemin préféré`

4. **Lance l’application** :
   `python everyDL.py`

5. **Accède à l’application** :
   Ouvre ton navigateur à cette adresse :
   `http://127.0.0.1:5000`

## 📄 Notes

- Le fichier HTML d’interface se trouve dans `templates/index.html`.

---

