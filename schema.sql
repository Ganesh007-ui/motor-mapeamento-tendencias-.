-- 1. TABELA DE UTILIZADORES
CREATE TABLE utilizadores (
    id_utilizador SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    nivel_perfil VARCHAR(50) DEFAULT 'Standard'
);

-- 2. TABELA DE SERVIÇOS E PARCEIROS DISPONÍVEIS
CREATE TABLE servicos_disponiveis (
    id_servico SERIAL PRIMARY KEY,
    nome_servico VARCHAR(100) NOT NULL,
    tipo_servico VARCHAR(50) NOT NULL,
    instituicao_parceira VARCHAR(100) NOT NULL,
    taxa_servico NUMERIC(10, 2) DEFAULT 0.00
);

-- 3. TABELA DE HISTÓRICO DE BUSCAS
CREATE TABLE historico_buscas (
    id_busca SERIAL PRIMARY KEY,
    id_utilizador INT REFERENCES utilizadores(id_utilizador),
    termo_pesquisado VARCHAR(255) NOT NULL,
    categoria_dor VARCHAR(100),
    urgencia_detetada VARCHAR(50),
    data_pesquisa TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
