import tkinter as tk
from tkinter import ttk
from agenda_logic import *  # Importa todas as funções de lógica do arquivo agenda_logic.py

# Definir o nome da sala
room_name = "Sala 1"

# Função para verificar se o evento está em andamento
def is_event_in_progress(start_time_str, end_time_str):
    now = datetime.now(BRASILIA_TZ)  # Hora atual no fuso horário GMT-3
    start_time = datetime.fromisoformat(start_time_str.replace('T', ' ')).replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ)
    end_time = datetime.fromisoformat(end_time_str.replace('T', ' ')).replace(tzinfo=pytz.utc).astimezone(BRASILIA_TZ)
    
    # Verifica se a hora atual está dentro do intervalo do evento
    return start_time <= now <= end_time

# Função para atualizar a tabela com os agendamentos filtrados
def update_appointments():
    
    appointments = load_appointments_from_json('appointments.json')  # Caminho para o arquivo JSON
    
    # Filtrar os agendamentos com base na sala (Remover esse filtro no principal/server)
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

        # Verificar se o evento está em andamento
        in_progress = is_event_in_progress(appointment.get('start', {}).get('dateTime', ''), 
                                           appointment.get('end', {}).get('dateTime', ''))
        
        # Inserir os dados na tabela
        item_id = tree.insert('', 'end', values=(subject, start_time, end_time, location, organizer))
        # Se o evento estiver em andamento, aplicar o fundo amarelo
        if in_progress:
            tree.item(item_id, tags=('in_progress',))
    
    
    # Atualizar a tabela a cada 10 segundos (pode ser ajustado)
    window.after(10000, update_appointments)

# Criar janela principal
window = tk.Tk()
window.title("Agenda da Sala")
window.geometry("900x600")
#window.attributes('-fullscreen', 1)

# Alterar o fundo da janela principal para escuro
window.config(bg="#2e2e2e")

# Adicionando um título na interface
label_title = tk.Label(window, text="Agendamentos da Sala", font=("Arial", 16, "bold"),background="#2e2e2e", foreground="white")
label_title.pack(pady=10)

# Criar a tabela para mostrar os agendamentos
columns = ("Subject", "Start Time", "End Time", "Location", "Organizer")
tree = ttk.Treeview(window, columns=columns, show="headings", height=15)

tree.heading("Subject", text="Componente Curricular")
tree.heading("Start Time", text="Início")
tree.heading("End Time", text="Fim")
tree.heading("Location", text="Local")
tree.heading("Organizer", text="Organizador")

# Ajustar o tamanho das colunas
tree.column("Subject", width=200)
tree.column("Start Time", width=150)
tree.column("End Time", width=150)
tree.column("Location", width=200)
tree.column("Organizer", width=200)

# Estilo da tabela
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#3e3e3e", foreground="black")
style.configure("Treeview", font=("Arial", 10), rowheight=30, background="#555555", foreground="white",fieldbackground="#3e3e3e")
tree.tag_configure("in_progress", background="lightblue", foreground="black")

# Definir o fundo da área vazia da tabela (não preenchida)
style.configure("background", background="#2e2e2e")  # Cor escura para a área vazia

tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Iniciar atualização da tabela
update_appointments()

# Rodar a interface
window.mainloop()
