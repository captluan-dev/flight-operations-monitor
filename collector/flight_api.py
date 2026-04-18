from dotenv import load_dotenv
import os

import requests
import pprint

load_dotenv()

def buscar_voos(airline=None, origin=None, arrival=None, status=None):

    api_key = os.getenv("API_KEY")
    url = "https://api.aviationstack.com/v1/flights"

    parameter = {
        "access_key": api_key,
        "airline_icao": airline,
        "dep_iata": origin,
        "arr_iata": arrival,
        "flight_status": status,
        "limit": 10
    }

    response = requests.get(url, params=parameter)

    if response.status_code == 200:
        request_data = response.json()
        # pprint.pprint(request_data)

        return request_data.get("data", [])
    
    else:
        print("Erro na API")
        return []