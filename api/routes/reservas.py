from fastapi import APIRouter, HTTPException, Query
from schemas.reserva import ReservaCreate
from services.reserva_service import (
    criar_reserva,
    listar_reservas,
    listar_reservas_usuario,
    buscar_reserva,
    cancelar_reserva,
    finalizar_reserva
)
from repositories.memory import db

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("")
def criar_reserva_route(data: ReservaCreate):
    try:
        return criar_reserva(
            data.usuario_id,
            data.sala_id,
            data.data,
            data.hora_inicio,
            data.hora_fim
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
def listar_reservas_route(data: str = Query(None)):
    reservas = listar_reservas()

    if data:
        reservas = [r for r in reservas if r.data == data]

    return reservas


@router.get("/usuario/{usuario_id}")
def listar_reservas_usuario_route(usuario_id: int):
    return listar_reservas_usuario(usuario_id)


@router.get("/{reserva_id}")
def buscar_reserva_route(reserva_id: int):
    try:
        return buscar_reserva(reserva_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{reserva_id}/cancelar")
def cancelar_reserva_route(reserva_id: int):
    try:
        return cancelar_reserva(reserva_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{reserva_id}/finalizar")
def finalizar_reserva_route(
    reserva_id: int,
    hora_atual: str = Query(...)
):
    try:
        return finalizar_reserva(reserva_id, hora_atual)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/disponiveis/")
def salas_disponiveis(data: str, hora_inicio: str, hora_fim: str):
    from domain.reserva import Reserva

    reservas = listar_reservas()
    salas_disponiveis = []

    reserva_fake = Reserva(
        0, 0, 0, data, hora_inicio, hora_fim
    )

    for sala in db.salas.values():
        conflito = False

        for r in reservas:
            if r.sala_id == sala.id and r.status == "active":
                if reserva_fake.conflita_com(r):
                    conflito = True
                    break

        if not conflito:
            salas_disponiveis.append(sala)

    return salas_disponiveis


@router.post("/bloquear_sala/{sala_id}")
def bloquear_sala(sala_id: int, data: str, hora_inicio: str, hora_fim: str):
    if sala_id not in db.salas:
        raise HTTPException(status_code=404, detail="Sala não encontrada")

    try:
        reserva = criar_reserva(1, sala_id, data, hora_inicio, hora_fim)
        reserva.status = "maintenance"
        return reserva
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/resumo/{usuario_id}")
def resumo_usuario(usuario_id: int):
    reservas = listar_reservas_usuario(usuario_id)

    total = len(reservas)
    ativas = len([r for r in reservas if r.status == "active"])
    canceladas = len([r for r in reservas if r.status == "canceled"])
    finalizadas = len([r for r in reservas if r.status == "finished"])

    return {
        "usuario_id": usuario_id,
        "total_reservas": total,
        "ativas": ativas,
        "canceladas": canceladas,
        "finalizadas": finalizadas
    }