"""
models.py - Mapeamento SQLAlchemy para o banco PostgreSQL

Modelos:
    Fornecedor, Cliente, Medicamento, ItemVenda, Venda
"""

import os
from datetime import date, datetime

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean, CheckConstraint, Column, Date, DateTime,
    ForeignKey, Integer, Numeric, String, Text,
    create_engine, event, text,
)
from sqlalchemy.orm import DeclarativeBase, Session, relationship

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/farmacia_db"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)


class Base(DeclarativeBase):
    pass


# ============================================================
#  FORNECEDOR
# ============================================================
class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id        = Column(Integer, primary_key=True, autoincrement=True)
    nome      = Column(String(255), nullable=False)
    cnpj      = Column(String(14), nullable=False, unique=True)
    telefone  = Column(String(20))
    email     = Column(String(120))
    endereco  = Column(String(255))
    ativo     = Column(Integer, nullable=False, default=1)

    medicamentos = relationship("Medicamento", back_populates="fornecedor")

    def validar(self):
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome do fornecedor deve ter pelo menos 3 caracteres")
        if not self.cnpj or len(self.cnpj) != 14 or not self.cnpj.isdigit():
            raise ValueError("CNPJ deve conter exatamente 14 digitos numericos")

    def __repr__(self):
        return f"<Fornecedor id={self.id} nome={self.nome!r}>"


# ============================================================
#  CLIENTE
# ============================================================
class Cliente(Base):
    __tablename__ = "clientes"

    id       = Column(Integer, primary_key=True, autoincrement=True)
    cpf      = Column(String(11), nullable=False, unique=True)
    nome     = Column(String(255), nullable=False)
    email    = Column(String(120))
    telefone = Column(String(20))
    endereco = Column(String(255))
    ativo    = Column(Integer, nullable=False, default=1)

    vendas = relationship("Venda", back_populates="cliente")

    def validar(self):
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome do cliente deve ter pelo menos 3 caracteres")
        if not self.cpf or len(self.cpf) != 11 or not self.cpf.isdigit():
            raise ValueError("CPF deve conter exatamente 11 digitos numericos")

    def __repr__(self):
        return f"<Cliente id={self.id} nome={self.nome!r}>"


# ============================================================
#  MEDICAMENTO
# ============================================================
class Medicamento(Base):
    __tablename__ = "medicamentos"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    nome            = Column(String(255), nullable=False, unique=True)
    principio_ativo = Column(String(255), nullable=False)
    preco           = Column(Numeric(12, 2), nullable=False)
    estoque         = Column(Integer, nullable=False, default=0)
    lote            = Column(String(50), nullable=False)
    data_validade   = Column(Date, nullable=False)
    fabricante      = Column(String(255))
    descricao       = Column(Text)
    id_fornecedor   = Column(Integer, ForeignKey("fornecedores.id",
                                                  ondelete="SET NULL"),
                             nullable=True)

    fornecedor = relationship("Fornecedor", back_populates="medicamentos")
    itens      = relationship("ItemVenda", back_populates="medicamento")

    def validar(self):
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome do medicamento deve ter pelo menos 3 caracteres")
        if self.preco is None or float(self.preco) <= 0:
            raise ValueError("Preco deve ser maior que zero")
        if self.estoque is not None and self.estoque < 0:
            raise ValueError("Estoque nao pode ser negativo")

    def __repr__(self):
        return f"<Medicamento id={self.id} nome={self.nome!r}>"


# ============================================================
#  ITEM DE VENDA
# ============================================================
class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    id_venda        = Column(Integer, ForeignKey("vendas.id",
                                                  ondelete="CASCADE"),
                             nullable=False)
    id_medicamento  = Column(Integer, ForeignKey("medicamentos.id",
                                                  ondelete="RESTRICT"),
                             nullable=False)
    quantidade      = Column(Integer, nullable=False)
    preco_unitario  = Column(Numeric(12, 2), nullable=False)

    venda       = relationship("Venda", back_populates="itens")
    medicamento = relationship("Medicamento", back_populates="itens")

    def validar(self):
        if self.quantidade is None or self.quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        if self.preco_unitario is None or float(self.preco_unitario) <= 0:
            raise ValueError("Preco unitario deve ser maior que zero")

    def calcular_subtotal(self) -> float:
        return round(float(self.quantidade) * float(self.preco_unitario), 2)

    def __repr__(self):
        return (f"<ItemVenda id={self.id} med_id={self.id_medicamento} "
                f"qtd={self.quantidade}>")


# ============================================================
#  VENDA
# ============================================================
class Venda(Base):
    __tablename__ = "vendas"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente  = Column(Integer, ForeignKey("clientes.id",
                                              ondelete="RESTRICT"),
                         nullable=False)
    data_venda  = Column(DateTime, nullable=False, default=datetime.utcnow)
    total       = Column(Numeric(14, 2), nullable=False, default=0)
    desconto    = Column(Numeric(12, 2), nullable=False, default=0)
    observacoes = Column(Text)

    cliente = relationship("Cliente", back_populates="vendas")
    itens   = relationship("ItemVenda", back_populates="venda",
                           cascade="all, delete-orphan")

    def validar(self):
        if self.id_cliente is None:
            raise ValueError("Venda deve estar associada a um cliente")
        if self.total is not None and float(self.total) < 0:
            raise ValueError("Total da venda nao pode ser negativo")

    def __repr__(self):
        return f"<Venda id={self.id} cliente_id={self.id_cliente} total={self.total}>"


# ============================================================
#  UTILITARIO: criar tabelas (somente para desenvolvimento)
# ============================================================
def criar_tabelas():
    Base.metadata.create_all(engine)
    print("Tabelas criadas/verificadas com sucesso.")


if __name__ == "__main__":
    criar_tabelas()

    with Session(engine) as session:
        fornecedores = session.query(Fornecedor).all()
        print("\nFornecedores:")
        for f in fornecedores:
            print(f"  {f}")

        clientes = session.query(Cliente).all()
        print("\nClientes:")
        for c in clientes:
            print(f"  {c}")

        medicamentos = session.query(Medicamento).all()
        print("\nMedicamentos:")
        for m in medicamentos:
            print(f"  {m}")

        vendas = session.query(Venda).all()
        print("\nVendas:")
        for v in vendas:
            print(f"  {v}")
