from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str