'''
Contains handler functions (to be attached to the bot's handlers in the main app.py file)
'''

import google.generativeai as genai
import os, time, random, datetime
from logger.bot_data import bot_data
from utils.messages import PREDEFINED_MESSAGES, load_base_prompt, store_message_in_cloud, HELP_COMMANDS

async def start_conversation(update, context):
    '''
    A handler to start the bot's conversation with the user. 
    '''
    await update.message.reply_text(PREDEFINED_MESSAGES.get('welcome_message'))

async def restart_conversation(update, context):
    '''
    A handler to start the bot's conversation with the user. 
    '''
    user_logger = bot_data.get_logger(update.message.from_user.id)
    user_logger.reset_logger()
    bot_data.save_data()
    await update.message.reply_text(PREDEFINED_MESSAGES.get('reset_conversation'))

async def display_help_menu(update, context):
    items = [f'- {i}: {v}' for i, v in HELP_COMMANDS.items()]
    items = 'I’m glad you’re here! Here’s a gentle reminder of the commands you can use to guide our time together:\n\n' + '\n'.join(items)
    await update.message.reply_text(items)

async def respond(update, context):
    '''
    Handles the rest of the conversation for the user - past the introduction,
    that is
    '''
    user_id, retry = update.message.from_user.id, 0
    user_logger = bot_data.get_logger(user_id)
    if not len(user_logger.messages):
        user_logger.log_message(load_base_prompt(), 'user')
    genai.configure(api_key = os.getenv('GEMINI_API_KEY'))
    chat_model = genai.GenerativeModel('gemini-2.5-flash')
    user_logger.log_message(update.message.text, 'user')
    store_message_in_cloud(user_logger.conversation_id, update.message.text, 'user', datetime.datetime.now())
    while retry < int(os.getenv('RETRY_LIMIT')):
        chat = chat_model.start_chat(history = user_logger.messages)
        response = chat.send_message(update.message.text)
        if isinstance(response, dict):
            if response.get('error') != None:
                time.sleep(random.randint(1, os.getenv('TIMEOUT_WAIT')))
        else:
            user_logger.log_message(response.text, 'model')
            store_message_in_cloud(user_logger.conversation_id, response.text, 'model', datetime.datetime.now())
            break
    await update.message.reply_text(response.text)