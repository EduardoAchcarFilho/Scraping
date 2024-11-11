Projeto de Web Scraping para Estatísticas de Partidas de Jogos
Este projeto realiza a coleta de dados de partidas de jogos em um site específico, utilizando bibliotecas de web scraping e armazena as informações coletadas em um banco de dados SQL Server.

Bibliotecas Utilizadas
Este projeto utiliza as seguintes bibliotecas:

selenium - Para automatizar a navegação e extração de dados da web.
webdriver_manager.chrome - Para gerenciar o driver do Chrome automaticamente.
BeautifulSoup - Para fazer o parsing do HTML e localizar elementos específicos.
pandas - Para manipulação e estruturação de dados em tabelas.
Estrutura do Banco de Dados
O banco de dados é estruturado em três tabelas principais:

1. Tabela de Partidas (Fato)
Armazena informações básicas sobre cada partida extraída.

sql
Copiar código
CREATE TABLE partidas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    data DATETIME,
    url NVARCHAR(500)
);
id: Identificador único da partida.
data: Data da partida.
url: URL da página com informações detalhadas sobre a partida.
2. Tabela de Armas (Dimensão)
Armazena o nome de cada tipo de arma identificada nas partidas.

sql
Copiar código
CREATE TABLE armas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100)
);
id: Identificador único da arma.
nome: Nome da arma.
3. Tabela de Kills (Fato)
Armazena o número de kills de cada tipo de arma em cada partida.

sql
Copiar código
CREATE TABLE kills (
    id INT IDENTITY(1,1) PRIMARY KEY,
    partida_id INT,
    arma_id INT,
    kills INT,
    FOREIGN KEY (partida_id) REFERENCES partidas(id),
    FOREIGN KEY (arma_id) REFERENCES armas(id)
);
id: Identificador único da kill.
partida_id: ID da partida em que a kill foi registrada (chave estrangeira para partidas).
arma_id: ID da arma utilizada na kill (chave estrangeira para armas).
kills: Quantidade de kills realizadas com a arma naquela partida.
Descrição do Fluxo
O projeto segue o seguinte fluxo para coletar e armazenar os dados:

Inicialização: Configuração do webdriver para iniciar a coleta de dados.
Extração das URLs de Partidas: O Selenium navega até a página principal e extrai as URLs das partidas que ocorreram dentro de um intervalo de datas específico.
Extração das URLs de Heatmaps: Para cada partida, é extraído o link para o "heatmap", que contém estatísticas de kills por tipo de arma.
Contagem de Kills por Arma: Para cada heatmap, é realizada a contagem de kills por tipo de arma.
Armazenamento em Banco de Dados: Os dados de partidas, armas e kills são inseridos nas tabelas SQL correspondentes.
Como Usar
Instale as bibliotecas necessárias:

bash
Copiar código
pip install selenium webdriver_manager beautifulsoup4 pandas
Configure as credenciais do SQL Server e execute o código para iniciar o scraping e o armazenamento dos dados.
