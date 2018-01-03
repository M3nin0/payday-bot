import json
import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ToolBox(object):
    '''
        Classe com utilitários para o funcionamento do bot
    '''
    @staticmethod
    def connect_api(file_json, name_sheet):
        '''
            Método que realiza a comunicação com a planilha do usuário,
            para que seja possível acessar as informações
        '''

        scope = ['https://spreadsheets.google.com/feeds']

        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name('./keys/' + str(file_json), scope)
            client = gspread.authorize(creds)
            return client.open(name_sheet).sheet1
        except BaseException as e:
            print(e)
            return -1
