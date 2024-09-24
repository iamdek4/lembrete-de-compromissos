import json
import os
import schedule  # type: ignore
import time
import threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

backup_file = 'agendamentos.json'
agendamentos = []
agendamentos_concluidos = []

def carregar_agendamentos():
    global agendamentos, agendamentos_concluidos
    agendamentos_concluidos = []
    if os.path.exists(backup_file):
        with open(backup_file, 'r') as f:
            try:
                data = json.load(f)
                agendamentos = [(datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S'), item[1]) for item in data['agendamentos']]
                agendamentos_concluidos = data['concluidos']
            except (ValueError, KeyError):
                agendamentos = []
                agendamentos_concluidos = []

def salvar_agendamentos():
    with open(backup_file, 'w') as f:
        json.dump({'agendamentos': [(data.strftime('%Y-%m-%d %H:%M:%S'), desc) for data, desc in agendamentos],
                    'concluidos': agendamentos_concluidos}, f)

def adicionar_agendamento(data_hora, descricao):
    global agendamentos
    try:
        data_hora = datetime.strptime(data_hora, '%d/%m/%Y %H:%M')
        agendamentos.append((data_hora, descricao))
        salvar_agendamentos()
        messagebox.showinfo("Sucesso", f"Agendamento adicionado: {data_hora.strftime('%d/%m/%Y %H:%M')} - {descricao}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao adicionar agendamento: {e}")

def beep():
    if os.name == 'nt':
        import winsound
        winsound.Beep(1000, 500)
    else:
        os.system('echo -n "\a"; sleep 0.5')

def notificar_agendamentos():
    agora = datetime.now()
    global agendamentos_concluidos
    for data, descricao in agendamentos[:]:
        if agora >= data:
            agendamentos_concluidos.append(descricao)
            agendamentos.remove((data, descricao))
            beep()
            messagebox.showinfo("Notificação", f"{descricao} em {data.strftime('%d/%m/%Y %H:%M')} - Agendamento concluído.")
    salvar_agendamentos()

def verificar_agendamentos():
    while True:
        notificar_agendamentos()
        time.sleep(60)

def adicionar_agendamento_interface():
    data_hora = entry_data.get() + " " + entry_hora.get()
    descricao = entry_descricao.get()
    adicionar_agendamento(data_hora, descricao)

carregar_agendamentos()
threading.Thread(target=verificar_agendamentos, daemon=True).start()

root = tk.Tk()
root.title("Agendador de Compromissos")

tk.Label(root, text="Data (dd/mm/yyyy):").pack()
entry_data = tk.Entry(root)
entry_data.pack()

tk.Label(root, text="Hora (hh:mm):").pack()
entry_hora = tk.Entry(root)
entry_hora.pack()

tk.Label(root, text="Descrição:").pack()
entry_descricao = tk.Entry(root)
entry_descricao.pack()

tk.Button(root, text="Adicionar Agendamento", command=adicionar_agendamento_interface).pack()

root.mainloop()
