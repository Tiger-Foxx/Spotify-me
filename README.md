# 🎵 Telegram Spotify Downloader

<p align="center">
  <a href="https://www.python.org">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg" width="250">
  </a>
  <a href="https://heroku.com/deploy?template=https://github.com/Tiger-Foxx/Spotify-me">
    <img src="https://www.herokucdn.com/deploy/button.svg" width="180">
  </a>
  <a href="https://t.me/spotdl_tel_bot">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&label=Demo" width="240">
  </a>
  <br>
  <a href="https://github.com/Tiger-Foxx/Spotify-me/stargazers">
    <img src="https://img.shields.io/github/stars/Tiger-Foxx/Spotify-me?style=social">
  </a>
  <a href="https://github.com/Tiger-Foxx/Spotify-me/fork">
    <img src="https://img.shields.io/github/forks/Tiger-Foxx/Spotify-me?label=Fork&style=social">
  </a>  
</p>

## 🦊 Qu'est-ce que c'est ?
C'est un bot Telegram qui permet de télécharger des musiques et des playlists Spotify en MP3 directement depuis YouTube. 🎶✨

### Ce que vous pouvez télécharger :
✅ Une seule chanson
✅ Un album complet
✅ Une playlist entière
✅ Tous les morceaux d'un artiste

📸 **Aperçu** :
<img src="https://github.com/Tiger-Foxx/Spotify-me/blob/master/demo.png" width="450" />

## 🚀 Comment l'utiliser ?

### 1️⃣ Configuration
Ajoutez votre token de bot Telegram dans un fichier `.env` avec la clé :
```
TELEGRAM_TOKEN=VOTRE_TOKEN_ICI
```

### 2️⃣ Installation des dépendances
Avant de lancer le bot, assurez-vous d'avoir installé les dépendances requises :
```
pip install -r requirements.txt
sudo snap install ffmpeg
npm install -g spotify-dl
```

### 3️⃣ Exécution du bot
Lancez simplement le bot avec :
```
python main.py
```

## 🔑 Authentification

Le bot propose une authentification simple. Pour l’activer, modifiez le fichier de configuration et mettez :
```json
"AUTH": {
  "ENABLE": true,
  "PASSWORD": "VotreMotDePasse"
}
```
Les utilisateurs devront entrer ce mot de passe pour accéder au bot. Les comptes autorisés seront enregistrés dans le fichier de configuration.

## 🎧 Téléchargement de musique

Le bot supporte plusieurs outils pour récupérer la musique à partir des liens Spotify. Choisissez votre préféré dans le fichier de config :

- **SpotDL (Python)** : [Spotify Downloader](https://github.com/spotDL/spotify-downloader)
- **SpotifyDL (JavaScript)** : [Spotify DL](https://github.com/SwapnilSoni1999/spotify-dl)

⚠ **Attention** : La version 3 de SpotDL a des bugs, il est recommandé d’utiliser SpotifyDL.

## 🐳 Docker

Envie de lancer ça proprement avec Docker ? C’est facile !
```bash
docker build -t telegram-spotify-downloader .
docker run -d telegram-spotify-downloader
```

## ☁️ Déploiement sur Heroku

Si vous voulez héberger le bot sur Heroku, voici comment faire :
1. Modifiez `config.json` si nécessaire et committez vos changements.
2. Ajoutez votre token de bot dans un fichier `.env` :
   ```
   TELEGRAM_TOKEN=VOTRE_TOKEN_ICI
   ```
3. Exécutez :
   ```
   ./heroku_deploy.sh
   ```

## ✅ TODO
- [x] Mettre à jour le Dockerfile
- [ ] Ajouter une barre de progression pour le téléchargement

---

🐾 **Développé avec amour par [Tiger-Foxx](https://github.com/Tiger-Foxx) !** 🦊🔥

