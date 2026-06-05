from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix="/api/clientes", tags=["clientes"])


@router.get("", response_model=list[ClienteResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Cliente).offset(skip).limit(limit).all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter(cliente_id: int, db: Session = Depends(get_db)):
    c = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not c:
        raise HTTPException(404, "Cliente nao encontrado")
    return c


@router.post("", response_model=ClienteResponse, status_code=201)
def criar(cliente: ClienteCreate, db: Session = Depends(get_db)):
    if db.query(Cliente).filter(Cliente.cpf == cliente.cpf).first():
        raise HTTPException(400, "CPF ja cadastrado")
    novo = Cliente(**cliente.model_dump())
    novo.validar()
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar(cliente_id: int, cliente: ClienteUpdate,
              db: Session = Depends(get_db)):
    c = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not c:
        raise HTTPException(404, "Cliente nao encontrado")
    for k, v in cliente.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    c.validar()
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{cliente_id}", status_code=204)
def deletar(cliente_id: int, db: Session = Depends(get_db)):
    c = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not c:
        raise HTTPException(404, "Cliente nao encontrado")
    db.delete(c)
    db.commit()
