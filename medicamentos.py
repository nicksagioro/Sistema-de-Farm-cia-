from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Medicamento
from schemas import MedicamentoCreate, MedicamentoUpdate, MedicamentoResponse

router = APIRouter(prefix="/api/medicamentos", tags=["medicamentos"])


@router.get("", response_model=list[MedicamentoResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Medicamento).offset(skip).limit(limit).all()


@router.get("/{med_id}", response_model=MedicamentoResponse)
def obter(med_id: int, db: Session = Depends(get_db)):
    m = db.query(Medicamento).filter(Medicamento.id == med_id).first()
    if not m:
        raise HTTPException(404, "Medicamento nao encontrado")
    return m


@router.post("", response_model=MedicamentoResponse, status_code=201)
def criar(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    if db.query(Medicamento).filter(Medicamento.nome == medicamento.nome).first():
        raise HTTPException(400, "Medicamento com este nome ja existe")
    novo = Medicamento(**medicamento.model_dump())
    novo.validar()
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.put("/{med_id}", response_model=MedicamentoResponse)
def atualizar(med_id: int, medicamento: MedicamentoUpdate,
              db: Session = Depends(get_db)):
    m = db.query(Medicamento).filter(Medicamento.id == med_id).first()
    if not m:
        raise HTTPException(404, "Medicamento nao encontrado")
    for k, v in medicamento.model_dump(exclude_unset=True).items():
        setattr(m, k, v)
    m.validar()
    db.commit()
    db.refresh(m)
    return m


@router.delete("/{med_id}", status_code=204)
def deletar(med_id: int, db: Session = Depends(get_db)):
    m = db.query(Medicamento).filter(Medicamento.id == med_id).first()
    if not m:
        raise HTTPException(404, "Medicamento nao encontrado")
    db.delete(m)
    db.commit()
