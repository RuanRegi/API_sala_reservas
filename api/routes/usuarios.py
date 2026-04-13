from fastapi import APIRouter, HTTPException
from schemas.usuario import UsuarioCreate
from services.reserva_service import criar_usuario, listar_usuarios

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("")
def criar_usuario_route(data: UsuarioCreate):
    try:
        return criar_usuario(data.nome, data.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def listar_usuarios_route():
    return listar_usuarios()