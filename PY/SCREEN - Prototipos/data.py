import tkinter as tk
from tkinter import filedialog, messagebox

def criar_janela_abrir_arquivo():
    """Cria uma janela com botão para abrir arquivo"""
    
    def abrir_arquivo():
        # Abrir diálogo para selecionar arquivo
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[
                ("Arquivos CSV", "*.csv"),
                ("Arquivos de texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        # Verificar se o usuário selecionou um arquivo
        if caminho_arquivo:
            # Mostrar informações do arquivo selecionado
            nome_arquivo = caminho_arquivo.split("/")[-1]  # Pega apenas o nome do arquivo
            label_status.config(text=f"Arquivo selecionado: {nome_arquivo}")
            messagebox.showinfo("Arquivo Selecionado", f"Você selecionou:\n{caminho_arquivo}")
        else:
            label_status.config(text="Nenhum arquivo selecionado")
    
    # Criar a janela principal
    janela = tk.Tk()
    janela.title("Abrir Arquivo")
    janela.geometry("400x200")
    janela.resizable(True, True)
    
    # Configurar o grid para centralizar
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(1, weight=1)
    
    # Título
    label_titulo = tk.Label(
        janela, 
        text="Seletor de Arquivos", 
        font=("Arial", 16, "bold"),
        fg="blue"
    )
    label_titulo.grid(row=0, column=0, pady=20)
    
    # Botão para abrir arquivo
    botao_abrir = tk.Button(
        janela,
        text="📁 Abrir Arquivo",
        command=abrir_arquivo,
        font=("Arial", 12),
        bg="lightblue",
        fg="black",
        padx=20,
        pady=10,
        cursor="hand2"
    )
    botao_abrir.grid(row=1, column=0, pady=10)
    
    # Label para mostrar status
    label_status = tk.Label(
        janela,
        text="Nenhum arquivo selecionado",
        font=("Arial", 10),
        fg="gray"
    )
    label_status.grid(row=2, column=0, pady=10)
    
    # Instruções
    label_instrucoes = tk.Label(
        janela,
        text="Clique no botão acima para selecionar um arquivo",
        font=("Arial", 9),
        fg="darkgreen"
    )
    label_instrucoes.grid(row=3, column=0, pady=5)
    
    return janela

# Executar a aplicação
if __name__ == "__main__":
    app = criar_janela_abrir_arquivo()
    app.mainloop()