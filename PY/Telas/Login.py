import customtkinter as ctk
import csv
from tkinter import messagebox
from main_screen import abrir_tela_principal  # ajuste conforme nome da pasta

# Configuração da aparência da interface
ctk.set_appearance_mode("light")

# Função de validação de login
def validar_login():
    usuario_digitado = campo_usuario.get()
    senha_digitada = campo_senha.get()

    # Verifica se os campos estão preenchidos
    if not usuario_digitado or not senha_digitada:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    try:
        with open("../DOC/usuarios.csv", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                if linha["usuario"] == usuario_digitado and linha["senha"] == senha_digitada:
                    messagebox.showinfo("Login", "Login realizado com sucesso!")
                    app.destroy()
                    abrir_tela_principal()
                    return
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de usuários não encontrado.")

# Criação da janela principal
app = ctk.CTk()
app.title("Sistema de Login")
app.geometry("400x300")
app.configure(fg_color="#f0f0f0")

# Label usuário
label_usuario = ctk.CTkLabel(app, text="Usuário:")
label_usuario.pack(pady=10)

# Campo de usuário
campo_usuario = ctk.CTkEntry(app, placeholder_text="Digite seu usuário")
campo_usuario.pack(pady=10)

# Label senha
label_senha = ctk.CTkLabel(app, text="Senha:")
label_senha.pack(pady=10)

# Campo de senha
campo_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
campo_senha.pack(pady=10)

# Botão login
botao_login = ctk.CTkButton(app, text="Login", command=validar_login)
botao_login.pack(pady=20)

# Rodapé centralizado
rodape = ctk.CTkLabel(app, text="© 2025 PIM II Inc.", font=("Helvetica", 8))
rodape.place(relx=0.5, rely=1.0, anchor="s")

# Inicia o loop da aplicação
app.mainloop()