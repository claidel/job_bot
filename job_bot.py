from flask import Flask
import threading

class JobBot:
    """Bot Telegram avec Flask pour un hébergement stable sur Render."""

    def __init__(self):
        """Initialise le bot Telegram et le serveur Flask."""
        self.bot = TelegramClient("bot", offreBot.API_ID, offreBot.API_HASH).start(bot_token=offreBot.TELEGRAM_BOT_TOKEN)
        self.client = MongoClient(offreBot.MONGO_URI)
        self.db = self.client["job_database"]
        self.jobs_collection = self.db["jobs"]
        self.categories = ["Informatique / IT", "Finance / Comptabilité", "Communication / Marketing", "Conseil / Stratégie", "Transport / Logistique", "Ingénierie / BTP", "Santé / Médical", "Autre"]
        
        # Serveur Flask pour éviter que Render coupe le bot
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.index)

        # Enregistre les handlers Telegram
        self.register_handlers()

    def index(self):
        """Page d'accueil Flask pour montrer que l'app fonctionne."""
        return "🚀 Bot Telegram est en ligne et fonctionne !"

    def register_handlers(self):
        """Enregistre les handlers du bot."""
        self.bot.on(events.NewMessage(pattern='/start'))(self.start)
        self.bot.on(events.CallbackQuery(pattern=b'get_total_jobs'))(self.send_total_jobs)
        self.bot.on(events.CallbackQuery(pattern=b'category_'))(self.send_category_jobs)
        self.bot.on(events.CallbackQuery(pattern=b'get_all_jobs'))(self.send_all_jobs)

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
