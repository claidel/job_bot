from flask import Flask
import threading
from telethon import TelegramClient, events, Button
from pymongo import MongoClient
import offreBot  # Fichier contenant API_ID, API_HASH, BOT_TOKEN et MONGO_URI
import random

class JobBot:
    """Bot Telegram avec Flask pour hébergement sur Render."""

    def __init__(self):
        """Initialise le bot Telegram et le serveur Flask."""
        self.bot = TelegramClient("bot", offreBot.API_ID, offreBot.API_HASH).start(bot_token=offreBot.TELEGRAM_BOT_TOKEN)
        self.client = MongoClient(offreBot.MONGO_URI)
        self.db = self.client["job_database"]
        self.jobs_collection = self.db["jobs"]
        
        # Catégories disponibles
        self.categories = [
            "Informatique / IT", "Finance / Comptabilité", "Communication / Marketing",
            "Conseil / Stratégie", "Transport / Logistique", "Ingénierie / BTP", "Santé / Médical", "Autre"
        ]

        # Serveur Flask pour éviter la coupure de Render
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.index)

        # Enregistre les handlers Telegram
        self.register_handlers()

    def index(self):
        """Page d'accueil Flask pour indiquer que le bot est actif."""
        return "🚀 Bot Telegram en ligne et actif !"

    def register_handlers(self):
        """Enregistre les handlers du bot."""
        self.bot.on(events.NewMessage(pattern='/start'))(self.start)
        self.bot.on(events.CallbackQuery(pattern=b'get_total_jobs'))(self.send_total_jobs)
        self.bot.on(events.CallbackQuery(pattern=b'category_'))(self.send_category_jobs)
        self.bot.on(events.CallbackQuery(pattern=b'get_all_jobs'))(self.send_all_jobs)

    async def start(self, event):
        """Affiche un bouton pour recevoir les annonces après /start."""
        chat_id = event.chat_id
        print(f"✅ Commande /start reçue de {chat_id}")

        welcome_text = "👋 Bienvenue sur le bot d'offres d'emploi !\nCliquez sur le bouton ci-dessous pour voir les annonces disponibles."
        keyboard = [[Button.inline("📩 Recevoir les annonces", data="get_total_jobs")]]

        await self.bot.send_message(chat_id, welcome_text, buttons=keyboard)
        print("✅ Bouton 'Recevoir les annonces' envoyé")

    async def send_total_jobs(self, event):
        """Affiche le total des offres et propose les catégories."""
        chat_id = event.chat_id
        print(f"🔍 Bouton '📩 Recevoir les annonces' cliqué par {chat_id}")

        total_jobs = self.jobs_collection.count_documents({})
        print(f"📊 Nombre total d'offres disponibles : {total_jobs}")

        if total_jobs == 0:
            await self.bot.send_message(chat_id, "⚠️ Aucune offre d'emploi disponible pour le moment.")
            print("❌ Aucune offre trouvée dans MongoDB.")
            return

        await self.bot.send_message(chat_id, f"📊 Nombre total d'offres disponibles : {total_jobs}\nVeuillez sélectionner une catégorie ci-dessous :")

        # Créer des boutons de catégorie
        category_buttons = [[Button.inline(cat, data=f"category_{cat}")] for cat in self.categories]
        category_buttons.append([Button.inline("📩 Toutes les offres", data="get_all_jobs")])

        await self.bot.send_message(chat_id, "📌 Sélectionnez une catégorie :", buttons=category_buttons)
        print("✅ Boutons de catégorie envoyés")

    async def send_category_jobs(self, event):
        """Envoie uniquement les offres d'une catégorie sélectionnée."""
        chat_id = event.chat_id
        category = event.data.decode().split("_", 1)[1]  # Récupère la catégorie
        print(f"🔍 Bouton '{category}' cliqué par {chat_id}")

        await self.send_jobs(chat_id, filter_by_category=category)

    async def send_all_jobs(self, event):
        """Envoie toutes les offres disponibles sans distinction de catégorie."""
        chat_id = event.chat_id
        print(f"🔍 Bouton '📩 Toutes les offres' cliqué par {chat_id}")

        await self.send_jobs(chat_id, filter_by_category=None)

    async def send_jobs(self, chat_id, filter_by_category=None):
        """Envoie les offres filtrées par catégorie ou toutes les offres si `filter_by_category` est None."""
        
        if filter_by_category:
            jobs = self.jobs_collection.find({"category": filter_by_category})
            print(f"📊 Recherche des offres dans la catégorie : {filter_by_category}")
        else:
            jobs = self.jobs_collection.find({})
            print(f"📊 Recherche de toutes les offres disponibles.")

        total_jobs = self.jobs_collection.count_documents({"category": filter_by_category} if filter_by_category else {})

        if total_jobs == 0:
            await self.bot.send_message(chat_id, f"⚠️ Aucune offre disponible dans la catégorie {filter_by_category}.")
            print(f"❌ Aucune offre trouvée pour {filter_by_category}.")
            return

        await self.bot.send_message(chat_id, f"📊 Nombre d'offres disponibles dans {filter_by_category if filter_by_category else 'toutes les catégories'} : {total_jobs}")

        for job in jobs:
            job_text = f"📌 *{job.get('title', 'Titre inconnu')}*\n🏢 {job.get('company', 'Entreprise inconnue')}\n📍 {job.get('location', 'Lieu inconnu')}\n\n📜 {job.get('resume', 'Pas de résumé disponible')}"
            keyboard = [[Button.url("📤 Postuler", job.get("url", "#"))]]

            await self.bot.send_message(chat_id, job_text, buttons=keyboard, parse_mode="md")
            print(f"✅ Offre envoyée : {job.get('title', 'Titre inconnu')}")

        await self.bot.send_message(chat_id, "✅ Toutes les offres disponibles ont été envoyées.")
        print(f"✅ Envoi terminé pour {chat_id}")

    def run(self):
        """Démarre le bot et Flask simultanément."""
        threading.Thread(target=self.run_flask).start()
        print("🤖 Bot Telegram en ligne...")
        self.bot.run_until_disconnected()

    def run_flask(self):
        """Démarre le serveur Flask sur le port 10000 (Render l'exige)."""
        print("🌍 Serveur Flask démarré sur le port 10000...")
        self.app.run(host="0.0.0.0", port=10000)

# ✅ Lancer le bot
if __name__ == "__main__":
    job_bot = JobBot()
    job_bot.run()
