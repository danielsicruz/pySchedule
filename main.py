import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import pytz  # Importando pytz para fuso horário


# Definir o fuso horário GMT-3 (Horário de Brasília)
BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')

room_name = "Sala 1"
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

# Função para filtrar os agendamentos com base no nome da sala
def filter_appointments_by_room(room_name, appointments):
    return [appointment for appointment in appointments if room_name.lower() in appointment['location']['displayName'].lower()]

# Função para filtrar os agendamentos futuros
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

# Função para atualizar a tabela com os agendamentos filtrados
def update_appointments():
    
    appointments = load_appointments_from_json('appointments.json')  # Caminho para o arquivo JSON
    
    # Filtrar os agendamentos com base na sala
    filtered_appointments = filter_appointments_by_room(room_name, appointments)
    
    # Filtrar os agendamentos futuros
    filtered_appointments = filter_appointments_future(filtered_appointments)

    # Ordenar os agendamentos por horário de início (start_time)
    sorted_appointments = sort_appointments_by_start_time(filtered_appointments)

    # Limpar a tabela existente
    for row in tree.get_children():
        tree.delete(row)
    
    # Preencher a tabela com os novos agendamentos
    for appointment in sorted_appointments:
        start_time = format_datetime(appointment.get('start', {}).get('dateTime', 'N/A'))
        end_time = format_datetime(appointment.get('end', {}).get('dateTime', 'N/A'))
        subject = appointment.get('subject', 'Sem assunto')
        location = appointment.get('location', {}).get('displayName', 'Sem local')
        organizer = appointment.get('organizer',{}).get('emailAddress', {}).get('name','Não definido')

        
        tree.insert('', 'end', values=(subject, start_time, end_time, location, organizer))
    
    # Atualizar a tabela a cada 10 segundos (pode ser ajustado)
    window.after(10000, update_appointments)

# Criar janela principal
window = tk.Tk()
window.title("Agenda da Sala")

# Criar a tabela para mostrar os agendamentos
columns = ("Subject", "Start Time", "End Time", "Location", "Organizer")
tree = ttk.Treeview(window, columns=columns, show="headings")

tree.heading("Subject", text="Assunto")
tree.heading("Start Time", text="Início")
tree.heading("End Time", text="Fim")
tree.heading("Location", text="Local")
tree.heading("Organizer", text="Organizador")

tree.pack(fill=tk.BOTH, expand=True)

# Iniciar atualização da tabela
update_appointments()

# Rodar a interface
window.mainloop()
