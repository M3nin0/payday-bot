import logging
import telegram
import datetime

from time import sleep
from toolbox import ToolBox
from threading import Thread

from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler

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
                update.message.reply_text('Erro ao tentar se conectar com a planilha de gastos, insira o arquivo novamente')
            else:
                update.message.reply_text('Pronto! Agora já tenho acesso a suas faturas, logo menos estarei verificando e enviando notificações sobre suas faturas para você')

                # Cria thread para evitar que o bot fique inutilizavel durante o processo de verificação
                thread = Thread(target = self.send_notify, args = (bot, update, table))
                thread.start()

        except BaseException as e:
            print(e)

    def send_notify(self, bot, update, table):
        # Faz verificação e envia notificação se necessário
        while True:
            update.message.reply_text('Estou fazendo a verificação de suas faturas agora')
            itens_table = table.get_all_values()[1:]
            # Data do dia atual
            hoje = datetime.date.today()
            for fatura in itens_table:
                if fatura[-1] != 'Fechado':
                    vencimento = fatura[2].split('-')[::-1]
                    data_vencimento = datetime.date(int(vencimento[0]),
                                                    int(vencimento[1]),
                                                    int(vencimento[2]))
                    atraso = (hoje - data_vencimento).days
                    if atraso > int(fatura[-2]):
                        update.message.reply_text('A seguinte fatura precisa ser paga: \n ' +
                                                  '- Data de emissão: ' + fatura[1] +
                                                  '\n - Data de vencimento: ' + fatura[2] +
                                                  '\n - Nome da empresa: ' + fatura[3] +
                                                  '\n - Valor da conta: ' + fatura[4] +
                                                '\n - Status da fatura: ' + fatura[6])
            # Entra em espera durante um dia
            sleep(86400)

if __name__ == '__main__':
    Bot()
