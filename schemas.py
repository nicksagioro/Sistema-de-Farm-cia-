"""
schemas.py - Schemas Pydantic para validacao de entrada e saida da API.
"""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================
#  MEDICAMENTOS
# ============================================================

class MedicamentoCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    principio_ativo: str = Field(..., min_length=3, max_length=255)
    preco: float = Field(..., gt=0)
    estoque: int = Field(default=0, ge=0)
    lote: str = Field(..., min_length=1, max_length=50)
    data_validade: date
    fabricante: Optional[str] = None
    descricao: Optional[str] = None
    id_fornecedor: Optional[int] = None


class MedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    principio_ativo: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None
    lote: Optional[str] = None
    data_validade: Optional[date] = None
    fabricante: Optional[str] = None
    descricao: Optional[str] = None
    id_fornecedor: Optional[int] = None


class MedicamentoResponse(BaseModel):
    id: int
    nome: str
    principio_ativo: str
    preco: float
    estoque: int
    lote: str
    data_validade: date
    fabricante: Optional[str] = None
    descricao: Optional[str] = None
    id_fornecedor: Optional[int] = None

    model_config = {"from_attributes": True}


# ============================================================
#  CLIENTES
# ============================================================

class ClienteCreate(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)
    nome: str = Field(..., min_length=3, max_length=255)
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

    @field_validator("cpf")
    @classmethod
    def cpf_deve_ser_numerico(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("CPF deve conter apenas digitos")
        return v


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[int] = None


class ClienteResponse(BaseModel):
    id: int
    cpf: str
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: int

    model_config = {"from_attributes": True}


# ============================================================
#  FORNECEDORES
# ============================================================

class FornecedorCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    cnpj: str = Field(..., min_length=14, max_length=14)
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None

    @field_validator("cnpj")
    @classmethod
    def cnpj_deve_ser_numerico(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("CNPJ deve conter apenas digitos")
        return v


class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[int] = None


class FornecedorResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    ativo: int

    model_config = {"from_attributes": True}


# ============================================================
#  ITENS DE VENDA
# ============================================================

class ItemVendaCreate(BaseModel):
    id_medicamento: int
    quantidade: int = Field(..., gt=0)
    preco_unitario: float = Field(..., gt=0)


class ItemVendaResponse(BaseModel):
    id: int
    id_medicamento: int
    quantidade: int
    preco_unitario: float

    model_config = {"from_attributes": True}


# ============================================================
#  VENDAS
# ============================================================

class VendaCreate(BaseModel):
    id_cliente: int
    desconto: float = Field(default=0, ge=0)
    observacoes: Optional[str] = None
    itens: List[ItemVendaCreate]


class VendaUpdate(BaseModel):
    desconto: Optional[float] = None
    observacoes: Optional[str] = None


class VendaResponse(BaseModel):
    id: int
    id_cliente: int
    data_venda: datetime
    total: float
    desconto: float
    itens: List[ItemVendaResponse]

    model_config = {"from_attributes": True}
