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
    filtered = []
    for appointment in appointments:
        locations_str = appointment.get('locations', '')
        try:
            locations = json.loads(locations_str)
            for loc in locations:
                if room_name.lower() in loc.get('DisplayName', '').lower():
                    filtered.append(appointment)
                    break
        except json.JSONDecodeError:
            continue
    return filtered


# Função para formatar a data e hora
def format_datetime(datetime_str):
    try:
        # Converte a string de data e hora ISO 8601 para objeto datetime
        dt_obj = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
        # Ajusta o fuso horário para GMT-3
        dt_obj = dt_obj.replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ)
        return dt_obj.strftime('%d/%m/%Y %H:%M')  # Exemplo: "10/08/2025 09:00"
    except ValueError:
        return "N/A"


def parse_custom_datetime(datetime_str):
    try:
        dt_obj = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
        dt_obj = BRASILIA_TZ.localize(dt_obj)
        return dt_obj
    except ValueError:
        return None


# Função para filtrar os agendamentos futuros
def filter_appointments_future(appointments):
    now = datetime.now(BRASILIA_TZ)  # Hora atual no fuso horário GMT-3
    
    filtered_appointments = []
    
    for appointment in appointments:
        end_time_str = appointment.get('end', {})
        if end_time_str:
            # Converte a data de término em string para objeto datetime e ajusta para o fuso horário GMT-3
            end_time = datetime.strptime(end_time_str, '%m/%d/%Y %I:%M:%S %p').replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ)
            # Verifica se o agendamento é futuro
            if end_time >= now:
                filtered_appointments.append(appointment)
    
    return filtered_appointments

# Função para ordenar os agendamentos por start_time
def sort_appointments_by_start_time(appointments):
    return sorted(appointments, key=lambda x: datetime.strptime(x['start'], '%m/%d/%Y %I:%M:%S %p').replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ))
