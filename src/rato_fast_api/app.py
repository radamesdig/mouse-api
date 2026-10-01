
from fastapi import FastAPI  

app = FastAPI() 

@app.get("/health") 
async def health_check():
    return {"status": "OK"}

@app.get("/")
async def function():
    return {"message": "hello, World!"}
    

