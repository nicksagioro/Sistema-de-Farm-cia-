from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from abc import ABC, abstractmethod

# ==================== CLASSE BASE ABSTRATA ====================
class EntidadeBase(ABC):
    """Classe base abstrata para todas as entidades do sistema"""
    
    @abstractmethod
    def validar(self) -> bool:
        """Valida os dados da entidade"""
        pass
    
    @abstractmethod
    def para_dict(self) -> dict:
        """Converte a entidade para dicionário"""
        pass


# ==================== MODELOS DO BANCO DE DADOS ====================

class Medicamento(Base, EntidadeBase):
    __tablename__ = "medicamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, unique=True, index=True)
    principio_ativo = Column(String(255), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, default=0)
    lote = Column(String(50), nullable=False)
    data_validade = Column(Date, nullable=False)
    fabricante = Column(String(255))
    descricao = Column(Text)
    id_fornecedor = Column(Integer, ForeignKey("fornecedores.id"))
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    fornecedor = relationship("Fornecedor", back_populates="medicamentos")
    itens_venda = relationship("ItemVenda", back_populates="medicamento")
    
    def validar(self) -> bool:
        """Valida se o medicamento está correto"""
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome do medicamento deve ter pelo menos 3 caracteres")
        if self.preco <= 0:
            raise ValueError("Preço deve ser maior que zero")
        if self.estoque < 0:
            raise ValueError("Estoque não pode ser negativo")
        return True
    
    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "principio_ativo": self.principio_ativo,
            "preco": float(self.preco),
            "estoque": self.estoque,
            "lote": self.lote,
            "data_validade": str(self.data_validade),
            "fabricante": self.fabricante,
            "descricao": self.descricao
        }


class Cliente(Base, EntidadeBase):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    telefone = Column(String(20))
    endereco = Column(Text)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    ativo = Column(Integer, default=1)  # 1 = ativo, 0 = inativo
    
    # Relacionamentos
    vendas = relationship("Venda", back_populates="cliente")
    
    def validar(self) -> bool:
        """Valida se o cliente está correto"""
        if not self.cpf or len(self.cpf) != 11 or not self.cpf.isdigit():
            raise ValueError("CPF inválido. Deve conter 11 dígitos")
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        if self.email and "@" not in self.email:
            raise ValueError("Email inválido")
        return True
    
    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "cpf": self.cpf,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "ativo": bool(self.ativo)
        }


class Fornecedor(Base, EntidadeBase):
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False, index=True)
    telefone = Column(String(20))
    email = Column(String(255))
    endereco = Column(Text)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    ativo = Column(Integer, default=1)
    
    # Relacionamentos
    medicamentos = relationship("Medicamento", back_populates="fornecedor")
    
    def validar(self) -> bool:
        """Valida se o fornecedor está correto"""
        if not self.cnpj or len(self.cnpj) != 14 or not self.cnpj.isdigit():
            raise ValueError("CNPJ inválido. Deve conter 14 dígitos")
        if not self.nome or len(self.nome) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return True
    
    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "telefone": self.telefone,
            "email": self.email,
            "endereco": self.endereco,
            "ativo": bool(self.ativo)
        }


class Venda(Base, EntidadeBase):
    __tablename__ = "vendas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_venda = Column(DateTime, default=datetime.utcnow)
    total = Column(Numeric(12, 2), default=0)
    desconto = Column(Numeric(10, 2), default=0)
    observacoes = Column(Text)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="vendas")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    
    def validar(self) -> bool:
        """Valida se a venda está correta"""
        if not self.id_cliente:
            raise ValueError("Cliente é obrigatório")
        if self.total < 0:
            raise ValueError("Total não pode ser negativo")
        if self.desconto < 0 or self.desconto > self.total:
            raise ValueError("Desconto inválido")
        return True
    
    def calcular_total(self) -> float:
        """Calcula o total baseado nos itens"""
        total = sum(float(item.preco_unitario) * item.quantidade for item in self.itens)
        self.total = total - float(self.desconto)
        return float(self.total)
    
    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "data_venda": str(self.data_venda),
            "total": float(self.total),
            "desconto": float(self.desconto),
            "itens": [item.para_dict() for item in self.itens]
        }


class ItemVenda(Base, EntidadeBase):
    __tablename__ = "itens_venda"
    
    id = Column(Integer, primary_key=True, index=True)
    id_venda = Column(Integer, ForeignKey("vendas.id"), nullable=False)
    id_medicamento = Column(Integer, ForeignKey("medicamentos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    
    # Relacionamentos
    venda = relationship("Venda", back_populates="itens")
    medicamento = relationship("Medicamento", back_populates="itens_venda")
    
    def validar(self) -> bool:
        """Valida se o item da venda está correto"""
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        if self.preco_unitario <= 0:
            raise ValueError("Preço unitário deve ser maior que zero")
        return True
    
    def calcular_subtotal(self) -> float:
        """Calcula o subtotal do item"""
        return float(self.preco_unitario) * self.quantidade
    
    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "id_medicamento": self.id_medicamento,
            "quantidade": self.quantidade,
            "preco_unitario": float(self.preco_unitario),
            "subtotal": self.calcular_subtotal()
        }
