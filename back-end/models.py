from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base  # Conexão direta com a Base do banco de dados

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(50), nullable=False, unique=True)
    telefone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    endereco = Column(String(255), nullable=True)
    ativo = Column(Integer, default=1, nullable=False)

    medicamentos = relationship("Medicamento", back_populates="fornecedor")

    def validar(self):
        # Método requerido pelos endpoints da API
        pass


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False, unique=True)
    principio_ativo = Column(String(255), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0, nullable=False)
    lote = Column(String(50), nullable=False)
    data_validade = Column(Date, nullable=False)
    fabricante = Column(String(255), nullable=True)
    descricao = Column(Text, nullable=True)
    id_fornecedor = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)

    fornecedor = relationship("Fornecedor", back_populates="medicamentos")

    def validar(self):
        pass


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=True)
    telefone = Column(String(50), nullable=True)
    endereco = Column(String(255), nullable=True)
    ativo = Column(Integer, default=1, nullable=False)

    def validar(self):
        pass


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    desconto = Column(Float, default=0.0, nullable=False)
    observacoes = Column(Text, nullable=True)
    total = Column(Float, default=0.0, nullable=False)

    # Relacionamento de um-para-muitos com os itens da venda
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

    def validar(self):
        pass


class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_venda = Column(Integer, ForeignKey("vendas.id"), nullable=False)
    id_medicamento = Column(Integer, ForeignKey("medicamentos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    venda = relationship("Venda", back_populates="itens")

    def validar(self):
        pass

    def calcular_subtotal(self) -> float:
        return self.quantidade * self.preco_unitario