function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function download(type) {
    const url = document.getElementById('url').value;
    if (!url) {
        showToast('Veuillez entrer une URL !');
        return;
    }

    const serviceName = type === 'soundcloud' ? 'SoundCloud' : type === 'spotify' ? 'Spotify' : 'YouTube Music';
    showToast(`Téléchargement ${serviceName} démarré...`);
    fetch(`/download_${type}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `url=${encodeURIComponent(url)}`
    })
    .then(resp => resp.json())
    .then(data => {
        if (data.error) {
            showToast('Erreur : ' + data.error);
        } else {
            showToast(data.message);
            startProgress(type);  // Lance le suivi de progression
        }
    })
    .catch(error => showToast('Erreur : ' + error));
}

function startProgress(type) {
    const progressContainer = document.querySelector('.progress-container');
    const progressText = document.getElementById('progress-text');
    progressContainer.style.display = 'block';

    const interval = setInterval(() => {
        fetch(`/progress/${type}`)
            .then(resp => resp.json())
            .then(data => {
                progressText.textContent = data.progress;
                if (data.progress.includes('terminé') || data.progress.includes('Erreur')) {
                    clearInterval(interval);
                    setTimeout(() => progressContainer.style.display = 'none', 2000);
                }
            });
    }, 1000);  // Met à jour toutes les secondes
}

const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    document.documentElement.setAttribute('data-theme', currentTheme === 'light' ? 'dark' : 'light');
});