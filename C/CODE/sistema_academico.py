import customtkinter as ctk
from tkinter import messagebox
import emoji
import pandas as pd
import tkinter as tk
from tkinter import ttk

# Configuração de tema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão Acadêmica (SiGA)")
        self.geometry("800x600")
        
        # Carregar dados do CSV
        self.carregar_dados()
        
        # Variáveis do sistema
        self.usuario_logado = None

        # Exibir a tela de login primeiro
        self.current_frame = None
        self.show_login_frame()

    def carregar_dados(self):
        """Carrega os dados do CSV gerado pelo programa em C"""
        try:
            self.df_usuarios = pd.read_csv('dados_usuarios.csv')
            self.df_notas = pd.read_csv('dados_notas.csv')
            print("✅ Dados carregados com sucesso!")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivos CSV não encontrados!")
            self.df_usuarios = pd.DataFrame()
            self.df_notas = pd.DataFrame()

    def switch_frame(self, frame):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def show_login_frame(self):
        login_frame = ctk.CTkFrame(self)
        
        title = ctk.CTkLabel(login_frame, text="Sistema de Gestão Acadêmica (SiGA)", font=("Arial bold", 30))
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(login_frame, text="Login de Acesso", font=("Arial", 14), text_color="gray")
        subtitle.pack(pady=(0, 20))

        # Frame para campos de entrada
        input_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        input_frame.pack(pady=20)

        ctk.CTkLabel(input_frame, text="RA:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.ra_entry = ctk.CTkEntry(input_frame, placeholder_text="Digite seu RA", width=250)
        self.ra_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Senha (Sobrenome):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.senha_entry = ctk.CTkEntry(input_frame, placeholder_text="Digite seu sobrenome", show="*", width=250)
        self.senha_entry.grid(row=1, column=1, padx=10, pady=5)

        # Frame para botões
        button_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        login_button = ctk.CTkButton(button_frame, text="Entrar", command=self.login, width=120)
        login_button.pack(pady=10)

        # Informações de login
        info_text = ctk.CTkLabel(login_frame, 
                                text="💡 Dicas de login:\n"
                                     "Aluno: ALUN## + Sobrenome\n"
                                     "Professor: PROF## + Sobrenome\n" 
                                     "Admin: ADM### + Sobrenome",
                                font=("Arial", 11),
                                text_color="gray",
                                justify="left")
        info_text.pack(pady=20)

        self.switch_frame(login_frame)

    def login(self):
        ra = self.ra_entry.get().strip().upper()
        senha = self.senha_entry.get().strip()

        if not ra or not senha:
            messagebox.showwarning("Login", "Por favor, preencha RA e senha!")
            return

        if self.df_usuarios.empty:
            messagebox.showerror("Erro", "Nenhum usuário cadastrado no sistema!")
            return

        # Buscar usuário no DataFrame
        usuario_encontrado = self.df_usuarios[self.df_usuarios['RA'] == ra]

        if usuario_encontrado.empty:
            messagebox.showerror("Login", "RA não encontrado!")
            return

        usuario = usuario_encontrado.iloc[0]
        sobrenome_correto = str(usuario['Sobrenome']).strip().lower()

        if senha.lower() != sobrenome_correto:
            messagebox.showerror("Login", "Senha incorreta!")
            return

        # Login bem-sucedido
        self.usuario_logado = {
            'ra': usuario['RA'],
            'nome': usuario['Nome'],
            'sobrenome': usuario['Sobrenome'],
            'tipo': usuario['Tipo'],
            'disciplina': usuario['Disciplina'] if 'Disciplina' in usuario and pd.notna(usuario['Disciplina']) else "N/A"
        }

        tipo_usuario = {1: "Aluno", 2: "Professor", 3: "Administrador"}[usuario['Tipo']]
        messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario['Nome']}!\nTipo: {tipo_usuario}")

        # Limpar campos e redirecionar
        self.ra_entry.delete(0, 'end')
        self.senha_entry.delete(0, 'end')
        self.redirecionar_por_tipo()

    def redirecionar_por_tipo(self):
        """Redireciona para a tela conforme o tipo de usuário"""
        tipo = self.usuario_logado['tipo']
        
        if tipo == 1:  # Aluno
            self.show_aluno_frame()
        elif tipo == 2:  # Professor
            self.show_professor_frame()
        elif tipo == 3:  # Admin
            self.show_admin_frame()

    def show_aluno_frame(self):
        aluno_frame = ctk.CTkFrame(self)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(aluno_frame, fg_color="transparent")
        header_frame.pack(pady=20)
        
        title = ctk.CTkLabel(header_frame, 
                            text=f"🎓 Área do Aluno",
                            font=("Arial bold", 24))
        title.pack()
        
        user_info = ctk.CTkLabel(header_frame,
                                text=f"{self.usuario_logado['nome']} {self.usuario_logado['sobrenome']} - {self.usuario_logado['ra']}",
                                font=("Arial", 14),
                                text_color="gray")
        user_info.pack(pady=5)

        # Abas
        tabview = ctk.CTkTabview(aluno_frame)
        tabview.pack(expand=True, fill="both", padx=20, pady=10)
        
        tabview.add("Notas e Faltas")
        tabview.add("Dados Pessoais")

        # Aba de Notas e Faltas
        self.mostrar_notas_aluno(tabview.tab("Notas e Faltas"))
        
        # Aba de Dados Pessoais
        dados_frame = tabview.tab("Dados Pessoais")
        info_text = f"""
        👤 DADOS PESSOAIS

        📋 RA: {self.usuario_logado['ra']}
        🧑‍🎓 Nome: {self.usuario_logado['nome']}
        📛 Sobrenome: {self.usuario_logado['sobrenome']}
        🎯 Tipo: Aluno

        💡 Funcionalidades disponíveis:
        • Consultar suas notas e faltas
        • Visualizar médias por disciplina
        • Verificar situação acadêmica
        """
        
        dados_label = ctk.CTkLabel(dados_frame, text=info_text, font=("Arial", 12), justify="left")
        dados_label.pack(pady=20)

        # Botão sair
        logout_button = ctk.CTkButton(aluno_frame, text="🚪 Sair", command=self.logout, fg_color="#E74C3C")
        logout_button.pack(pady=10)

        self.switch_frame(aluno_frame)

    def mostrar_notas_aluno(self, parent):
        """Mostra notas e faltas do aluno logado"""
        if self.df_notas.empty:
            lbl_sem_dados = ctk.CTkLabel(parent, text="📝 Nenhuma nota registrada ainda.", font=("Arial", 14))
            lbl_sem_dados.pack(expand=True)
            return
        
        # Filtrar notas do aluno
        notas_aluno = self.df_notas[self.df_notas['RA_Aluno'] == self.usuario_logado['ra']]
        
        if notas_aluno.empty:
            lbl_sem_dados = ctk.CTkLabel(parent, text="📝 Nenhuma nota encontrada para seu RA.", font=("Arial", 14))
            lbl_sem_dados.pack(expand=True)
            return

        # Frame com scroll
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Mostrar dados de cada disciplina
        for idx, disciplina in notas_aluno.iterrows():
            disc_frame = ctk.CTkFrame(scroll_frame)
            disc_frame.pack(fill="x", padx=5, pady=5)

            # Título da disciplina
            title = ctk.CTkLabel(disc_frame, 
                                text=f"📚 {disciplina['Disciplina']}",
                                font=("Arial bold", 14))
            title.pack(anchor="w", pady=(10, 5))

            # Cabeçalho da tabela
            header_frame = ctk.CTkFrame(disc_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=10)
            
            ctk.CTkLabel(header_frame, text="Bimestre", font=("Arial bold", 11), width=80).pack(side="left")
            ctk.CTkLabel(header_frame, text="Nota", font=("Arial bold", 11), width=60).pack(side="left")
            ctk.CTkLabel(header_frame, text="Faltas", font=("Arial bold", 11), width=60).pack(side="left")

            # Dados dos bimestres
            notas = []
            faltas_totais = 0
            
            for i in range(4):
                bim_frame = ctk.CTkFrame(disc_frame, fg_color="transparent")
                bim_frame.pack(fill="x", padx=10)
                
                nota_col = f'Nota_Bimestre_{i+1}'
                faltas_col = f'Faltas_Bimestre_{i+1}'
                
                nota = disciplina[nota_col] if nota_col in disciplina else 0
                faltas = disciplina[faltas_col] if faltas_col in disciplina else 0
                
                notas.append(nota)
                faltas_totais += faltas
                
                ctk.CTkLabel(bim_frame, text=f"{i+1}°", width=80).pack(side="left")
                ctk.CTkLabel(bim_frame, text=f"{nota:.1f}", width=60).pack(side="left")
                ctk.CTkLabel(bim_frame, text=f"{faltas}", width=60).pack(side="left")

            # Resumo
            media = sum(notas) / len(notas) if notas else 0
            status = "✅ APROVADO" if media >= 6.0 else "❌ REPROVADO"
            cor_status = "green" if media >= 6.0 else "red"
            
            resumo_frame = ctk.CTkFrame(disc_frame)
            resumo_frame.pack(fill="x", padx=10, pady=5)
            
            resumo_text = f"📈 Média: {media:.1f} | 📅 Faltas: {faltas_totais} | {status}"
            resumo_label = ctk.CTkLabel(resumo_frame, text=resumo_text, font=("Arial bold", 12))
            resumo_label.pack(pady=5)

    def show_professor_frame(self):
        professor_frame = ctk.CTkFrame(self)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(professor_frame, fg_color="transparent")
        header_frame.pack(pady=20)
        
        title = ctk.CTkLabel(header_frame, 
                            text=f"👨‍🏫 Área do Professor",
                            font=("Arial bold", 24))
        title.pack()
        
        user_info = ctk.CTkLabel(header_frame,
                                text=f"{self.usuario_logado['nome']} {self.usuario_logado['sobrenome']} - {self.usuario_logado['disciplina']}",
                                font=("Arial", 14),
                                text_color="gray")
        user_info.pack(pady=5)

        # Abas
        tabview = ctk.CTkTabview(professor_frame)
        tabview.pack(expand=True, fill="both", padx=20, pady=10)
        
        tabview.add("Consultar Alunos")
        tabview.add("Estatísticas")

        # Aba de Consultar Alunos
        self.mostrar_alunos_professor(tabview.tab("Consultar Alunos"))
        
        # Aba de Estatísticas
        self.mostrar_estatisticas_professor(tabview.tab("Estatísticas"))

        # Botão sair
        logout_button = ctk.CTkButton(professor_frame, text="🚪 Sair", command=self.logout, fg_color="#E74C3C")
        logout_button.pack(pady=10)

        self.switch_frame(professor_frame)

    def mostrar_alunos_professor(self, parent):
        """Mostra alunos para o professor"""
        alunos = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
        
        if alunos.empty:
            lbl_sem_alunos = ctk.CTkLabel(parent, text="Nenhum aluno cadastrado no sistema.", font=("Arial", 14))
            lbl_sem_alunos.pack(expand=True)
            return

        # Frame com scroll
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Cabeçalho
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(header_frame, text="RA", font=("Arial bold", 12), width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Nome", font=("Arial bold", 12), width=200).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Sobrenome", font=("Arial bold", 12), width=150).pack(side="left", padx=5)

        # Lista de alunos
        for _, aluno in alunos.iterrows():
            aluno_frame = ctk.CTkFrame(scroll_frame)
            aluno_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(aluno_frame, text=aluno['RA'], width=100).pack(side="left", padx=5)
            ctk.CTkLabel(aluno_frame, text=aluno['Nome'], width=200).pack(side="left", padx=5)
            ctk.CTkLabel(aluno_frame, text=aluno['Sobrenome'], width=150).pack(side="left", padx=5)

        # Informação do total
        total_frame = ctk.CTkFrame(parent, fg_color="transparent")
        total_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(total_frame, text=f"Total de alunos: {len(alunos)}", font=("Arial", 12)).pack()

    def mostrar_estatisticas_professor(self, parent):
        """Mostra estatísticas para o professor"""
        total_alunos = len(self.df_usuarios[self.df_usuarios['Tipo'] == 1])
        total_registros = len(self.df_notas) if not self.df_notas.empty else 0
        
        info_text = f"""
        📊 ESTATÍSTICAS DO SISTEMA

        👨‍🎓 Total de Alunos: {total_alunos}
        📝 Registros de Notas: {total_registros}
        📚 Sua Disciplina: {self.usuario_logado['disciplina']}

        💡 Funcionalidades disponíveis:
        • Consultar todos os alunos
        • Visualizar estatísticas
        • Acompanhar desempenho
        """
        
        info_label = ctk.CTkLabel(parent, text=info_text, font=("Arial", 12), justify="left")
        info_label.pack(pady=20)

    def show_admin_frame(self):
        admin_frame = ctk.CTkFrame(self)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(admin_frame, fg_color="transparent")
        header_frame.pack(pady=20)
        
        title = ctk.CTkLabel(header_frame, 
                            text=f"👨‍💼 Área do Administrador",
                            font=("Arial bold", 24))
        title.pack()
        
        user_info = ctk.CTkLabel(header_frame,
                                text=f"{self.usuario_logado['nome']} {self.usuario_logado['sobrenome']}",
                                font=("Arial", 14),
                                text_color="gray")
        user_info.pack(pady=5)

        # Abas
        tabview = ctk.CTkTabview(admin_frame)
        tabview.pack(expand=True, fill="both", padx=20, pady=10)
        
        tabview.add("Estatísticas Gerais")
        tabview.add("Todos os Usuários")

        # Aba de Estatísticas
        self.mostrar_estatisticas_admin(tabview.tab("Estatísticas Gerais"))
        
        # Aba de Usuários
        self.mostrar_todos_usuarios(tabview.tab("Todos os Usuários"))

        # Botão sair
        logout_button = ctk.CTkButton(admin_frame, text="🚪 Sair", command=self.logout, fg_color="#E74C3C")
        logout_button.pack(pady=10)

        self.switch_frame(admin_frame)

    def mostrar_estatisticas_admin(self, parent):
        """Mostra estatísticas gerais para o admin"""
        total_alunos = len(self.df_usuarios[self.df_usuarios['Tipo'] == 1])
        total_professores = len(self.df_usuarios[self.df_usuarios['Tipo'] == 2])
        total_admins = len(self.df_usuarios[self.df_usuarios['Tipo'] == 3])
        total_registros = len(self.df_notas) if not self.df_notas.empty else 0
        
        info_text = f"""
        📈 ESTATÍSTICAS COMPLETAS

        👥 TOTAL DE USUÁRIOS: {len(self.df_usuarios)}
        👨‍🎓 Alunos: {total_alunos}
        👨‍🏫 Professores: {total_professores}
        👨‍💼 Administradores: {total_admins}

        📊 REGISTROS ACADÊMICOS:
        📝 Registros de notas: {total_registros}

        💡 Funcionalidades disponíveis:
        • Visualizar todas as estatísticas
        • Gerenciar usuários do sistema
        • Acessar todos os registros
        """
        
        info_label = ctk.CTkLabel(parent, text=info_text, font=("Arial", 12), justify="left")
        info_label.pack(pady=20)

    def mostrar_todos_usuarios(self, parent):
        """Mostra todos os usuários para o admin"""
        if self.df_usuarios.empty:
            lbl_sem_dados = ctk.CTkLabel(parent, text="Nenhum usuário cadastrado.", font=("Arial", 14))
            lbl_sem_dados.pack(expand=True)
            return

        # Frame com scroll
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Cabeçalho
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(header_frame, text="RA", font=("Arial bold", 12), width=80).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Nome", font=("Arial bold", 12), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Sobrenome", font=("Arial bold", 12), width=120).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Tipo", font=("Arial bold", 12), width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Disciplina", font=("Arial bold", 12), width=120).pack(side="left", padx=5)

        # Lista de usuários
        for _, usuario in self.df_usuarios.iterrows():
            user_frame = ctk.CTkFrame(scroll_frame)
            user_frame.pack(fill="x", pady=2)
            
            tipo_str = {1: "Aluno", 2: "Professor", 3: "Admin"}[usuario['Tipo']]
            disciplina = usuario.get('Disciplina', 'N/A')
            
            ctk.CTkLabel(user_frame, text=usuario['RA'], width=80).pack(side="left", padx=5)
            ctk.CTkLabel(user_frame, text=usuario['Nome'], width=150).pack(side="left", padx=5)
            ctk.CTkLabel(user_frame, text=usuario['Sobrenome'], width=120).pack(side="left", padx=5)
            ctk.CTkLabel(user_frame, text=tipo_str, width=100).pack(side="left", padx=5)
            ctk.CTkLabel(user_frame, text=disciplina, width=120).pack(side="left", padx=5)

    def logout(self):
        self.usuario_logado = None
        messagebox.showinfo("Logout", "Você saiu do sistema!")
        self.show_login_frame()

if __name__ == "__main__":
    app = App()
    app.mainloop()