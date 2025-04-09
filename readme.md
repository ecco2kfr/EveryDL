# 🎵 EveryDL

Une application web en Python (Flask) pour télécharger rapidement des musiques en MP3 depuis **SoundCloud** et **Spotify** via une interface simple.

## 🚀 Fonctionnalités

- Téléchargement MP3 depuis **SoundCloud** (via `yt-dlp`)
- Téléchargement MP3 depuis **Spotify** (via `spotdl`)
- Interface web claire avec formulaire
- Lancement automatique dans le navigateur

## 🛠️ Technologies utilisées

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [spotdl](https://github.com/spotDL/spotify-downloader)

## ⚙️ Configuration

1. Installe les dépendances :

    ```bash
    pip install flask spotdl
    ```

2. Télécharge [`yt-dlp`](https://github.com/yt-dlp/yt-dlp/releases):

3. Assure-toi d’avoir un dossier de destination pour les téléchargements :

    ```python
    DOWNLOAD_DIR = r"Ton chemin vers le dossier destination"
    ```

4. Lance l’application :

    ```bash
    python everyDL.py
    ```

5. Elle s’ouvrira automatiquement sur :

    ```
    http://127.0.0.1:5000
    ```

## 📄 Notes

- Le fichier HTML d’interface se trouve dans `templates/index.html`.

---

