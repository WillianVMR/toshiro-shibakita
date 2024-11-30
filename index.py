from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import random
import string
import socket

app = FastAPI()

# Configuração do banco de dados
DB_CONFIG = {
    "host": "54.234.153.24",
    "user": "root",
    "password": "Senha123",
    "database": "meubanco",
}

# Modelo de dados para inserir
class DataModel(BaseModel):
    aluno_id: int
    nome: str
    sobrenome: str
    endereco: str
    cidade: str
    host: str

@app.post("/insert")
async def insert_data():
    try:
        # Gerar dados aleatórios
        valor_rand1 = random.randint(1, 999)
        valor_rand2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        host_name = socket.gethostname()

        # Conexão com o banco de dados
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = """
        INSERT INTO dados (AlunoID, Nome, Sobrenome, Endereco, Cidade, Host)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (valor_rand1, valor_rand2, valor_rand2, valor_rand2, valor_rand2, host_name)

        # Executar o comando
        cursor.execute(query, values)
        connection.commit()

        return {"message": "New record created successfully", "id": valor_rand1}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
