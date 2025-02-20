from telethon import TelegramClient, events, Button
from pymongo import MongoClient
import random
import offreBot  # Fichier contenant API_ID, API_HASH, BOT_TOKEN et MONGO_URI

class JobBot:
    """Bot Telegram permettant d'envoyer des offres d'emploi classées par catégorie."""

    def __init__(self):
        """Initialisation du bot Telegram et connexion à MongoDB."""
        self.bot = TelegramClient("bot", offreBot.API_ID, offreBot.API_HASH).start(bot_token=offreBot.TELEGRAM_BOT_TOKEN)
        
        # Connexion à MongoDB
        self.client = MongoClient(offreBot.MONGO_URI)
        self.db = self.client["job_database"]
        self.jobs_collection = self.db["jobs"]

        # Modèles pour reformuler les offres
        self.templates = [
            "📌 *{title}* chez *{company}* à {location}.\n{resume}\n",
            "🚀 Opportunité : *{title}* !\nEntreprise : *{company}*\n📍 Localisation : {location}\n👉 {resume}\n",
            "🎯 Poste : *{title}*\n🏢 Employeur : *{company}*\n📍 Lieu : {location}\n📜 {resume}\n"
        ]

        # Catégories disponibles
        self.categories = [
            "Informatique / IT", "Finance / Comptabilité", "Communication / Marketing",
            "Conseil / Stratégie", "Transport / Logistique", "Ingénierie / BTP", "Santé / Médical", "Autre"
        ]

        # Enregistrement des handlers
        self.register_handlers()

    def register_handlers(self):
        """Enregistre tous les événements du bot."""
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
        category = event.data.decode().split("_", 1)[1]  # Récupère le nom de la catégorie
        print(f"🔍 Bouton '{category}' cliqué par {chat_id}")

        await self.send_jobs(chat_id, filter_by_category=category)

    async def send_all_jobs(self, event):
        """Envoie toutes les offres disponibles sans distinction de catégorie."""
        chat_id = event.chat_id
        print(f"🔍 Bouton '📩 Toutes les offres' cliqué par {chat_id}")

        await self.send_jobs(chat_id, filter_by_category=None)

    async def send_jobs(self, chat_id, filter_by_category=None):
        """Envoie les offres filtrées par catégorie ou toutes les offres si `filter_by_category` est None."""
        query = {"category": filter_by_category} if filter_by_category else {}
        jobs = self.jobs_collection.find(query)
        total_jobs = self.jobs_collection.count_documents(query)

        if total_jobs == 0:
            await self.bot.send_message(chat_id, f"⚠️ Aucune offre disponible dans la catégorie {filter_by_category}.")
            print(f"❌ Aucune offre trouvée pour {filter_by_category}.")
            return

        await self.bot.send_message(chat_id, f"📊 Nombre d'offres disponibles dans {filter_by_category if filter_by_category else 'toutes les catégories'} : {total_jobs}")

        for job in jobs:
            job_text = random.choice(self.templates).format(
                title=job.get("title", "Titre inconnu"),
                company=job.get("company", "Entreprise inconnue"),
                location=job.get("location", "Lieu inconnu"),
                resume=job.get("resume", "Pas de résumé disponible")
            )

            # Création du bouton "Postuler"
            keyboard = [[Button.url("📤 Postuler", job.get("url", "#"))]]

            # Envoi de l'annonce
            await self.bot.send_message(chat_id, job_text, buttons=keyboard, parse_mode="md")
            print(f"✅ Offre envoyée : {job.get('title', 'Titre inconnu')}")

        await self.bot.send_message(chat_id, "✅ Toutes les offres disponibles ont été envoyées.")
        print(f"✅ Envoi terminé pour {chat_id}")

    def run(self):
        """Démarre le bot."""
        print("🤖 Bot en ligne...")
        self.bot.run_until_disconnected()


# ✅ **Utilisation de la classe**
if __name__ == "__main__":
    job_bot = JobBot()
    job_bot.run()
