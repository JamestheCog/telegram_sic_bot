from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.messages import respond, start_conversation, restart_conversation, display_help_menu
import os, dotenv 

dotenv.load_dotenv()

async def handle_message(update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler('start', start_conversation))
    application.add_handler(CommandHandler('help', display_help_menu))
    application.add_handler(CommandHandler('restart', restart_conversation))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Start the bot
    print('running...')
    application.run_polling()

if __name__ == "__main__":
    main()