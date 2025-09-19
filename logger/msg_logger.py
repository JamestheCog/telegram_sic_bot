'''
A utility to contain a custom message logger I built.
'''

import string, random, dotenv
from utils.messages import load_base_prompt

dotenv.load_dotenv()
class Logger():
    def __init__(self):
        self.messages = [{'role' : 'user', 'parts' : [load_base_prompt()]}]
        self.conversation_id = self._create_id()
        self.assistant_prompt = load_base_prompt()
    
    def reset_logger(self):
        self.messages = [{'role' : 'user', 'parts' : [self.assistant_prompt]}]
        self.conversation_id = self._create_id()
    
    def log_message(self, message: str, role: str):
        self.messages.append({'role' : role, 'parts' : [message]})
    
    def to_dict(self):
        '''Serialize Logger data for JSON storage.'''
        return {
            "conversation_id": self.conversation_id,
            "messages": self.messages
        }
    
    @staticmethod
    def _create_id(id_length = 10):
        CHARS = list(string.ascii_letters) + [str(i) for i in range(0, 9)]
        return(''.join(random.sample(CHARS, id_length)))
    
    @classmethod
    def from_dict(cls, data):
        '''Create a Logger instance from JSON data'''
        logger = object.__new__(cls)
        logger.conversation_id = data.get('conversation_id', logger._create_id())
        logger.messages = data.get('messages', [{'role' : 'user', 'parts' : [load_base_prompt()]}])
        logger.assistant_prompt = load_base_prompt()
        return(logger)
