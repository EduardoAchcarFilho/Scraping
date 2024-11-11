#Bibliotecas:
1 - selenium,
2 - webdriver_manager.chrome,
3 - BeautifulSoup,
4 - pandas



-- Tabela de Partidas (Fato)
CREATE TABLE partidas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    data DATETIME,
    url NVARCHAR(500)
);

-- Tabela de Armas (Dimensão)
CREATE TABLE armas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100)
);

-- Tabela de Kills (Fato)
CREATE TABLE kills (
    id INT IDENTITY(1,1) PRIMARY KEY,
    partida_id INT,
    arma_id INT,
    kills INT,
    FOREIGN KEY (partida_id) REFERENCES partidas(id),
    FOREIGN KEY (arma_id) REFERENCES armas(id)
);
