from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from collections import defaultdict
import pyodbc
import time
import re
from datetime import datetime
import urllib

# Configuração do driver do Chrome
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
options.add_argument("--log-level=3")

# Configuração de conexão com o banco de dados
DADOS_CONEXAO = (
    "Driver={SQL Server};"
    "Server=DUXPC;"  # Nome do servidor
    "Database=scraping;"  # Nome do banco de dados
    "Trusted_Connection=yes;"  # Usando autenticação do Windows
)

# Codifica os parâmetros de conexão
params = urllib.parse.quote_plus(DADOS_CONEXAO)

# Conexão com o SQL Server
conn = pyodbc.connect(DADOS_CONEXAO)
cursor = conn.cursor()

# Função para extrair URLs de partidas em um intervalo de datas
def extrair_urls_partidas(data_inicio, data_fim):
    urls_partidas = []
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url_pagina_principal = "https://www.hltv.org/stats/matches?matchType=Majors"
        driver.get(url_pagina_principal)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        tabela_partidas = soup.find("table", class_="stats-table matches-table no-sort")
        
        if tabela_partidas:
            classes_desejadas = ["group-2 first", "group-2", "group-1 first", "group-1"]
            grupo_partidas = tabela_partidas.find_all("tr", class_=classes_desejadas)

            for partida in grupo_partidas:
                div_com_data = partida.find("div", {"class": "time", "data-time-format": "d/M/yy"})
                
                if div_com_data:
                    # Converte a data da partida para datetime
                    data_partida = datetime.strptime(div_com_data.get_text(strip=True), '%d/%m/%y')

                    # Verifica se a data da partida está dentro do intervalo
                    if data_inicio <= data_partida <= data_fim:
                        link_relativo = div_com_data.find_parent("a")["href"]
                        urls_partidas.append((f"https://www.hltv.org{link_relativo}", data_partida))
        else:
            print("Tabela de partidas não encontrada.")
            
    finally:
        driver.quit()

    return urls_partidas

# Função para extrair URLs de heatmaps das partidas encontradas
def extrair_urls_heatmaps(url_partida):
    urls_heatmaps = []
    driver = webdriver.Chrome(service=service, options=options)
    
    local_wait = WebDriverWait(driver, 15)  # Aumentando o tempo de espera para 15 segundos
    
    try:
        driver.get(url_partida)
        
        # Espera até que o elemento 'stats-top-menu' esteja visível
        local_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.stats-top-menu")))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        stats_top_menu = soup.find("div", class_="stats-top-menu")
        
        if stats_top_menu:
            heatmaps_link = stats_top_menu.find("a", string="Heatmaps")
            if heatmaps_link:
                href = heatmaps_link.get("href")
                urls_heatmaps.append(f"https://www.hltv.org{href}")
        else:
            print(f"Menu de stats não encontrado para a partida: {url_partida}")

    except TimeoutException:
        print(f"Elemento 'stats-top-menu' não encontrado para a partida: {url_partida}")
        
    finally:
        driver.quit()

    return urls_heatmaps

# Função para contar kills por tipo de arma a partir das URLs de heatmaps
def contar_kills_por_arma(urls_heatmaps):
    armas_kills = defaultdict(int)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        for url in urls_heatmaps:
            driver.get(url)
            time.sleep(10)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            select_options = soup.find_all("option", selected="selected")

            for option in select_options:
                texto_option = option.get_text(strip=True)
                
                # Usar regex para extrair o nome da arma e a quantidade de kills
                match = re.match(r"(.+?) \((\d+)\)", texto_option)
                if match:
                    arma = match.group(1)  # Nome da arma
                    kills = int(match.group(2))  # Quantidade de kills
                    armas_kills[arma] += kills  # Somar kills ao total para a arma
                    
    finally:
        driver.quit()
        
    return armas_kills

# Definindo as datas de início e fim para o intervalo
data_inicio = datetime.strptime("30/3/24", "%d/%m/%y")
data_fim = datetime.strptime("31/3/24", "%d/%m/%y")

# Passo 1: Extrair URLs de partidas dentro do intervalo de datas
urls_partidas = extrair_urls_partidas(data_inicio, data_fim)

# Listas para armazenar as informações extraídas
dados_partidas = []
dados_armas = []
dados_kills = []

# Passo 2 e 3: Para cada partida, extrair URLs de heatmaps e contar kills
for url_partida, data_partida in urls_partidas:
    # Inserir partida na tabela de partidas
    cursor.execute("INSERT INTO partidas (data, url) VALUES (?, ?)", data_partida, url_partida)
    
    urls_heatmaps = extrair_urls_heatmaps(url_partida)
    armas_kills_partida = contar_kills_por_arma(urls_heatmaps)

    # Armazenar armas e kills
    for arma, kills in armas_kills_partida.items():
        # Inserir arma na tabela de armas (somente se não existir)
        cursor.execute("IF NOT EXISTS (SELECT 1 FROM armas WHERE nome = ?) INSERT INTO armas (nome) VALUES (?)", arma, arma)
        cursor.execute("SELECT id FROM armas WHERE nome = ?", arma)
        arma_id = cursor.fetchone()[0]

        # Inserir kills na tabela de kills
        cursor.execute("INSERT INTO kills (partida_id, arma_id, kills) VALUES ((SELECT id FROM partidas WHERE url = ?), ?, ?)", url_partida, arma_id, kills)

    dados_partidas.append((url_partida, data_partida))
    dados_armas.extend(armas_kills_partida.keys())
    dados_kills.extend(armas_kills_partida.values())

# Commit das transações e fechamento da conexão
conn.commit()
cursor.close()
conn.close()