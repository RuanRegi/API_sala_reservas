from datetime import datetime, date
from domain.usuario import Usuario
from domain.sala import Sala
from domain.reserva import Reserva
from repositories.memory import db

def criar_usuario(nome: str, email: str):
    if not nome or not email:
        raise ValueError("Nome e email são obrigatórios")

    for u in db.usuarios.values():
        if u.email == email:
            raise ValueError("Email já cadastrado")

    usuario = Usuario(db.next_usuario_id, nome, email)
    db.usuarios[usuario.id] = usuario
    db.next_usuario_id += 1
    return usuario

def listar_usuarios():
    return list(db.usuarios.values())

def criar_sala(nome: str, capacidade: int, bloco: str):
    if not nome:
        raise ValueError("Nome da sala é obrigatório")

    if capacidade <= 0:
        raise ValueError("Capacidade deve ser maior que zero")

    sala = Sala(db.next_sala_id, nome, capacidade, bloco)
    db.salas[sala.id] = sala
    db.next_sala_id += 1
    return sala

def listar_salas():
    return list(db.salas.values())

def criar_reserva(usuario_id: int, sala_id: int, data: str, hora_inicio: str, hora_fim: str):
    if usuario_id not in db.usuarios:
        raise ValueError("Usuário não existe")

    if sala_id not in db.salas:
        raise ValueError("Sala não existe")

    inicio = datetime.strptime(hora_inicio, "%H:%M")
    fim = datetime.strptime(hora_fim, "%H:%M")

    if fim <= inicio:
        raise ValueError("Hora final deve ser maior que a inicial")

    hoje = date.today().strftime("%Y-%m-%d")
    if data < hoje:
        raise ValueError("Não pode reservar para o passado")

    nova = Reserva(
        db.next_reserva_id,
        usuario_id,
        sala_id,
        data,
        hora_inicio,
        hora_fim
    )

    if nova.duracao_em_horas() > 2:
        raise ValueError("Duração máxima é de 2 horas")

    for r in db.reservas.values():

        if r.status != "active":
            continue

        if r.sala_id == sala_id and nova.conflita_com(r):
            raise ValueError("Conflito de horário na sala")

        if r.usuario_id == usuario_id and nova.conflita_com(r):
            raise ValueError("Usuário já possui reserva nesse horário")

    reservas_usuario_dia = [
        r for r in db.reservas.values()
        if r.usuario_id == usuario_id and r.data == data and r.status == "active"
    ]

    if len(reservas_usuario_dia) >= 2:
        raise ValueError("Usuário já possui 2 reservas nesse dia")

    db.reservas[nova.id] = nova
    db.next_reserva_id += 1

    return nova

def listar_reservas():
    return list(db.reservas.values())

def listar_reservas_usuario(usuario_id: int):
    return [r for r in db.reservas.values() if r.usuario_id == usuario_id]

def buscar_reserva(reserva_id: int):
    if reserva_id not in db.reservas:
        raise ValueError("Reserva não encontrada")
    return db.reservas[reserva_id]

def cancelar_reserva(reserva_id: int):
    reserva = buscar_reserva(reserva_id)
    reserva.cancelar()
    return reserva

def finalizar_reserva(reserva_id: int, hora_atual: str):
    reserva = buscar_reserva(reserva_id)
    reserva.finalizar(hora_atual)
    return reserva