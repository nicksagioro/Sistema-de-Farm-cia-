-- ============================================================
--  BANCO DE DADOS - SISTEMA DE GESTÃO
--  Execute este script no DBeaver conectado ao PostgreSQL
-- ============================================================

-- Criar schema dedicado (opcional, mas recomendado)
CREATE SCHEMA IF NOT EXISTS gestao;
SET search_path TO gestao;

-- ============================================================
--  TABELA: FORNECEDORES
-- ============================================================
CREATE TABLE IF NOT EXISTS fornecedores (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(150) NOT NULL,
    cnpj        VARCHAR(18) UNIQUE NOT NULL,
    email       VARCHAR(120),
    telefone    VARCHAR(20),
    endereco    VARCHAR(255),
    cidade      VARCHAR(100),
    estado      CHAR(2),
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
--  TABELA: CLIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(150) NOT NULL,
    cpf_cnpj    VARCHAR(18) UNIQUE NOT NULL,
    email       VARCHAR(120),
    telefone    VARCHAR(20),
    endereco    VARCHAR(255),
    cidade      VARCHAR(100),
    estado      CHAR(2),
    tipo        VARCHAR(10) NOT NULL DEFAULT 'PF' CHECK (tipo IN ('PF', 'PJ')),
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
--  TABELA: ESTOQUE
-- ============================================================
CREATE TABLE IF NOT EXISTS estoque (
    id              SERIAL PRIMARY KEY,
    fornecedor_id   INTEGER NOT NULL REFERENCES fornecedores(id) ON DELETE RESTRICT,
    nome            VARCHAR(150) NOT NULL,
    descricao       TEXT,
    sku             VARCHAR(50) UNIQUE,
    categoria       VARCHAR(80),
    unidade         VARCHAR(20) NOT NULL DEFAULT 'UN',
    quantidade      NUMERIC(12, 3) NOT NULL DEFAULT 0,
    estoque_minimo  NUMERIC(12, 3) NOT NULL DEFAULT 0,
    preco_custo     NUMERIC(12, 2) NOT NULL DEFAULT 0,
    preco_venda     NUMERIC(12, 2) NOT NULL DEFAULT 0,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
--  TABELA: VENDAS
-- ============================================================
CREATE TABLE IF NOT EXISTS vendas (
    id              SERIAL PRIMARY KEY,
    cliente_id      INTEGER NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    estoque_id      INTEGER NOT NULL REFERENCES estoque(id) ON DELETE RESTRICT,
    quantidade      NUMERIC(12, 3) NOT NULL,
    preco_unitario  NUMERIC(12, 2) NOT NULL,
    desconto        NUMERIC(5, 2) NOT NULL DEFAULT 0,     -- percentual 0-100
    total           NUMERIC(14, 2) GENERATED ALWAYS AS (
                        ROUND(quantidade * preco_unitario * (1 - desconto / 100.0), 2)
                    ) STORED,
    status          VARCHAR(20) NOT NULL DEFAULT 'PENDENTE'
                        CHECK (status IN ('PENDENTE', 'CONFIRMADA', 'CANCELADA', 'ENTREGUE')),
    observacao      TEXT,
    data_venda      TIMESTAMP NOT NULL DEFAULT NOW(),
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
--  ÍNDICES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_estoque_fornecedor   ON estoque(fornecedor_id);
CREATE INDEX IF NOT EXISTS idx_estoque_categoria    ON estoque(categoria);
CREATE INDEX IF NOT EXISTS idx_vendas_cliente       ON vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_estoque       ON vendas(estoque_id);
CREATE INDEX IF NOT EXISTS idx_vendas_status        ON vendas(status);
CREATE INDEX IF NOT EXISTS idx_vendas_data          ON vendas(data_venda);

-- ============================================================
--  TRIGGER: atualiza "atualizado_em" automaticamente
-- ============================================================
CREATE OR REPLACE FUNCTION gestao.fn_atualizar_timestamp()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_fornecedores_upd BEFORE UPDATE ON fornecedores
    FOR EACH ROW EXECUTE FUNCTION gestao.fn_atualizar_timestamp();

CREATE TRIGGER trg_clientes_upd BEFORE UPDATE ON clientes
    FOR EACH ROW EXECUTE FUNCTION gestao.fn_atualizar_timestamp();

CREATE TRIGGER trg_estoque_upd BEFORE UPDATE ON estoque
    FOR EACH ROW EXECUTE FUNCTION gestao.fn_atualizar_timestamp();

CREATE TRIGGER trg_vendas_upd BEFORE UPDATE ON vendas
    FOR EACH ROW EXECUTE FUNCTION gestao.fn_atualizar_timestamp();

-- ============================================================
--  DADOS DE EXEMPLO
-- ============================================================
INSERT INTO fornecedores (nome, cnpj, email, telefone, cidade, estado)
VALUES
    ('Distribuidora Alpha Ltda', '12.345.678/0001-99', 'contato@alpha.com', '(21) 99999-0001', 'Rio de Janeiro', 'RJ'),
    ('Indústria Beta S.A.',      '98.765.432/0001-11', 'vendas@beta.com',   '(11) 88888-0002', 'São Paulo',      'SP');

INSERT INTO clientes (nome, cpf_cnpj, email, telefone, cidade, estado, tipo)
VALUES
    ('João da Silva',        '123.456.789-00', 'joao@email.com',    '(21) 91234-5678', 'Araruama',     'RJ', 'PF'),
    ('Comércio Gama Ltda',   '11.222.333/0001-44', 'gama@loja.com', '(21) 97654-3210', 'Rio de Janeiro','RJ', 'PJ');

INSERT INTO estoque (fornecedor_id, nome, sku, categoria, quantidade, estoque_minimo, preco_custo, preco_venda)
VALUES
    (1, 'Produto A', 'SKU-001', 'Eletrônicos', 100, 10, 50.00, 89.90),
    (2, 'Produto B', 'SKU-002', 'Informática',  50,  5, 30.00, 59.90);

INSERT INTO vendas (cliente_id, estoque_id, quantidade, preco_unitario, desconto, status)
VALUES
    (1, 1, 2, 89.90, 0,  'CONFIRMADA'),
    (2, 2, 5, 59.90, 10, 'PENDENTE');
