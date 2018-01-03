import logging
import telegram
from time import sleep
from telegram.error import Unauthorized
from telegram.error import NetworkError

class Bot(object):
    def __init__(self):
        self.bot = telegram.Bot('TOKEN')
        self.update_id = None

        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.conversa()

    def conversa(self):
        while True:
            try:
                self._receive_file(self.bot)
            except NetworkError:
                sleep(1)
            except Unauthorized:
                self.update_id += 1

    def _receive_file(self, bot):
        for update in bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1

            if update.message:
                try:
                    file_id = update.message.voice.file_id
                    _json_key = bot.get_file(file_id)
                    _json_key.download(str(file_id) + '.json')
                except BaseException as e:
                    print('Não fez envio de arquivo')

    def send_notify(self, bot):
        pass

if __name__ == '__main__':
    Bot()
