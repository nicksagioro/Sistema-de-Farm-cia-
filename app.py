from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import uvicorn

from database import get_db, init_db
from models import Medicamento, Cliente, Fornecedor, Venda, ItemVenda
from schemas import (
    MedicamentoCreate, MedicamentoUpdate, MedicamentoResponse,
    ClienteCreate, ClienteUpdate, ClienteResponse,
    FornecedorCreate, FornecedorUpdate, FornecedorResponse,
    VendaCreate, VendaUpdate, VendaResponse,
    ItemVendaCreate, ItemVendaResponse
)

app = FastAPI(
    title="Farmácia API",
    description="API REST para sistema de gerenciamento de farmácia",
    version="1.0.0"
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== INICIALIZAÇÃO ====================
@app.on_event("startup")
def startup():
    init_db()

# ==================== ENDPOINTS MEDICAMENTOS ====================

@app.get("/api/medicamentos", response_model=list[MedicamentoResponse])
def listar_medicamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os medicamentos com paginação"""
    medicamentos = db.query(Medicamento).offset(skip).limit(limit).all()
    return medicamentos

@app.get("/api/medicamentos/{med_id}", response_model=MedicamentoResponse)
def obter_medicamento(med_id: int, db: Session = Depends(get_db)):
    """Obtém um medicamento específico pelo ID"""
    medicamento = db.query(Medicamento).filter(Medicamento.id == med_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return medicamento

@app.post("/api/medicamentos", response_model=MedicamentoResponse, status_code=201)
def criar_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    """Cria um novo medicamento"""
    # Verificar se já existe medicamento com o mesmo nome
    existente = db.query(Medicamento).filter(Medicamento.nome == medicamento.nome).first()
    if existente:
        raise HTTPException(status_code=400, detail="Medicamento com este nome já existe")
    
    novo_medicamento = Medicamento(**medicamento.dict())
    novo_medicamento.validar()
    
    db.add(novo_medicamento)
    db.commit()
    db.refresh(novo_medicamento)
    return novo_medicamento

@app.put("/api/medicamentos/{med_id}", response_model=MedicamentoResponse)
def atualizar_medicamento(med_id: int, medicamento: MedicamentoUpdate, db: Session = Depends(get_db)):
    """Atualiza um medicamento existente"""
    db_medicamento = db.query(Medicamento).filter(Medicamento.id == med_id).first()
    if not db_medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    
    dados_atualizacao = medicamento.dict(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(db_medicamento, campo, valor)
    
    db_medicamento.validar()
    db.commit()
    db.refresh(db_medicamento)
    return db_medicamento

@app.delete("/api/medicamentos/{med_id}", status_code=204)
def deletar_medicamento(med_id: int, db: Session = Depends(get_db)):
    """Deleta um medicamento"""
    medicamento = db.query(Medicamento).filter(Medicamento.id == med_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    
    db.delete(medicamento)
    db.commit()
    return None

# ==================== ENDPOINTS CLIENTES ====================

@app.get("/api/clientes", response_model=list[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os clientes"""
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return clientes

@app.get("/api/clientes/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtém um cliente específico"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@app.post("/api/clientes", response_model=ClienteResponse, status_code=201)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Cria um novo cliente"""
    # Verificar se CPF já existe
    existente = db.query(Cliente).filter(Cliente.cpf == cliente.cpf).first()
    if existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    novo_cliente = Cliente(**cliente.dict())
    novo_cliente.validar()
    
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@app.put("/api/clientes/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    """Atualiza um cliente"""
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    dados_atualizacao = cliente.dict(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(db_cliente, campo, valor)
    
    db_cliente.validar()
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@app.delete("/api/clientes/{cliente_id}", status_code=204)
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Deleta um cliente"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(cliente)
    db.commit()
    return None

# ==================== ENDPOINTS FORNECEDORES ====================

@app.get("/api/fornecedores", response_model=list[FornecedorResponse])
def listar_fornecedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os fornecedores"""
    fornecedores = db.query(Fornecedor).offset(skip).limit(limit).all()
    return fornecedores

@app.get("/api/fornecedores/{fornecedor_id}", response_model=FornecedorResponse)
def obter_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """Obtém um fornecedor específico"""
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@app.post("/api/fornecedores", response_model=FornecedorResponse, status_code=201)
def criar_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    """Cria um novo fornecedor"""
    existente = db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor.cnpj).first()
    if existente:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    
    novo_fornecedor = Fornecedor(**fornecedor.dict())
    novo_fornecedor.validar()
    
    db.add(novo_fornecedor)
    db.commit()
    db.refresh(novo_fornecedor)
    return novo_fornecedor

@app.put("/api/fornecedores/{fornecedor_id}", response_model=FornecedorResponse)
def atualizar_fornecedor(fornecedor_id: int, fornecedor: FornecedorUpdate, db: Session = Depends(get_db)):
    """Atualiza um fornecedor"""
    db_fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not db_fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    dados_atualizacao = fornecedor.dict(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(db_fornecedor, campo, valor)
    
    db_fornecedor.validar()
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor

@app.delete("/api/fornecedores/{fornecedor_id}", status_code=204)
def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """Deleta um fornecedor"""
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    db.delete(fornecedor)
    db.commit()
    return None

# ==================== ENDPOINTS VENDAS ====================

@app.get("/api/vendas", response_model=list[VendaResponse])
def listar_vendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as vendas"""
    vendas = db.query(Venda).offset(skip).limit(limit).all()
    return vendas

@app.get("/api/vendas/{venda_id}", response_model=VendaResponse)
def obter_venda(venda_id: int, db: Session = Depends(get_db)):
    """Obtém uma venda específica"""
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@app.post("/api/vendas", response_model=VendaResponse, status_code=201)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)):
    """Cria uma nova venda"""
    # Verificar se cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == venda.id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    nova_venda = Venda(
        id_cliente=venda.id_cliente,
        desconto=venda.desconto,
        observacoes=venda.observacoes
    )
    
    # Adicionar itens
    total = 0
    for item_data in venda.itens:
        medicamento = db.query(Medicamento).filter(Medicamento.id == item_data.id_medicamento).first()
        if not medicamento:
            raise HTTPException(status_code=404, detail=f"Medicamento {item_data.id_medicamento} não encontrado")
        
        if medicamento.estoque < item_data.quantidade:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {medicamento.nome}")
        
        item = ItemVenda(
            id_medicamento=item_data.id_medicamento,
            quantidade=item_data.quantidade,
            preco_unitario=item_data.preco_unitario
        )
        item.validar()
        total += item.calcular_subtotal()
        nova_venda.itens.append(item)
        
        # Atualizar estoque
        medicamento.estoque -= item_data.quantidade
    
    nova_venda.total = total - nova_venda.desconto
    nova_venda.validar()
    
    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)
    return nova_venda

@app.put("/api/vendas/{venda_id}", response_model=VendaResponse)
def atualizar_venda(venda_id: int, venda: VendaUpdate, db: Session = Depends(get_db)):
    """Atualiza uma venda (apenas desconto e observações)"""
    db_venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not db_venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    dados_atualizacao = venda.dict(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(db_venda, campo, valor)
    
    db_venda.validar()
    db.commit()
    db.refresh(db_venda)
    return db_venda

@app.delete("/api/vendas/{venda_id}", status_code=204)
def deletar_venda(venda_id: int, db: Session = Depends(get_db)):
    """Deleta uma venda e restaura estoque dos medicamentos"""
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    # Restaurar estoque
    for item in venda.itens:
        medicamento = db.query(Medicamento).filter(Medicamento.id == item.id_medicamento).first()
        if medicamento:
            medicamento.estoque += item.quantidade
    
    db.delete(venda)
    db.commit()
    return None

# ==================== ROTA HEALTH CHECK ====================

@app.get("/health")
def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "OK", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)