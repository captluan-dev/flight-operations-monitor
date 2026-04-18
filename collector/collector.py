import mysql.connector
from dotenv import load_dotenv
import os
from flight_api import buscar_voos

load_dotenv()

def exibir_aviso(origem, destino):

    if not origem or not destino:
        print("\n" + "-" * 50)
        print("AVISO: Sem filtros de aeroporto, você verá voos")
        print("de companhias parceiras (Codeshare) no resultado.")
        print("-" * 50 + "\n")

def menu_principal():

    print("1 - Buscar por Companhia")
    print("2 - Buscar por Rota Específica")

    opcao = int(input("Escolha: "))

    match opcao:
        case 1:
            companhia = input("Código ICAO da Cia (ex: GLO): ")
            exibir_aviso(None, None)
            coletar(companhia=companhia)
        case 2:
            companhia = input("Código ICAO da Cia (ex: GLO): ")
            origem = input("Código IATA de Origem (ex: BSB): ")
            destino = input("Código IATA de Destino (ex: GRU): ")
            coletar(companhia=companhia, origem=origem, destino=destino)
        
def conectar():

    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "flights")
    )
    return db

def coletar(companhia=None, origem=None, destino=None):

    conn = conectar()
    cursor = conn.cursor()

    voos = buscar_voos(airline=companhia, origin=origem, arrival=destino)
    inserted = 0

    for voo in voos[:10]:
        numero_voo = voo.get("flight", {}).get("iata")
        origem = voo.get("departure", {}).get("iata")
        destino = voo.get("arrival", {}).get("iata")

        status = voo.get("flight_status")
        status = status.lower() if status else "unknown"

        if not numero_voo:
            continue

        query = """
        INSERT INTO voos (numero_voo, origem, destino, status, horario_coleta)
        VALUES (%s, %s, %s, %s, NOW())
        """

        dados = (numero_voo, origem, destino, status)

        cursor.execute(query, dados)
        inserted += 1

    conn.commit()

    print(f"{inserted} voos inseridos!")

if __name__ == "__main__":
    menu_principal()