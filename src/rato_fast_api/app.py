# importa a classe FastAPI da biblioteca fastapi 
from fastapi import FastAPI  

# instancia a classe no objeto de nome bot
app = FastAPI() 

# cria a primeira rota para o endpoint /health e retorna uma mensagem simples 
# usamos o decorador com o método GET
# depois, usamos uma função assíncrona, que é chamada quando o usuário usa o endpoint /health
@app.get("/health") 
async def health_check():
    return {"status": "OK"}


    

