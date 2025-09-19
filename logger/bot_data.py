import os, json
from logger.msg_logger import Logger

class BotData():
    def __init__(self, file_path = './logger/user_data/bot_data.json'):
        self.file_path = file_path
        self.loggers = {}
        self.load_data()
    
    def load_data(self):
        '''Loads data from the bot_data.json() file (if it exists)'''
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as raw:
                user_data = json.load(raw)
                self.loggers = {int(k) : Logger.from_dict(v) for k, v in user_data.items()}
        else:
            self.loggers = {}
    
    def save_data(self):
        '''Save the data to a JSON file'''
        data = {str(k) : v.to_dict() for k, v in self.loggers.items()}
        with open(self.file_path, 'w') as raw_data:
            json.dump(data, raw_data)
    
    def get_logger(self, user_id):
        '''Get or create a Logger for a user'''
        if user_id not in self.loggers:
            self.loggers[user_id] = Logger()
            self.save_data()
        return(self.loggers[user_id])

bot_data = BotData()