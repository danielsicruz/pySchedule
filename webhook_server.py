from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'appointments.json'

@app.route('/webhook/bookings', methods=['POST'])
def receber_agendamento():
    novo_agendamento = request.json

    # Carregar agendamentos existentes
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    else:
        dados = {"value": []}

    # Adicionar novo agendamento
    dados["value"].append(novo_agendamento)

    # Salvar de volta no arquivo
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "Agendamento recebido com sucesso"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
