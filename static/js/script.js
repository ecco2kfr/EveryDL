function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000); // Disparaît après 3 secondes
}

function download(type) {
    const url = document.getElementById('url').value;
    if (!url) {
        showToast('Veuillez entrer une URL !');
        return;
    }

    // Afficher la notification de lancement (même style pour les deux)
    showToast(`Lancement du téléchargement ${type === 'soundcloud' ? 'SoundCloud' : 'Spotify'}...`);

    // Lancer le téléchargement
    const endpoint = type === 'soundcloud' ? '/download_soundcloud' : '/download_spotify';
    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `url=${encodeURIComponent(url)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast('Erreur : ' + data.error);
        } else {
            showToast(data.message + ' (Regarde la console pour les détails)');
        }
    })
    .catch(error => {
        showToast('Erreur : ' + error);
    });
}

const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    if (currentTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }
});