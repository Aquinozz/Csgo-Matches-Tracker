import requests
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN não encontrado no arquivo .env")

BASE_URL = "https://api.pandascore.co/csgo/matches"

def get_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

def buscar_proximas_partidas():
    response = requests.get(f"{BASE_URL}/upcoming", headers=get_headers())
    return response.json() if response.status_code == 200 else []

def buscar_partidas_ao_vivo():
    response = requests.get(f"{BASE_URL}/running", headers=get_headers())
    return response.json() if response.status_code == 200 else []

def buscar_partidas_passadas():
    url = f"https://api.pandascore.co/csgo/matches/past?sort=-begin_at&per_page=10"
    response = requests.get(url, headers=get_headers())
    return response.json() if response.status_code == 200 else []