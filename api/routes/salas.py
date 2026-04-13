from fastapi import APIRouter, HTTPException
from schemas.sala import SalaCreate
from services.reserva_service import criar_sala, listar_salas

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post("")
def criar_sala_route(data: SalaCreate):
    try:
        return criar_sala(data.nome, data.capacidade, data.bloco)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def listar_salas_route():
    return listar_salas()