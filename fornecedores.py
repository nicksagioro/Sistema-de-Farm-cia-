from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Fornecedor
from schemas import FornecedorCreate, FornecedorUpdate, FornecedorResponse

router = APIRouter(prefix="/api/fornecedores", tags=["fornecedores"])


@router.get("", response_model=list[FornecedorResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Fornecedor).offset(skip).limit(limit).all()


@router.get("/{forn_id}", response_model=FornecedorResponse)
def obter(forn_id: int, db: Session = Depends(get_db)):
    f = db.query(Fornecedor).filter(Fornecedor.id == forn_id).first()
    if not f:
        raise HTTPException(404, "Fornecedor nao encontrado")
    return f


@router.post("", response_model=FornecedorResponse, status_code=201)
def criar(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    if db.query(Fornecedor).filter(Fornecedor.cnpj == fornecedor.cnpj).first():
        raise HTTPException(400, "CNPJ ja cadastrado")
    novo = Fornecedor(**fornecedor.model_dump())
    novo.validar()
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{forn_id}", response_model=FornecedorResponse)
def atualizar(forn_id: int, fornecedor: FornecedorUpdate,
              db: Session = Depends(get_db)):
    f = db.query(Fornecedor).filter(Fornecedor.id == forn_id).first()
    if not f:
        raise HTTPException(404, "Fornecedor nao encontrado")
    for k, v in fornecedor.model_dump(exclude_unset=True).items():
        setattr(f, k, v)
    f.validar()
    db.commit()
    db.refresh(f)
    return f


@router.delete("/{forn_id}", status_code=204)
def deletar(forn_id: int, db: Session = Depends(get_db)):
    f = db.query(Fornecedor).filter(Fornecedor.id == forn_id).first()
    if not f:
        raise HTTPException(404, "Fornecedor nao encontrado")
    db.delete(f)
    db.commit()
