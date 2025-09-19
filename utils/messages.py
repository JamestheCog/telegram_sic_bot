'''
A module to contain functions for responding to user inputs - Telegram messages if you will!
'''

import os, datetime, sqlitecloud, dotenv
from cryptography.fernet import Fernet
dotenv.load_dotenv()

# === Constants ===
PREDEFINED_MESSAGES = {'welcome_message' : 'Welcome! I’m here for you—feel free to share a message whenever you’re ready to begin our conversation. There’s no rush, and I’m all ears.',
                       'reset_conversation' : 'Your conversation has been gently reset. Do reset the conversation with "Clear history"!'}
HELP_COMMANDS = {
    '/start' : 'Begin conversing with the chatbot',
    '/help' : 'Displays a list of commands for the chatbot',
    '/restart' : 'Restarts the conversation'
}

# === Functions ===
def store_message_in_cloud(id, message, role, time = datetime.datetime.now()):
    '''Store a message in the cloud database'''
    connector = sqlitecloud.connect(os.getenv('SQLITE_CONNECTOR'))
    cursor = connector.cursor()
    cursor.execute(f"INSERT INTO {os.getenv('TABLE_NAME')} VALUES (?, ?, ?, ?)", (id, time, role, message))
    cursor.close()

def load_base_prompt(fernet_key = os.getenv('FERNET_DECRYPTION_KEY')):
    '''
    Given a fernet_key, decrypt the base prompt
    '''
    if not fernet_key.strip():
        raise ValueError('`FERNET_DECRYPTION_KEY` environment variable not set.')
    decryptor = Fernet(rf'{fernet_key}')
    with open('./prompts/base_bot_prompt.txt', 'rb') as encrypted:
        return(decryptor.decrypt(encrypted.read()).decode('utf-8'))