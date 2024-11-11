from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import re
from selenium.common.exceptions import TimeoutException
import pandas as pd
from datetime import datetime

Configuração do driver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
options.add_argument("--log-level=3")

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

# Lista para armazenar as informações de kills de cada partida
dados_kills = []

# Passo 2 e 3: Para cada partida, extrair URLs de heatmaps e contar kills
for url_partida, data_partida in urls_partidas:
    urls_heatmaps = extrair_urls_heatmaps(url_partida)
    armas_kills_partida = contar_kills_por_arma(urls_heatmaps)

    # Armazenar kills por arma para a data específica
    for arma, kills in armas_kills_partida.items():
        dados_kills.append({'arma': arma, 'kills': kills, 'data': data_partida})

# Criando um DataFrame com as informações
df = pd.DataFrame(dados_kills)

# Agrupando o DataFrame por 'data' e 'arma' e somando as kills
df = df.groupby(['data', 'arma'], as_index=False)['kills'].sum()

# Filtrando para remover linhas onde a arma é igual a 'ALL'
df = df[df['arma'] != 'All']

# Exibindo o DataFrame filtrado e consolidado
print("\nDataFrame de kills por arma e data:")
print(df)

# Renomeando as colunas para o padrão desejado
df = df.rename(columns={"data": "Data", "arma": "Arma", "kills": "kill"})

# Usar ponto e vírgula como separador
df.to_csv("kills_por_arma_e_data.csv", index=False, encoding="utf-8", sep=";")
