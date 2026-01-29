import requests
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN não encontrado no arquivo .env")

BASE_URL = "https://api.pandascore.co/csgo"

def get_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

def buscar_proximas_partidas():
    response = requests.get(f"{BASE_URL}/matches/upcoming", headers=get_headers())
    return response.json() if response.status_code == 200 else []

def buscar_partidas_ao_vivo():
    response = requests.get(f"{BASE_URL}/matches/running", headers=get_headers())
    return response.json() if response.status_code == 200 else []

def buscar_partidas_passadas():
    response = requests.get(f"{BASE_URL}/matches/past", headers=get_headers())
    return response.json() if response.status_code == 200 else []

def torneios_cs():
    response = requests.get(f"{BASE_URL}/tournaments", headers=get_headers())
    return response.json() if response.status_code == 200 else []

def buscar_torneio(tournament_id):
    url = f"https://api.pandascore.co/tournaments/{tournament_id}"
    
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None

def buscar_time(team_id):
    # A rota da PandaScore para um time específico
    url = f"https://api.pandascore.co/teams/{team_id}"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None
def buscar_times_por_nome(nome_time):
    """Busca times por nome na API PandaScore"""
    try:
        # Usar o endpoint de times com filtro de search
        response = requests.get(
            f"https://api.pandascore.co/teams",
            headers=get_headers(),
            params={
                "search[name]": nome_time,
                "per_page": 20
            }
        )
        
        if response.status_code == 200:
            times = response.json()
            # Filtrar e formatar os dados dos times
            times_formatados = []
            for time in times:
                # Extrair país de diferentes campos possíveis
                pais = (
                    time.get('country') or 
                    time.get('location') or 
                    time.get('name', 'País desconhecido')
                )
                
                times_formatados.append({
                    'id': time.get('id'),
                    'name': time.get('name'),
                    'country': pais,
                    'image_url': time.get('image_url'),
                    'location': time.get('location'),
                    'acronym': time.get('acronym')
                })
            return times_formatados
        return []
    except Exception as e:
        print(f"Erro ao buscar times: {e}")
        return []