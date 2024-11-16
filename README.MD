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

1. **extrair_urls_partidas(data_inicio, data_fim)**
Acessa a página de partidas e extrai os links das partidas que ocorreram entre as datas data_inicio e data_fim.

2. **extrair_urls_heatmaps(url_partida)**
Acessa a página de uma partida e extrai a URL do heatmap associado.

3. **contar_kills_por_arma(urls_heatmaps)**
Acessa os links dos heatmaps e conta a quantidade de kills por tipo de arma.

4. **Inserção de Dados no Banco de Dados**
Para cada partida, o script insere os dados no banco de dados SQL Server, criando registros para a partida, as armas e as kills.

### Banco de Dados
O banco de dados utilizado é o SQL Server, e ele deve ter as seguintes tabelas para armazenar os dados:

### Tabela partidas
 - `id`: Identificador único da partida.
 - `data`: Data da partida.
 - `url`: URL da partida no site HLTV.
### Tabela armas
 - `id`: Identificador único da arma.
 - `nome`: Nome da arma.
### Tabela kills
 - `id`: Identificador único do registro de kill.
 - `partida_id`: ID da partida relacionada.
 - `arma_id`: ID da arma utilizada.
 - `kills`: Quantidade de kills feitas com a arma.

Obs: Foi usado um padrão SNOWFLAKE na estrutura da modelagem do banco de dados. 

### Como Usar
1. Configuração do Banco de Dados
Configure a variável DADOS_CONEXAO com as credenciais do seu banco de dados SQL Server.

2. Execução
Defina o intervalo de datas desejado nas variáveis data_inicio e data_fim (formato dd/mm/yy).
Execute o script para iniciar o processo de raspagem e inserção dos dados no banco.
3. Ajustes
Caso o site HLTV.org tenha alterações em seu layout, pode ser necessário ajustar o código para encontrar os elementos corretos no HTML.


### Para instalar as dependências necessárias, use o seguinte comando:

```bash
pip install selenium beautifulsoup4 pyodbc webdriver-manager

