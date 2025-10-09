import tkinter as tk
from tkinter import messagebox
import subprocess

def iniciar_app():
    subprocess.Popen(["python", "data.py"])
    janela.destroy()


# Ação ao clicar no botão "Sair"
def sair_app():
    janela.destroy()

# Janela principal
janela = tk.Tk()
janela.title("Tela Inicial")
janela.geometry("400x300")
janela.configure(bg="#f0f0f0")

# Título
titulo = tk.Label(janela, text="Adicionar Titulo do PIM", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
titulo.pack(pady=20)

# Botão "Iniciar"
botao_iniciar = tk.Button(janela, text="Iniciar", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=iniciar_app)
botao_iniciar.pack(pady=10)

# Botão "Sair"
botao_sair = tk.Button(janela, text="Sair", font=("Helvetica", 12), bg="#f44336", fg="white", command=sair_app)
botao_sair.pack(pady=5)

# Rodapé
rodape = tk.Label(janela, text="© 2025 PIM II Inc.", font=("Helvetica", 10), bg="#f0f0f0")
rodape.pack(side="bottom", pady=10)

# Loop da interface
janela.mainloop()
