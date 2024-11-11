# Web Scraping de Estatísticas de Partidas e Kills - HLTV

Este projeto realiza a raspagem de dados do site HLTV.org para extrair informações sobre partidas de e-sports, mais especificamente de torneios de CS:GO, incluindo dados de kills por tipo de arma a partir dos heatmaps de cada partida. Os dados extraídos são salvos em um banco de dados SQL Server.

## Funcionalidades

- **Extração de URLs de partidas**: O script acessa a página de partidas do HLTV.org e extrai os links para partidas que ocorreram dentro de um intervalo de datas específico.
- **Extração de URLs de Heatmaps**: Para cada partida, o script visita a página da partida e extrai a URL do heatmap associado.
- **Contagem de kills por tipo de arma**: A partir dos links de heatmaps, o script conta a quantidade de kills por tipo de arma e armazena esses dados.
- **Armazenamento em banco de dados SQL Server**: Todos os dados extraídos (partidas, armas e kills) são armazenados em um banco de dados SQL Server.

## Requisitos

- **Python 3.x**
- Bibliotecas:
  - `selenium`: Para automação de navegação e raspagem de dados no site.
  - `beautifulsoup4`: Para parsing do HTML das páginas.
  - `pyodbc`: Para conectar ao banco de dados SQL Server e executar comandos SQL.
  - `webdriver-manager`: Para gerenciar o driver do Chrome.
  - `re`: Para utilizar expressões regulares e extrair os dados necessários.


## Estrutura do Projeto
O código está estruturado para realizar a raspagem de forma automatizada e salvar os resultados no banco de dados. As principais funções incluem:

1. extrair_urls_partidas(data_inicio, data_fim)
Acessa a página de partidas e extrai os links das partidas que ocorreram entre as datas data_inicio e data_fim.

2. extrair_urls_heatmaps(url_partida)
Acessa a página de uma partida e extrai a URL do heatmap associado.

3. contar_kills_por_arma(urls_heatmaps)
Acessa os links dos heatmaps e conta a quantidade de kills por tipo de arma.

4. Inserção de Dados no Banco de Dados
Para cada partida, o script insere os dados no banco de dados SQL Server, criando registros para a partida, as armas e as kills.

# Banco de Dados
O banco de dados utilizado é o SQL Server, e ele deve ter as seguintes tabelas para armazenar os dados:

# Tabela partidas
`id`: Identificador único da partida.
`data`: Data da partida.
`url`: URL da partida no site HLTV.
# Tabela armas
id: Identificador único da arma.
nome: Nome da arma.
# Tabela kills
id: Identificador único do registro de kill.
partida_id: ID da partida relacionada.
arma_id: ID da arma utilizada.
kills: Quantidade de kills feitas com a arma.

# Como Usar
1. Configuração do Banco de Dados
Configure a variável DADOS_CONEXAO com as credenciais do seu banco de dados SQL Server.

2. Execução
Defina o intervalo de datas desejado nas variáveis data_inicio e data_fim (formato dd/mm/yy).
Execute o script para iniciar o processo de raspagem e inserção dos dados no banco.
3. Ajustes
Caso o site HLTV.org tenha alterações em seu layout, pode ser necessário ajustar o código para encontrar os elementos corretos no HTML.

## Exemplo de Execução

# Definindo as datas de início e fim para o intervalo
data_inicio = datetime.strptime("30/3/24", "%d/%m/%y")
data_fim = datetime.strptime("31/3/24", "%d/%m/%y")

# Passo 1: Extrair URLs de partidas dentro do intervalo de datas
urls_partidas = extrair_urls_partidas(data_inicio, data_fim)

# Passo 2 e 3: Para cada partida, extrair URLs de heatmaps e contar kills
for url_partida, data_partida in urls_partidas:
    # Inserir partida na tabela de partidas
    cursor.execute("INSERT INTO partidas (data, url) VALUES (?, ?)", data_partida, url_partida)
    
    urls_heatmaps = extrair_urls_heatmaps(url_partida)
    armas_kills_partida = contar_kills_por_arma(urls_heatmaps)

    # Armazenar armas e kills
    for arma, kills in armas_kills_partida.items():
        cursor.execute("IF NOT EXISTS (SELECT 1 FROM armas WHERE nome = ?) INSERT INTO armas (nome) VALUES (?)", arma, arma)
        cursor.execute("SELECT id FROM armas WHERE nome = ?", arma)
        arma_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO kills (partida_id, arma_id, kills) VALUES ((SELECT id FROM partidas WHERE url = ?), ?, ?)", url_partida, arma_id, kills)

# Commit das transações e fechamento da conexão
conn.commit()
cursor.close()
conn.close()




### Para instalar as dependências necessárias, use o seguinte comando:

```bash
pip install selenium beautifulsoup4 pyodbc webdriver-manager

