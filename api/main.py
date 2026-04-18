from fastapi import FastAPI
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/voos")

def listar_voos():
    
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "flights")
    )
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voos")

    return cursor.fetchall()