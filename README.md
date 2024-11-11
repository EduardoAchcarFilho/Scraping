readme_content = """
# Projeto de Web Scraping para Estatísticas de Partidas de Jogos

Este projeto realiza a coleta de dados de partidas de jogos em um site específico, utilizando bibliotecas de web scraping e armazena as informações coletadas em um banco de dados SQL Server.

## Bibliotecas Utilizadas

Este projeto utiliza as seguintes bibliotecas:

- **selenium** - Para automatizar a navegação e extração de dados da web.
- **webdriver_manager.chrome** - Para gerenciar o driver do Chrome automaticamente.
- **BeautifulSoup** - Para fazer o parsing do HTML e localizar elementos específicos.
- **pandas** - Para manipulação e estruturação de dados em tabelas.

## Estrutura do Banco de Dados

O banco de dados é estruturado em três tabelas principais:

### 1. Tabela de Partidas (Fato)

Armazena informações básicas sobre cada partida extraída.

```sql
CREATE TABLE partidas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    data DATETIME,
    url NVARCHAR(500)
);
