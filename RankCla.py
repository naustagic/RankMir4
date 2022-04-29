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

data = np.empty_like
data = datetime.datetime.now()
data_atual = data.strftime('%d/%m/%Y')
hora_atual = data.strftime('%H:%M')

data = [f"Atualizado em {data_atual} às {hora_atual}h"]
data_atualizacao = np.array([data]).tolist()

configs = pd.read_json('configs.json').to_dict('records')
for config in configs:
    cla = np.array(config['clan'])
    mundo = str(config['mundo'])
    grupo_mundo = str(config['grupo_mundo'])
    planilha_id = str(config['planilha_id'])
    range_titulo = str(config['range_titulo'])
    range_planilha = str(config['range_planilha'])
    atualizado_em = str(config['atualizado_em'])

url = f"https://forum.mir4global.com/rank?ranktype=1&worldgroupid={grupo_mundo}&worldid={mundo}"

multi_cla = np.empty((0, 1), int)
for array_cla in cla:
    multi_cla = np.append(multi_cla, np.array([[array_cla]]), axis=0).tolist()

option = Options()
option.headless = True
driver = webdriver.Firefox()
driver.get(url)

time.sleep(5)

for i in range(9):
    driver.find_element(by=By.CLASS_NAME, value='btn_flat').click()
    time.sleep(2)

html_conteudo = driver.find_elements(
    by=By.CLASS_NAME, 
    value="rank_section"
    )[2].get_attribute("innerHTML")
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
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
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
            body={"values": multi_cla}
        ).execute()
        
        sheet.values().update(
            spreadsheetId=planilha_id,
            range='Ranking!A4',
            valueInputOption="USER_ENTERED",
            body={"values": linha_array}
        ).execute()
        sheet.values().update(
            spreadsheetId=planilha_id,
            range=atualizado_em,
            valueInputOption="USER_ENTERED",
            body={"values": data_atualizacao}
        ).execute()
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
    

