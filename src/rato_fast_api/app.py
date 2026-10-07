from fastapi import FastAPI 
from pydantic import BaseModel
from datetime import datetime, timezone, date 
import uuid

class CriarPessoa(BaseModel):
    nome_completo: str
    cpf: str
    email: str 
    data_nascimento: date
    telefone: str | None = None

class RetornarPessoa(CriarPessoa):
    id: uuid.UUID 
    ativo: bool 
    criado_em: datetime 
    atualizado_em: datetime

app = FastAPI() 

lista_de_pessoas_saida = []

@app.get("/health") 
async def health_check():
    return {"status": "OK"}

@app.post("/api/v1/pessoas", status_code=201)
async def criar_pessoa(pessoa_entrada: CriarPessoa):
    agora = datetime.now(timezone.utc)
    pessoa_saida = RetornarPessoa(
        **pessoa_entrada.model_dump(),
        id = uuid.uuid4(), 
        ativo = True, 
        criado_em = agora, 
        atualizado_em = agora)
    lista_de_pessoas_saida.append(pessoa_saida)
    return pessoa_saida

