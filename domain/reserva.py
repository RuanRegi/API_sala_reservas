from datetime import datetime

class Reserva:
    def __init__(
        self,
        id: int,
        usuario_id: int,
        sala_id: int,
        data: str,
        hora_inicio: str,
        hora_fim: str,
        status: str = "active"
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.sala_id = sala_id
        self.data = data
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.status = status

    def cancelar(self):
        if self.status != "active":
            raise ValueError("Apenas reservas ativas podem ser canceladas")
        self.status = "canceled"

    def finalizar(self, hora_atual: str):
        if self.status != "active":
            raise ValueError("Apenas reservas ativas podem ser finalizadas")

        fim = datetime.strptime(self.hora_fim, "%H:%M")
        atual = datetime.strptime(hora_atual, "%H:%M")

        if atual < fim:
            raise ValueError("Só pode finalizar após o horário de término")

        self.status = "finished"

    def duracao_em_horas(self) -> float:
        inicio = datetime.strptime(self.hora_inicio, "%H:%M")
        fim = datetime.strptime(self.hora_fim, "%H:%M")
        return (fim - inicio).seconds / 3600

    def conflita_com(self, outra_reserva) -> bool:
        if self.data != outra_reserva.data:
            return False

        inicio1 = datetime.strptime(self.hora_inicio, "%H:%M")
        fim1 = datetime.strptime(self.hora_fim, "%H:%M")

        inicio2 = datetime.strptime(outra_reserva.hora_inicio, "%H:%M")
        fim2 = datetime.strptime(outra_reserva.hora_fim, "%H:%M")

        return inicio1 < fim2 and inicio2 < fim1