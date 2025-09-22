from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.messages import respond, start_conversation, restart_conversation, display_help_menu
import os, dotenv, logging
from logger.bot_data import bot_data

dotenv.load_dotenv()

application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

# Add handlers for commands and messages
application.add_handler(CommandHandler('start', start_conversation))
application.add_handler(CommandHandler('help', display_help_menu))
application.add_handler(CommandHandler('restart', restart_conversation))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

# Enable logging for debugging purposes when needed:
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info('Application started...')
    logger.info(f"Application is running at: {os.getenv('WEBHOOK_URL')}")
    application.run_webhook(
        listen = "0.0.0.0",
        port = int(10000),  # Render default port
        url_path = "webhook",
        webhook_url = os.getenv('WEBHOOK_URL')
    )