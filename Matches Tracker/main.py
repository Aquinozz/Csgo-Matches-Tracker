from flask import Flask, render_template
from api.reqs import buscar_partidas_passadas, buscar_proximas_partidas, buscar_partidas_ao_vivo
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/proximas')
def proximas():
    dados = buscar_proximas_partidas()
    return render_template('matches.html', matches=dados, titulo="Próximas Partidas")

@app.route('/ao-vivo')
def ao_vivo():
    dados = buscar_partidas_ao_vivo()
    return render_template('matches.html', matches=dados, titulo="Partidas Agora")

@app.route('/passadas')
def passadas():
    dados = buscar_partidas_passadas()
    return render_template('matches.html', matches=dados, titulo="Partidas Passadas")

@app.template_filter('br_time')
def br_time(value):
    if not value:
        return "Horário não disponível"
    try:
        # Converte a string da API para objeto datetime
        dt_utc = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
      
        dt_br = dt_utc - timedelta(hours=3)

        return dt_br.strftime("%d/%m/%Y %H:%M")
    except Exception as e:
        try:
             dt_utc = datetime.strptime(value, "%Y-%m-%dT%H:%M:%Z")
             dt_br = dt_utc - timedelta(hours=3)
             return dt_br.strftime("%d/%m/%Y %H:%M")
        except:
             return "Data Indisponível"

if __name__ == '__main__':
    app.run(debug=True)