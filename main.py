# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot, ChatAction
import json
import logging
import os
import subprocess
from dotenv import dotenv_values
from time import sleep

# Configuration des emojis de renard
RENARD = "🦊"
VERROU = "🔒"
MUSIQUE = "🎵"
ERREUR = "❌"
CHARGEMENT = "⏳"
SUCCES = "✅"
TELEVERSEMENT = "📤"

logging.basicConfig(
    format=f'{RENARD} %(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

with open("config.json", "r") as fichier_config:
    config = json.load(fichier_config)


def sauvegarder_config():
    with open("config.json", "w") as fichier_config:
        json.dump(config, fichier_config)


try:
    token = dotenv_values(".env")["TELEGRAM_TOKEN"]
except Exception:
    token = os.environ['TELEGRAM_TOKEN']

updater = Updater(token)
dispatcher = updater.dispatcher


def envoyer_action(chat_id, action):
    """Affiche une action en cours (typing, upload_audio, etc.)"""
    updater.bot.send_chat_action(chat_id=chat_id, action=action)


def afficher_progression(chat_id, progression, total=10):
    """Affiche une barre de progression stylisée"""
    barre = f"{RENARD} [{'🟧' * progression}{'⬜' * (total - progression)}] {progression * 10}%"
    updater.bot.send_message(chat_id=chat_id, text=barre)


def gerer_message(bot, update):
    if config["AUTH"]["ENABLE"]:
        authentifier(bot, update)
    telecharger_musique(bot, update)


def telecharger_musique(bot, update):
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id
    utilisateur = update.message.chat.username

    logging.info(f'Début du traitement pour {utilisateur}')
    envoyer_action(chat_id, ChatAction.TYPING)

    try:
        url = update.effective_message.text
        dossier_temp = f".temp_{message_id}_{chat_id}"

        # Création du dossier temporaire
        os.makedirs(dossier_temp, exist_ok=True)

        # Configuration du processus de téléchargement
        commande = 'spotdl' if config["SPOTDL_DOWNLOADER"] else 'spotifydl'
        processus = subprocess.Popen(
            [commande, url],
            cwd=dossier_temp,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # Envoi de la progression
        bot.send_message(chat_id, f"{CHARGEMENT} Recherche de la musique... {RENARD}")
        derniere_progression = 0

        while True:
            sortie = processus.stdout.readline()
            if sortie == '' and processus.poll() is not None:
                break
            if "progress" in sortie.lower():
                progression_actuelle = int(sortie.split('%')[0].strip()[-2:].strip()) // 10
                if progression_actuelle != derniere_progression:
                    afficher_progression(chat_id, progression_actuelle)
                    derniere_progression = progression_actuelle

        # Envoi des fichiers
        envoyer_action(chat_id, ChatAction.UPLOAD_AUDIO)
        fichiers = [os.path.join(dp, f) for dp, _, fn in os.walk(dossier_temp)
                    for f in fn if f.endswith('.mp3')]

        if not fichiers:
            raise FileNotFoundError(f"{ERREUR} Aucun fichier trouvé")

        bot.send_message(chat_id, f"{TELEVERSEMENT} Envoi de {len(fichiers)} fichier(s)... {MUSIQUE}")

        for fichier in fichiers:
            with open(fichier, 'rb') as audio:
                bot.send_audio(chat_id=chat_id, audio=audio, timeout=1000)

        bot.send_message(chat_id, f"{SUCCES} Téléchargement terminé ! {RENARD}")

    except Exception as e:
        bot.send_message(chat_id, f"{ERREUR} Erreur : {str(e)}")
        logging.error(f"Erreur : {str(e)}")
    finally:
        # Nettoyage du dossier temporaire
        if os.path.exists(dossier_temp):
            for root, dirs, files in os.walk(dossier_temp, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(dossier_temp)


def authentifier(bot, update):
    chat_id = update.effective_message.chat_id
    utilisateur = update.message.chat.username

    if chat_id in config["AUTH"]["USERS"]:
        return  # Déjà authentifié

    if update.effective_message.text == config["AUTH"]["PASSWORD"]:
        config["AUTH"]["USERS"].append(chat_id)
        sauvegarder_config()
        bot.send_message(chat_id, f"{VERROU} Authentification réussie ! Profitez-en ! {RENARD}")
        logging.info(f'Nouvel utilisateur authentifié : {utilisateur}')
        return

    # Demande d'authentification
    bot.send_message(
        chat_id=chat_id,
        text=f"{VERROU} Ce bot est privé. Veuillez entrer le mot de passe :"
    )
    raise PermissionError("Accès non autorisé")


# Gestion des erreurs
def gerer_erreur(bot, update, error):
    logging.error(f"Erreur non traitée : {error}")
    bot.send_message(update.effective_chat.id, f"{ERREUR} Une erreur est survenue : {error}")


dispatcher.add_handler(MessageHandler(Filters.text, gerer_message))
dispatcher.add_error_handler(gerer_erreur)

# Message de démarrage
updater.bot.send_message(chat_id=config["ADMIN_CHAT_ID"], text=f"{RENARD} Le bot Fox Music est opérationnel !")

updater.start_polling(poll_interval=0.8)
updater.idle()