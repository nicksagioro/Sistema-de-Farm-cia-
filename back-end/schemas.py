from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List

# ==================== MEDICAMENTOS ====================

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
    fabricante: Optional[str]
    descricao: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== CLIENTES ====================

class ClienteCreate(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)
    nome: str = Field(..., min_length=3, max_length=255)
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    
    @validator('cpf')
    def cpf_must_be_digits(cls, v):
        if not v.isdigit():
            raise ValueError('CPF deve conter apenas dígitos')
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
    email: Optional[str]
    telefone: Optional[str]
    endereco: Optional[str]
    ativo: int
    
    class Config:
        from_attributes = True


# ==================== FORNECEDORES ====================

class FornecedorCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    cnpj: str = Field(..., min_length=14, max_length=14)
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    
    @validator('cnpj')
    def cnpj_must_be_digits(cls, v):
        if not v.isdigit():
            raise ValueError('CNPJ deve conter apenas dígitos')
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
    telefone: Optional[str]
    email: Optional[str]
    endereco: Optional[str]
    ativo: int
    
    class Config:
        from_attributes = True


# ==================== ITENS VENDA ====================

class ItemVendaCreate(BaseModel):
    id_medicamento: int
    quantidade: int = Field(..., gt=0)
    preco_unitario: float = Field(..., gt=0)

class ItemVendaResponse(BaseModel):
    id: int
    id_medicamento: int
    quantidade: int
    preco_unitario: float
    
    class Config:
        from_attributes = True


# ==================== VENDAS ====================

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
    
    class Config:
        from_attributes = True
