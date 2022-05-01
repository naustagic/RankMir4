# WebScraping de Fórum / Inserção em Google Sheet

Varrer uma página, tratar os dados, filtrar somente as linhas com clã especificado, gerar arquivo com esses dados e também inserir em uma planilha Google Sheet.

## O problema

1. São exibidos todos os jogadores do servidor;
2. A cada 100 jogadores exibidos, precisa-se clicar em "mostrar mais...";
3. São no total 10 páginas, ou seja, 1000 jogadores.

## A solução

1. Abrir o fórum;
2. Descer a página e clicar no "mostrar mais...";
3. Após carregar todas as páginas, armazenar as informações daquela tabela;
4. Tratar as informações daquela tabela;
5. Filtrar o resultado tratado para guardar apenas o clã informado;
6. Aplicar o resultado deste filtro em uma planilha do Google Sheet.

## Pacotes Utilizados

~~~python
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
~~~

![Screenshot_4](https://user-images.githubusercontent.com/103384209/166146076-178cec0c-28f2-4832-afbb-1096a3d45b35.png)
![Screenshot_5](https://user-images.githubusercontent.com/103384209/166146159-077dac4d-c15d-426e-a613-5a81256adc8d.png)
![WebScrapingFuncionando](https://user-images.githubusercontent.com/103384209/166148955-8f46a553-acd6-45d3-bdc7-e34c69520690.gif)
