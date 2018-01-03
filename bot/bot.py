import logging
import telegram
from time import sleep
from toolbox import ToolBox
from telegram.error import Unauthorized
from telegram.error import NetworkError

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class Bot(object):
    def __init__(self):
        self.updater = Updater('TOKEN')
        self.update_id = None

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.dp = self.updater.dispatcher

        # Adicionando os comandos
        self.dp.add_handler(CommandHandler("start", self._init_config))
        # Filtrando o tipo por document
        self.dp.add_handler(MessageHandler(Filters.document, self._receive_file))

        # Inicia bot
        self.updater.start_polling()
        self.updater.idle()

    def _init_config(self, bot, update):
        try:
            self.update_id = bot.get_updates()[0].update_id
        except BaseException as e:
            self.update_id = None

        update.message.reply_text('Olá! Vou auxiliar você a realizar as configurações, \
                                  para que eu possa acessar suas faturas e te lembrar delas =D')
        update.message.reply_text('Primeiro insira o arquivo .json com as credênciais de sua API do Google')

    def _receive_file(self, bot, update):
        table = -1
        try:
            # Recebe o arquivo .json e faz a conexão com a planilha do usuário
            file_id = update.message.document.file_id
            _json_key = bot.get_file(file_id)
            _json_key.download('keys/' + str(file_id) + '.json')

            table = ToolBox.connect_api(str(file_id) + '.json', 'faturas')
            if table == -1:
                print(table)
                update.message.reply_text('Erro ao tentar se conectar com a planilha de gastos, insira o arquivo novamente')
            else:
                print(table)
                update.message.reply_text('Pronto! Agora já tenho acesso a suas faturas, logo menos estarei verificando e enviando notificações para você')
        except BaseException as e:
            print(e)

    def send_notify(self, bot, update):
        pass

if __name__ == '__main__':
    Bot()
