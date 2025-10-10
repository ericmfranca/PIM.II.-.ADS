import tkinter as tk
from tkinter import messagebox
import subprocess

def iniciar_app():
    subprocess.Popen(["python", "data.py"])
    janela.destroy()

def sair_app():
    if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
        janela.destroy()

# Janela principal
janela = tk.Tk()
janela.title("Tela Inicial")
janela.geometry("800x600")
janela.configure(bg="#f0f0f0")

# Título
titulo = tk.Label(janela, text="Adicionar Titulo do PIM", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
titulo.pack(pady=20)

# Campo de texto para exibir dados do CSV
campo_dados = tk.Text(janela, height=15, width=80, font=("Courier", 10))
campo_dados.pack(pady=10)

# Frame para alinhar os botões horizontalmente
frame_botoes = tk.Frame(janela, bg="#f0f0f0")
frame_botoes.pack(pady=10)

# Botão "Iniciar"
botao_iniciar = tk.Button(frame_botoes, text="Iniciar", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=iniciar_app)
botao_iniciar.pack(side=tk.LEFT, padx=10)

# Botão "Sair"
botao_sair = tk.Button(frame_botoes, text="Sair", font=("Helvetica", 12), bg="#f44336", fg="white", command=sair_app)
botao_sair.pack(side=tk.LEFT, padx=10)

# Rodapé
rodape = tk.Label(janela, text="© 2025 PIM II Inc.", font=("Helvetica", 10), bg="#f0f0f0")
rodape.pack(side="bottom", pady=10)

# Loop da interface
janela.mainloop()
# Fim do código