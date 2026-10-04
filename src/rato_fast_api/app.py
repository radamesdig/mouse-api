from fastapi import FastAPI 
from pydantic import BaseModel
from datetime import date 

class CriarPessoa(BaseModel):
    nome_completo: str
    cpf: str
    email: str 
    data_nascimento: date
    telefone: str | None = None

app = FastAPI() 

@app.get("/health") 
async def health_check():
    return {"status": "OK"}

@app.post("/api/v1/pessoas", status_code=201)
async def criar_pessoa(pessoa: CriarPessoa):
    return pessoa

