from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente, ItemVenda, Medicamento, Venda
from schemas import VendaCreate, VendaUpdate, VendaResponse

router = APIRouter(prefix="/api/vendas", tags=["vendas"])


@router.get("", response_model=list[VendaResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Venda).offset(skip).limit(limit).all()


@router.get("/{venda_id}", response_model=VendaResponse)
def obter(venda_id: int, db: Session = Depends(get_db)):
    v = db.query(Venda).filter(Venda.id == venda_id).first()
    if not v:
        raise HTTPException(404, "Venda nao encontrada")
    return v


@router.post("", response_model=VendaResponse, status_code=201)
def criar(venda: VendaCreate, db: Session = Depends(get_db)):
    if not db.query(Cliente).filter(Cliente.id == venda.id_cliente).first():
        raise HTTPException(404, "Cliente nao encontrado")

    nova = Venda(id_cliente=venda.id_cliente,
                 desconto=venda.desconto,
                 observacoes=venda.observacoes)
    db.add(nova)
    db.flush()

    total = 0.0
    for item_data in venda.itens:
        med = db.query(Medicamento).filter(
            Medicamento.id == item_data.id_medicamento).first()
        if not med:
            db.rollback()
            raise HTTPException(404, f"Medicamento {item_data.id_medicamento} nao encontrado")
        if med.estoque < item_data.quantidade:
            db.rollback()
            raise HTTPException(400, f"Estoque insuficiente para {med.nome}")
        item = ItemVenda(id_venda=nova.id,
                         id_medicamento=item_data.id_medicamento,
                         quantidade=item_data.quantidade,
                         preco_unitario=item_data.preco_unitario)
        item.validar()
        total += item.calcular_subtotal()
        db.add(item)
        med.estoque -= item_data.quantidade

    nova.total = round(total - float(nova.desconto), 2)
    nova.validar()
    db.commit()
    db.refresh(nova)
    return nova


@router.put("/{venda_id}", response_model=VendaResponse)
def atualizar(venda_id: int, venda: VendaUpdate,
              db: Session = Depends(get_db)):
    v = db.query(Venda).filter(Venda.id == venda_id).first()
    if not v:
        raise HTTPException(404, "Venda nao encontrada")
    for k, val in venda.model_dump(exclude_unset=True).items():
        setattr(v, k, val)
    v.validar()
    db.commit()
    db.refresh(v)
    return v


@router.delete("/{venda_id}", status_code=204)
def deletar(venda_id: int, db: Session = Depends(get_db)):
    v = db.query(Venda).filter(Venda.id == venda_id).first()
    if not v:
        raise HTTPException(404, "Venda nao encontrada")
    for item in v.itens:
        med = db.query(Medicamento).filter(
            Medicamento.id == item.id_medicamento).first()
        if med:
            med.estoque += item.quantidade
    db.delete(v)
    db.commit()
