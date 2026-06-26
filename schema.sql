-- 1. TABELA DE UTILIZADORES
-- Guarda o perfil básico de quem está a usar o app
CREATE TABLE utilizadores (
    id_utilizador SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telemovel VARCHAR(20) UNIQUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nivel_perfil VARCHAR(20) DEFAULT 'Standard' -- Ex: Permite identificar necessidades específicas
);

-- 2. TABELA DE MOTORES DE BUSCA / LOGS DE TENDÊNCIAS
-- Aqui o Python vai registar o que o algoritmo capturou das APIs do telemóvel
CREATE TABLE historico_buscas (
    id_busca SERIAL PRIMARY KEY,
    id_utilizador INT REFERENCES utilizadores(id_utilizador),
    termo_pesquisado VARCHAR(255) NOT NULL,
    categoria_dor VARCHAR(50) NOT NULL, -- Ex: 'Serviços Públicos', 'Rotas', 'Pagamentos'
    urgencia_detetada BOOLEAN DEFAULT FALSE,
    data_pesquisa TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABELA DE SERVIÇOS PÚBLICOS E PARCEIROS
-- Centraliza as soluções desburocratizadas que o app oferece
CREATE TABLE servicos_disponiveis (
    id_servico SERIAL PRIMARY KEY,
    nome_servico VARCHAR(100) NOT NULL,
    tipo_servico VARCHAR(50) NOT NULL, -- Ex: 'Luz', 'Água', 'Transporte', 'Reserva'
    instituicao_parceira VARCHAR(100) NOT NULL,
    taxa_servico NUMERIC(10, 2) DEFAULT 0.00
);

-- 4. TABELA DE TRANSAÇÕES E PAGAMENTOS
-- Simplifica o histórico financeiro do utilizador (independente da classe social)
CREATE TABLE pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    id_utilizador INT REFERENCES utilizadores(id_utilizador),
    id_servico INT REFERENCES servicos_disponiveis(id_servico),
    valor NUMERIC(10, 2) NOT NULL,
    metodo_pagamento VARCHAR(30) NOT NULL, -- Ex: 'PIX', 'Cartão', 'Saldo App'
    status_pagamento VARCHAR(20) DEFAULT 'Pendente', -- Ex: 'Sucesso', 'Falhado'
    data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. TABELA DE ROTAS E GEOLOCALIZAÇÃO
-- Para mapear os caminhos mais rápidos e resolver problemas de transporte em tempo real
CREATE TABLE rotas_frequentes (
    id_rota SERIAL PRIMARY KEY,
    id_utilizador INT REFERENCES utilizadores(id_utilizador),
    ponto_partida VARCHAR(255) NOT NULL,
    ponto_destino VARCHAR(255) NOT NULL,
    tempo_medio_minutos INT,
    alerta_transito BOOLEAN DEFAULT FALSE
);
