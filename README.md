Job Bot
Python License: MIT

🚀 Project Title
Job Bot - An automated Python bot designed to search for job offers on Pôle Emploi (France's public employment service) and send real-time notifications via Telegram.

📝 Description
The Job Bot is a lightweight and highly configurable Python application that continuously monitors new job postings on the Pôle Emploi platform. It allows users to define specific keywords and geographical locations to tailor their job search. Upon discovering new offers that match the criteria, the bot sends instant notifications to a designated Telegram chat, ensuring you never miss a relevant opportunity. It cleverly tracks previously notified offers to prevent duplicate messages.

✨ Features
Targeted Job Search: Specifically designed to scrape job offers from Pôle Emploi (France's public employment service).
Customizable Search Parameters: Easily configure keywords and locations in a config.json file to refine your job search.
Telegram Notifications: Receives instant alerts for new job opportunities directly in your specified Telegram chat.
Duplicate Prevention: Intelligently tracks and stores already notified job offers in data.json to prevent sending redundant messages.
Configurable Frequency: Set how often the bot checks for new offers to suit your needs.
Secure Configuration: Utilizes .env files for securely managing sensitive information like your Telegram Bot Token.
⚙️ Installation
Follow these steps to set up and run the Job Bot on your local machine.

Prerequisites
Python 3.x
pip (Python package installer)
Steps
Clone the Repository: First, clone the job_bot repository to your local machine using Git:

git clone https://github.com/claidel/job_bot.git
cd job_bot
Install Dependencies: Install the required Python packages using pip:

pip install -r requirements.txt
This will install requests for HTTP requests and python-dotenv for environment variable management.

Configure Environment Variables: Create a file named .env in the root directory of the project. This file will store your Telegram Bot Token.

TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
How to get a Telegram Bot Token: Talk to @BotFather on Telegram and follow the instructions to create a new bot and obtain its API token.
Configure Search Parameters: Create a file named config.json in the root directory of the project. This file defines your job search criteria and Telegram chat ID.

{
  "keywords": ["développeur", "fullstack"],
  "locations": ["paris", "lyon"],
  "frequency": 3600,
  "telegram_chat_id": "-123456789"
}
keywords: A list of job keywords you are interested in (e.g., "développeur", "data scientist").
locations: A list of locations for job search (e.g., "paris", "lyon", "nantes").
frequency: The interval (in seconds) at which the bot will check for new job offers. For example, 3600 means it will check every hour.
telegram_chat_id: The ID of the Telegram chat where you want to receive notifications.
How to get your Telegram Chat ID: You can use a bot like @getidbot or @userinfobot on Telegram. Start a chat with one of these bots and it will provide your chat ID. If you want to send messages to a group, add the bot to the group and then use one of these bots within the group. Group chat IDs usually start with a -.
🚀 Usage
Once installed and configured, you can run the bot.

Start the Bot: You can run the bot using the provided start.sh script:

./start.sh
Alternatively, you can run it directly with Python:

python3 job_bot.py
Monitoring: The bot will run continuously in the background (if started via a process manager) or in your terminal, checking for new job offers at the specified frequency and sending notifications to your Telegram chat.

Example Telegram Notification: When a new job offer is found, you will receive a message similar to this in your Telegram chat:

💼 New Job Offer!
ID: 123456789
Title: Développeur Fullstack H/F
URL: https://candidat.pole-emploi.fr/offres/recherche/detail/123456789
📜 License
This project is open-source and currently does not have an explicit license file. It is recommended to add a license such as the MIT License to specify terms of use and distribution.

🤝 Contribution Guidelines
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix: git checkout -b feature/your-feature-name or bugfix/fix-something.
Make your changes.
Commit your changes with a clear and concise message.
Push your branch to your forked repository.
Open a Pull Request to the main branch of the original repository, describing your changes in detail.
🔗 Possible Sources
Pôle Emploi API: The bot interacts with the public API endpoint for job search: https://candidat.pole-emploi.fr/offres/api/v1/recherche.
Telegram Bot API: The bot uses the Telegram Bot API for sending messages: https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/sendMessage. You can find more details in the official Telegram Bot API documentation.
