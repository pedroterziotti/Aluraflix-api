CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    url TEXT NOT NULL,
    categoriaId INTEGER DEFAULT 1,
    FOREIGN KEY (categoriaId)
        REFERENCES categorias (id));

CREATE TABLE IF NOT EXISTS categorias(
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    cor TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL);


INSERT INTO categorias (titulo,cor) VALUES ('Livre','Livre');
INSERT INTO videos (titulo, descricao,url) VALUES ('Video','Video','Video');
INSERT INTO users (username,password) VALUES ('admin','admin');