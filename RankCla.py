# GoogleSheet
from __future__ import print_function
from msvcrt import LK_LOCK
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
import datetime
import json
import time
import pandas as pd
from bs4 import BeautifulSoup
from prompt_toolkit import print_formatted_text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


# ! CORRIGIR OS UPDATE QUE ESTÃO DUPLICANDO AS MENSAGENS DOS BOTS DISCORD
# TODO Verificar correção dos UPDATES no googlesheet que estão duplicando inserts do BOTDiscord.

data_atualizacao = datetime.datetime.now()
data_atual = data_atualizacao.strftime('%d/%m/%Y')
hora_atual = data_atualizacao.strftime('%H:%M')

data_atualizacao = np.empty((0, 0), int)
data_atualizacao = [f"Atualizado em {data_atual} às {hora_atual}h"]
atualizacao = np.array([data_atualizacao]).tolist()

configs = pd.read_json('configs.json').to_dict('records')
for config in configs:
    cla = np.array(config['clan'])
    mundo = str(config['mundo'])
    grupo_mundo = str(config['grupo_mundo'])
    planilha_id = str(config['planilha_id'])
    range_planilha = str(config['range_planilha'])
    celula_hora_atualizacao = str(config['celula_hora_atualizacao'])
    range_titulo = str(config['range_titulo'])

teste3 = np.empty((0, 1), int)
for titulo_tabela in cla:
    teste3 = np.append(teste3, np.array([[titulo_tabela]]), axis=0).tolist()

url = f"https://forum.mir4global.com/rank?ranktype=1&worldgroupid={grupo_mundo}&worldid={mundo}"

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

option = Options()
option.headless = True

driver = webdriver.Firefox()
driver.get(url)

time.sleep(5)
for i in range(9):
    driver.find_element(by=By.CLASS_NAME, value='btn_flat').click()
    time.sleep(2)

html_conteudo = driver.find_elements(by=By.CLASS_NAME, value="rank_section")[
    2].get_attribute("innerHTML")

soup = BeautifulSoup(html_conteudo, 'html.parser')
tabela = soup.find(name='table')

tabela_completa = pd.read_html(str(tabela))[0]
info_tabela = {}
info_tabela = tabela_completa.to_dict('records')

teste = []
membro_clan = []
clan_ = []
linha_array = np.empty((0, 5), int)
rank_cla = 1
hora_atualizacao = [[time.asctime()]]
for membro in info_tabela:
    for cla_ in cla:
        if membro['Clan'] == cla_:
            membro['Ranking'] = membro['Ranking'].split(' ')
            membro['Ranking'] = membro['Ranking'][0]
            teste.append(membro)
            linha_array = np.append(linha_array,
                                np.array([
                                        [
                                        
                                         rank_cla,
                                         membro['Ranking'],
                                         membro['Character'],
                                         membro['Clan'],
                                         membro['Power Score']
                                        
                                        ]]), axis=0
                                    ).tolist()
            rank_cla = rank_cla+1

js = json.dumps(linha_array)
fp = open('membros.json', 'w')
fp.write(js)
fp.close
driver.quit

def main():
    creds = None
    if os.path.exists('token.json'):

        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        sheet.values().clear(
            spreadsheetId=planilha_id,
            range='Ranking!A4:E150',
            body={}
        ).execute()
        sheet.values().clear(
            spreadsheetId=planilha_id,
            range='Ranking!G5:G9',
            body={}
        ).execute()        
        
        sheet.values().update(
            spreadsheetId=planilha_id,
            range=range_titulo,
            valueInputOption="USER_ENTERED",
            body={"values": teste3}
        ).execute()
        
        sheet.values().update(
            spreadsheetId=planilha_id,
            range='Ranking!A4',
            valueInputOption="USER_ENTERED",
            body={"values": linha_array}
        ).execute()
        sheet.values().update(
            spreadsheetId=planilha_id,
            range=celula_hora_atualizacao,
            valueInputOption="USER_ENTERED",
            body={"values": atualizacao}
        ).execute()
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
    

