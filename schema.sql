-- ============================================================
--  BANCO DE DADOS - SISTEMA DE FARMACIA
--  Execute este script no DBeaver conectado ao PostgreSQL
-- ============================================================

-- Criar banco (execute separadamente se necessario)
-- CREATE DATABASE farmacia_db;

-- ============================================================
--  TABELA: FORNECEDORES
-- ============================================================
CREATE TABLE IF NOT EXISTS fornecedores (
    id        SERIAL PRIMARY KEY,
    nome      VARCHAR(255) NOT NULL,
    cnpj      VARCHAR(14)  NOT NULL UNIQUE,
    telefone  VARCHAR(20),
    email     VARCHAR(120),
    endereco  VARCHAR(255),
    ativo     SMALLINT NOT NULL DEFAULT 1
);

-- ============================================================
--  TABELA: CLIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id        SERIAL PRIMARY KEY,
    cpf       VARCHAR(11)  NOT NULL UNIQUE,
    nome      VARCHAR(255) NOT NULL,
    email     VARCHAR(120),
    telefone  VARCHAR(20),
    endereco  VARCHAR(255),
    ativo     SMALLINT NOT NULL DEFAULT 1
);

-- ============================================================
--  TABELA: MEDICAMENTOS
-- ============================================================
CREATE TABLE IF NOT EXISTS medicamentos (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(255) NOT NULL UNIQUE,
    principio_ativo VARCHAR(255) NOT NULL,
    preco           NUMERIC(12, 2) NOT NULL,
    estoque         INTEGER NOT NULL DEFAULT 0,
    lote            VARCHAR(50) NOT NULL,
    data_validade   DATE NOT NULL,
    fabricante      VARCHAR(255),
    descricao       TEXT,
    id_fornecedor   INTEGER REFERENCES fornecedores(id) ON DELETE SET NULL
);

-- ============================================================
--  TABELA: VENDAS
-- ============================================================
CREATE TABLE IF NOT EXISTS vendas (
    id          SERIAL PRIMARY KEY,
    id_cliente  INTEGER NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    data_venda  TIMESTAMP NOT NULL DEFAULT NOW(),
    total       NUMERIC(14, 2) NOT NULL DEFAULT 0,
    desconto    NUMERIC(12, 2) NOT NULL DEFAULT 0,
    observacoes TEXT
);

-- ============================================================
--  TABELA: ITENS_VENDA
-- ============================================================
CREATE TABLE IF NOT EXISTS itens_venda (
    id             SERIAL PRIMARY KEY,
    id_venda       INTEGER NOT NULL REFERENCES vendas(id) ON DELETE CASCADE,
    id_medicamento INTEGER NOT NULL REFERENCES medicamentos(id) ON DELETE RESTRICT,
    quantidade     INTEGER NOT NULL,
    preco_unitario NUMERIC(12, 2) NOT NULL
);

-- ============================================================
--  INDICES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_medicamentos_nome      ON medicamentos(nome);
CREATE INDEX IF NOT EXISTS idx_itens_venda_venda      ON itens_venda(id_venda);
CREATE INDEX IF NOT EXISTS idx_itens_venda_medicamento ON itens_venda(id_medicamento);
CREATE INDEX IF NOT EXISTS idx_vendas_cliente         ON vendas(id_cliente);
CREATE INDEX IF NOT EXISTS idx_vendas_data            ON vendas(data_venda);

-- ============================================================
--  DADOS DE EXEMPLO
-- ============================================================
INSERT INTO fornecedores (nome, cnpj, email, telefone)
VALUES
    ('Industria Farmaceutica Brasil S.A.', '12345678000100', 'contato@farmbrasil.com.br', '1133334444'),
    ('Medicamentos Genericos LTDA',        '98765432000100', 'vendas@medgenericos.com.br', '1144445555')
ON CONFLICT (cnpj) DO NOTHING;

INSERT INTO clientes (cpf, nome, email, telefone)
VALUES
    ('11144477788', 'Joao Silva Santos',   'joao.silva@email.com',   '11987654321'),
    ('22255588899', 'Maria Oliveira Costa','maria.oliveira@email.com','11912345678')
ON CONFLICT (cpf) DO NOTHING;
