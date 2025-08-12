import json
from datetime import datetime
import pytz

# Definir o fuso horário GMT-3 (Horário de Brasília)
BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

# Função para carregar dados de agendamento de um arquivo JSON
def load_appointments_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['value']

# Função para filtrar os agendamentos com base no nome da sala
def filter_appointments_by_room(room_name, appointments):
    return [appointment for appointment in appointments if room_name.lower() in appointment['location']['displayName'].lower()]

# Função para formatar a data e hora
def format_datetime(datetime_str):
    try:
        # Converte a string de data e hora ISO 8601 para objeto datetime
        dt_obj = datetime.fromisoformat(datetime_str.replace('T', ' '))
        # Ajusta o fuso horário para GMT-3
        dt_obj = dt_obj.replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ)
        return dt_obj.strftime('%d/%m/%Y %H:%M')  # Exemplo: "10/08/2025 09:00"
    except ValueError:
        return "N/A"

# Função para filtrar os agendamentos futuros
def filter_appointments_future(appointments):
    now = datetime.now(BRASILIA_TZ)  # Hora atual no fuso horário GMT-3
    
    filtered_appointments = []
    
    for appointment in appointments:
        end_time_str = appointment.get('end', {}).get('dateTime', None)
        if end_time_str:
            # Converte a data de término em string para objeto datetime e ajusta para o fuso horário GMT-3
            end_time = datetime.fromisoformat(end_time_str.replace('T', ' ')).replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ)
            # Verifica se o agendamento é futuro
            if end_time >= now:
                filtered_appointments.append(appointment)
    
    return filtered_appointments

# Função para ordenar os agendamentos por start_time
def sort_appointments_by_start_time(appointments):
    return sorted(appointments, key=lambda x: datetime.fromisoformat(x['start']['dateTime'].replace('T', ' ')).replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ))
