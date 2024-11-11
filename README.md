#Bibliotecas:
1 - selenium,
2 - webdriver_manager.chrome,
3 - BeautifulSoup,
4 - pandas



CREATE TABLE partidas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    data DATETIME NOT NULL,
    url VARCHAR(255) NOT NULL
);


CREATE TABLE armas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    arma VARCHAR(100) NOT NULL
);

CREATE TABLE kills_por_arma (
    id INT IDENTITY(1,1) PRIMARY KEY,
    data DATETIME NOT NULL,
    arma VARCHAR(100) NOT NULL,
    kills INT NOT NULL
);
