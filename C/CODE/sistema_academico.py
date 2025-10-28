import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para usar sem interface gráfica
from io import BytesIO
from PIL import Image, ImageTk
import numpy as np

# Configuração de tema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class DashboardManager:
    def __init__(self, df_usuarios, df_notas):
        self.df_usuarios = df_usuarios
        self.df_notas = df_notas
        self.setup_estilo_graficos()
    
    def setup_estilo_graficos(self):
        """Configura o estilo visual dos gráficos"""
        plt.style.use('default')
        self.cores = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6']
    
    def gerar_grafico_evolucao_turma(self, disciplina, professor_ra):
        """Gera gráfico de evolução das médias da turma por bimestre"""
        try:
            # Filtrar notas da disciplina do professor
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return None
            
            # Calcular médias por bimestre
            medias_bimestres = []
            for bimestre in range(1, 5):
                coluna_nota = f'Nota_Bimestre_{bimestre}'
                notas_bimestre = notas_disciplina[coluna_nota].replace(0, np.nan).dropna()
                if not notas_bimestre.empty:
                    media = notas_bimestre.mean()
                    medias_bimestres.append(media)
                else:
                    medias_bimestres.append(0)
            
            # Criar gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            bimestres = ['1° Bi', '2° Bi', '3° Bi', '4° Bi']
            
            bars = ax.bar(bimestres, medias_bimestres, color=self.cores, alpha=0.8)
            ax.set_ylabel('Média das Notas', fontsize=12, fontweight='bold')
            ax.set_xlabel('Bimestres', fontsize=12, fontweight='bold')
            ax.set_title(f'Evolução da Turma - {disciplina}', fontsize=14, fontweight='bold', pad=20)
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars, medias_bimestres):
                if valor > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                           f'{valor:.1f}', ha='center', va='bottom', fontweight='bold')
            
            ax.set_ylim(0, 10)
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            return self.fig_para_imagem(fig)
            
        except Exception as e:
            print(f"Erro ao gerar gráfico de evolução: {e}")
            return None
    
    def gerar_grafico_desempenho_individual(self, disciplina, professor_ra):
        """Gera gráfico de desempenho individual dos alunos"""
        try:
            # Filtrar notas da disciplina
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return None
            
            # Calcular médias dos alunos
            alunos_medias = []
            for _, row in notas_disciplina.iterrows():
                ra_aluno = row['RA_Aluno']
                notas = [row[f'Nota_Bimestre_{i}'] for i in range(1, 5)]
                notas_validas = [n for n in notas if n > 0]
                
                if notas_validas:
                    media = sum(notas_validas) / len(notas_validas)
                    # Buscar nome do aluno
                    aluno_info = self.df_usuarios[self.df_usuarios['RA'] == ra_aluno]
                    nome_aluno = aluno_info['Nome'].iloc[0] if not aluno_info.empty else ra_aluno
                    
                    alunos_medias.append({
                        'ra': ra_aluno,
                        'nome': nome_aluno,
                        'media': media,
                        'situacao': 'Aprovado' if media >= 6.0 else 'Reprovado'
                    })
            
            # Ordenar por média e pegar top 10
            alunos_medias.sort(key=lambda x: x['media'], reverse=True)
            alunos_top = alunos_medias[:10]
            
            if not alunos_top:
                return None
            
            # Criar gráfico
            fig, ax = plt.subplots(figsize=(12, 6))
            nomes = [f"{aluno['nome'][:15]}..." if len(aluno['nome']) > 15 else aluno['nome'] 
                    for aluno in alunos_top]
            medias = [aluno['media'] for aluno in alunos_top]
            cores = ['#2ECC71' if aluno['situacao'] == 'Aprovado' else '#E74C3C' 
                    for aluno in alunos_top]
            
            bars = ax.bar(nomes, medias, color=cores, alpha=0.8)
            ax.set_ylabel('Média Final', fontsize=12, fontweight='bold')
            ax.set_xlabel('Alunos', fontsize=12, fontweight='bold')
            ax.set_title(f'Top 10 Alunos - {disciplina}', fontsize=14, fontweight='bold', pad=20)
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars, medias):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       f'{valor:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
            
            ax.set_ylim(0, 10)
            plt.xticks(rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            return self.fig_para_imagem(fig)
            
        except Exception as e:
            print(f"Erro ao gerar gráfico individual: {e}")
            return None
    
    def gerar_grafico_distribuicao_notas(self, disciplina, professor_ra):
        """Gera gráfico de distribuição das notas"""
        try:
            # Filtrar notas da disciplina
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return None
            
            # Coletar todas as notas
            todas_notas = []
            for _, row in notas_disciplina.iterrows():
                for i in range(1, 5):
                    nota = row[f'Nota_Bimestre_{i}']
                    if nota > 0:
                        todas_notas.append(nota)
            
            if not todas_notas:
                return None
            
            # Criar histograma
            fig, ax = plt.subplots(figsize=(10, 6))
            n, bins, patches = ax.hist(todas_notas, bins=10, range=(0, 10), 
                                      color='#3498DB', alpha=0.7, edgecolor='black')
            
            ax.set_xlabel('Notas', fontsize=12, fontweight='bold')
            ax.set_ylabel('Quantidade de Alunos', fontsize=12, fontweight='bold')
            ax.set_title(f'Distribuição de Notas - {disciplina}', fontsize=14, fontweight='bold', pad=20)
            
            # Adicionar linha da média
            media = np.mean(todas_notas)
            ax.axvline(media, color='#E74C3C', linestyle='--', linewidth=2, 
                      label=f'Média: {media:.2f}')
            
            # Adicionar linha da nota mínima para aprovação
            ax.axvline(6.0, color='#2ECC71', linestyle='--', linewidth=2, 
                      label='Mínimo para Aprovação')
            
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            
            return self.fig_para_imagem(fig)
            
        except Exception as e:
            print(f"Erro ao gerar distribuição: {e}")
            return None
    
    def calcular_metricas_turma(self, disciplina, professor_ra):
        """Calcula métricas gerais da turma"""
        try:
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return {}
            
            # Coletar dados
            total_alunos = len(notas_disciplina)
            medias_alunos = []
            alunos_risco = []
            
            for _, row in notas_disciplina.iterrows():
                ra_aluno = row['RA_Aluno']
                notas = [row[f'Nota_Bimestre_{i}'] for i in range(1, 5)]
                notas_validas = [n for n in notas if n > 0]
                
                if notas_validas:
                    media = sum(notas_validas) / len(notas_validas)
                    medias_alunos.append(media)
                    
                    # Verificar se está em risco (nota < 6)
                    if media < 6.0:
                        aluno_info = self.df_usuarios[self.df_usuarios['RA'] == ra_aluno]
                        nome_aluno = aluno_info['Nome'].iloc[0] if not aluno_info.empty else ra_aluno
                        alunos_risco.append({
                            'nome': nome_aluno,
                            'media': media,
                            'ra': ra_aluno
                        })
            
            if not medias_alunos:
                return {}
            
            media_geral = np.mean(medias_alunos)
            taxa_aprovacao = len([m for m in medias_alunos if m >= 6.0]) / len(medias_alunos) * 100
            
            return {
                'total_alunos': total_alunos,
                'media_geral': media_geral,
                'taxa_aprovacao': taxa_aprovacao,
                'alunos_risco': alunos_risco,
                'melhor_nota': max(medias_alunos),
                'pior_nota': min(medias_alunos)
            }
            
        except Exception as e:
            print(f"Erro ao calcular métricas: {e}")
            return {}
    
    def fig_para_imagem(self, fig):
        """Converte figura matplotlib em imagem para tkinter"""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return Image.open(buf)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão Acadêmica (SiGA)")
        self.geometry("800x600")
        
        # Carregar dados do CSV
        self.carregar_dados()
        
        # Inicializar Dashboard Manager
        self.dashboard_manager = DashboardManager(self.df_usuarios, self.df_notas)
        
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
        # CORREÇÃO 3: Bind Enter key
        self.ra_entry.bind("<Return>", lambda event: self.login())

        ctk.CTkLabel(input_frame, text="Senha (Sobrenome):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.senha_entry = ctk.CTkEntry(input_frame, placeholder_text="Digite seu sobrenome", show="*", width=250)
        self.senha_entry.grid(row=1, column=1, padx=10, pady=5)
        # CORREÇÃO 3: Bind Enter key
        self.senha_entry.bind("<Return>", lambda event: self.login())

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
        
        tabview.add("Lançar Notas")
        tabview.add("Consultar Alunos")
        tabview.add("Cadastrar Aluno")  # NOVA ABA 🆕
        tabview.add("Dashboard")
        tabview.add("Estatísticas")

        # Aba de Lançar Notas
        self.mostrar_lancar_notas(tabview.tab("Lançar Notas"))
        
        # Aba de Consultar Alunos
        self.mostrar_alunos_professor(tabview.tab("Consultar Alunos"))
        
        # NOVA ABA: Cadastrar Aluno 🆕
        self.mostrar_cadastrar_aluno(tabview.tab("Cadastrar Aluno"))
        
        # Aba: Dashboard
        self.mostrar_dashboard_professor(tabview.tab("Dashboard"))
        
        # Aba de Estatísticas
        self.mostrar_estatisticas_professor(tabview.tab("Estatísticas"))

        # Botão sair
        logout_button = ctk.CTkButton(professor_frame, text="🚪 Sair", command=self.logout, fg_color="#E74C3C")
        logout_button.pack(pady=10)

        self.switch_frame(professor_frame)

    # ===============================
    # NOVA FUNCIONALIDADE: CADASTRAR ALUNO 🆕
    # ===============================

    def mostrar_cadastrar_aluno(self, parent):
        """Interface para professor cadastrar novos alunos"""
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="👨‍🎓 Cadastrar Novo Aluno",
            font=("Arial bold", 20)
        )
        title.pack(pady=10)

        # Informação do professor
        info_professor = ctk.CTkLabel(
            main_frame,
            text=f"Professor: {self.usuario_logado['nome']} | Disciplina: {self.usuario_logado['disciplina']}",
            font=("Arial", 12),
            text_color="blue"
        )
        info_professor.pack(pady=5)

        # Frame do formulário
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=20, padx=50)

        # Campo Nome
        ctk.CTkLabel(form_frame, text="Nome do Aluno:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        self.nome_aluno_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Digite o nome do aluno",
            width=300
        )
        self.nome_aluno_entry.pack(fill="x", pady=5, padx=10)

        # Campo Sobrenome
        ctk.CTkLabel(form_frame, text="Sobrenome do Aluno:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        self.sobrenome_aluno_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Digite o sobrenome do aluno",
            width=300
        )
        self.sobrenome_aluno_entry.pack(fill="x", pady=5, padx=10)

        # Informações automáticas
        info_auto_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        info_auto_frame.pack(fill="x", pady=10, padx=10)

        info_text = """
        💡 Informações que serão geradas automaticamente:
        • RA do aluno (ALUN##)
        • Status: Ativo
        • Tipo: Aluno
        • Disciplina vinculada: A mesma do professor
        """
        
        ctk.CTkLabel(
            info_auto_frame,
            text=info_text,
            font=("Arial", 10),
            text_color="green",
            justify="left"
        ).pack(anchor="w")

        # Botões
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        btn_cadastrar = ctk.CTkButton(
            button_frame,
            text="✅ Cadastrar Aluno",
            command=self.cadastrar_novo_aluno,
            fg_color="#27AE60",
            hover_color="#219955",
            height=40
        )
        btn_cadastrar.pack(side="left", padx=10)

        btn_limpar = ctk.CTkButton(
            button_frame,
            text="🔄 Limpar Campos",
            command=self.limpar_campos_cadastro,
            fg_color="#F39C12",
            hover_color="#E67E22",
            height=40
        )
        btn_limpar.pack(side="left", padx=10)

    def cadastrar_novo_aluno(self):
        """Cadastra um novo aluno no sistema"""
        nome = self.nome_aluno_entry.get().strip()
        sobrenome = self.sobrenome_aluno_entry.get().strip()

        # Validações
        if not nome or not sobrenome:
            messagebox.showwarning("Cadastro", "Por favor, preencha nome e sobrenome!")
            return

        if len(nome) < 2 or len(sobrenome) < 2:
            messagebox.showwarning("Cadastro", "Nome e sobrenome devem ter pelo menos 2 caracteres!")
            return

        try:
            # Gerar RA automático (ALUN##)
            alunos_existentes = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
            novo_numero = len(alunos_existentes) + 1
            novo_ra = f"ALUN{novo_numero:02d}"

            # Verificar se RA já existe (por segurança)
            while novo_ra in self.df_usuarios['RA'].values:
                novo_numero += 1
                novo_ra = f"ALUN{novo_numero:02d}"

            # Criar novo registro do aluno
            novo_aluno = {
                'RA': novo_ra,
                'Nome': nome,
                'Sobrenome': sobrenome,
                'Tipo': 1,  # Aluno
                'Disciplina': self.usuario_logado['disciplina'],
                'Ativo': 1  # Aluno ativo por padrão
            }

            # Adicionar ao DataFrame
            novo_df = pd.DataFrame([novo_aluno])
            self.df_usuarios = pd.concat([self.df_usuarios, novo_df], ignore_index=True)

            # Salvar no CSV
            self.df_usuarios.to_csv('dados_usuarios.csv', index=False)

            # Mensagem de sucesso
            mensagem = f"""
            ✅ Aluno cadastrado com sucesso!

            📋 RA: {novo_ra}
            🧑‍🎓 Nome: {nome} {sobrenome}
            📚 Disciplina: {self.usuario_logado['disciplina']}
            🟢 Status: Ativo

            💡 O aluno já pode receber notas e faltas!
            """
            
            messagebox.showinfo("Sucesso", mensagem)

            # Limpar campos
            self.limpar_campos_cadastro()

            # Recarregar dados
            self.carregar_dados()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {e}")

    def limpar_campos_cadastro(self):
        """Limpa os campos do formulário de cadastro"""
        self.nome_aluno_entry.delete(0, 'end')
        self.sobrenome_aluno_entry.delete(0, 'end')

    # ===============================
    # DASHBOARD DO PROFESSOR
    # ===============================

    def mostrar_dashboard_professor(self, parent):
        """Mostra dashboard com gráficos e métricas para o professor"""
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text=f"📊 Dashboard - {self.usuario_logado['disciplina']}",
            font=("Arial bold", 20)
        )
        title.pack(pady=10)

        # Frame de métricas rápidas
        metricas = self.dashboard_manager.calcular_metricas_turma(
            self.usuario_logado['disciplina'], 
            self.usuario_logado['ra']
        )
        
        if metricas:
            self.mostrar_metricas_rapidas(main_frame, metricas)
        
        # Frame principal com scroll para gráficos
        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(fill="both", expand=True, pady=10)

        # Gerar e mostrar gráficos
        self.mostrar_graficos_dashboard(scroll_frame)

    def mostrar_metricas_rapidas(self, parent, metricas):
        """Mostra métricas rápidas da turma"""
        metricas_frame = ctk.CTkFrame(parent)
        metricas_frame.pack(fill="x", pady=10, padx=10)

        # Métricas em grid
        grid_frame = ctk.CTkFrame(metricas_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=20, pady=10)

        # Total de Alunos
        ctk.CTkLabel(grid_frame, text="👥 Total de Alunos", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=20, pady=5)
        ctk.CTkLabel(grid_frame, text=f"{metricas['total_alunos']}", 
                    font=("Arial", 16, "bold"), text_color="#3498DB").grid(row=1, column=0, padx=20)

        # Média Geral
        ctk.CTkLabel(grid_frame, text="📈 Média Geral", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=20, pady=5)
        ctk.CTkLabel(grid_frame, text=f"{metricas['media_geral']:.1f}", 
                    font=("Arial", 16, "bold"), text_color="#2ECC71").grid(row=1, column=1, padx=20)

        # Taxa de Aprovação
        ctk.CTkLabel(grid_frame, text="✅ Taxa de Aprovação", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=20, pady=5)
        ctk.CTkLabel(grid_frame, text=f"{metricas['taxa_aprovacao']:.1f}%", 
                    font=("Arial", 16, "bold"), text_color="#27AE60").grid(row=1, column=2, padx=20)

        # Alunos em Risco
        ctk.CTkLabel(grid_frame, text="⚠️ Alunos em Risco", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=20, pady=5)
        ctk.CTkLabel(grid_frame, text=f"{len(metricas['alunos_risco'])}", 
                    font=("Arial", 16, "bold"), text_color="#E74C3C").grid(row=1, column=3, padx=20)

        # Mostrar alunos em risco se houver
        if metricas['alunos_risco']:
            risco_frame = ctk.CTkFrame(parent)
            risco_frame.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(risco_frame, text="🎯 Alunos que Precisam de Atenção:", 
                        font=("Arial", 12, "bold"), text_color="#E74C3C").pack(anchor="w", pady=5)
            
            for aluno in metricas['alunos_risco']:
                aluno_text = f"• {aluno['nome']} - Média: {aluno['media']:.1f}"
                ctk.CTkLabel(risco_frame, text=aluno_text, font=("Arial", 11)).pack(anchor="w")

    def mostrar_graficos_dashboard(self, parent):
        """Gera e exibe os gráficos no dashboard"""
        try:
            # Gráfico 1: Evolução da Turma
            evolucao_img = self.dashboard_manager.gerar_grafico_evolucao_turma(
                self.usuario_logado['disciplina'], 
                self.usuario_logado['ra']
            )
            
            if evolucao_img:
                frame_evolucao = ctk.CTkFrame(parent)
                frame_evolucao.pack(fill="x", pady=10, padx=10)
                
                ctk.CTkLabel(frame_evolucao, text="📈 Evolução da Turma por Bimestre", 
                            font=("Arial", 14, "bold")).pack(pady=5)
                
                evolucao_tk = ctk.CTkImage(light_image=evolucao_img, dark_image=evolucao_img, size=(600, 400))
                evolucao_label = ctk.CTkLabel(frame_evolucao, image=evolucao_tk, text="")
                evolucao_label.pack(pady=10)

            # Gráfico 2: Desempenho Individual
            desempenho_img = self.dashboard_manager.gerar_grafico_desempenho_individual(
                self.usuario_logado['disciplina'], 
                self.usuario_logado['ra']
            )
            
            if desempenho_img:
                frame_desempenho = ctk.CTkFrame(parent)
                frame_desempenho.pack(fill="x", pady=10, padx=10)
                
                ctk.CTkLabel(frame_desempenho, text="🎓 Top 10 Alunos - Desempenho Individual", 
                            font=("Arial", 14, "bold")).pack(pady=5)
                
                desempenho_tk = ctk.CTkImage(light_image=desempenho_img, dark_image=desempenho_img, size=(700, 400))
                desempenho_label = ctk.CTkLabel(frame_desempenho, image=desempenho_tk, text="")
                desempenho_label.pack(pady=10)

            # Gráfico 3: Distribuição de Notas
            distribuicao_img = self.dashboard_manager.gerar_grafico_distribuicao_notas(
                self.usuario_logado['disciplina'], 
                self.usuario_logado['ra']
            )
            
            if distribuicao_img:
                frame_distribuicao = ctk.CTkFrame(parent)
                frame_distribuicao.pack(fill="x", pady=10, padx=10)
                
                ctk.CTkLabel(frame_distribuicao, text="📊 Distribuição de Notas da Turma", 
                            font=("Arial", 14, "bold")).pack(pady=5)
                
                distribuicao_tk = ctk.CTkImage(light_image=distribuicao_img, dark_image=distribuicao_img, size=(600, 400))
                distribuicao_label = ctk.CTkLabel(frame_distribuicao, image=distribuicao_tk, text="")
                distribuicao_label.pack(pady=10)

        except Exception as e:
            error_label = ctk.CTkLabel(parent, text=f"Erro ao gerar gráficos: {e}", text_color="red")
            error_label.pack(pady=20)

    # ===============================
    # SISTEMA DE LANÇAMENTO DE NOTAS (mantido)
    # ===============================

    def mostrar_lancar_notas(self, parent):
        """Interface para professor lançar notas e faltas"""
        # Frame principal
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text=f"📝 Lançar Notas - {self.usuario_logado['disciplina']}",
            font=("Arial bold", 18)
        )
        title.pack(pady=10)

        # Frame de pesquisa
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(search_frame, text="🔍 Pesquisar Aluno:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Digite RA, nome ou sobrenome...",
            width=300
        )
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filtrar_alunos_lancamento)

        # Frame da lista de alunos
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # Lista de alunos com scroll
        self.scroll_frame = ctk.CTkScrollableFrame(list_frame, height=200)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame de informações
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=10, padx=10)

        info_text = ctk.CTkLabel(
            info_frame,
            text="💡 Selecione um aluno da lista para lançar notas e faltas",
            font=("Arial", 11),
            text_color="gray"
        )
        info_text.pack()

        # Carregar lista de alunos
        self.carregar_alunos_lancamento()

    def carregar_alunos_lancamento(self):
        """Carrega a lista de alunos para lançamento de notas"""
        self.lista_alunos_completa = []
        
        # Filtrar apenas alunos
        alunos_df = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
        
        for _, aluno in alunos_df.iterrows():
            self.lista_alunos_completa.append({
                'ra': aluno['RA'],
                'nome': aluno['Nome'],
                'sobrenome': aluno['Sobrenome']
            })
        
        # Ordenar por RA
        self.lista_alunos_completa.sort(key=lambda x: x['ra'])
        self.mostrar_alunos_lancamento(self.lista_alunos_completa)

    def filtrar_alunos_lancamento(self, event=None):
        """Filtra alunos baseado no texto da pesquisa"""
        texto_pesquisa = self.search_entry.get().strip().upper()
        
        if not texto_pesquisa:
            self.mostrar_alunos_lancamento(self.lista_alunos_completa)
            return
        
        alunos_filtrados = []
        for aluno in self.lista_alunos_completa:
            # Buscar por RA
            if texto_pesquisa in aluno['ra']:
                alunos_filtrados.append(aluno)
            # Buscar por nome
            elif texto_pesquisa in aluno['nome'].upper():
                alunos_filtrados.append(aluno)
            # Buscar por sobrenome
            elif texto_pesquisa in aluno['sobrenome'].upper():
                alunos_filtrados.append(aluno)
        
        self.mostrar_alunos_lancamento(alunos_filtrados)

    def mostrar_alunos_lancamento(self, alunos):
        """Mostra a lista de alunos no frame"""
        # Limpar frame atual
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not alunos:
            label_vazio = ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhum aluno encontrado com o filtro aplicado.",
                text_color="gray"
            )
            label_vazio.pack(pady=20)
            return
        
        # Criar botões para cada aluno
        for aluno in alunos:
            frame_aluno = ctk.CTkFrame(self.scroll_frame)
            frame_aluno.pack(fill="x", pady=2, padx=5)
            
            texto_aluno = f"{aluno['ra']} - {aluno['nome']} {aluno['sobrenome']}"
            
            btn_aluno = ctk.CTkButton(
                frame_aluno,
                text=texto_aluno,
                command=lambda ra=aluno['ra']: self.abrir_lancamento_aluno(ra),
                fg_color="transparent",
                hover_color="#2B2B2B" if ctk.get_appearance_mode() == "Dark" else "#F0F0F0",
                # CORREÇÃO 1: Text color adaptativo + alinhamento à esquerda
                text_color=("black", "white"),  # (light theme, dark theme)
                anchor="w"  # Alinhamento à esquerda
            )
            btn_aluno.pack(fill="x", padx=5, pady=2)

    def abrir_lancamento_aluno(self, ra_aluno):
        """Abre janela para lançar notas do aluno selecionado"""
        # Obter informações do aluno
        aluno_info = None
        for aluno in self.lista_alunos_completa:
            if aluno['ra'] == ra_aluno:
                aluno_info = aluno
                break
        
        if not aluno_info:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return
        
        # Criar janela de lançamento
        lancamento_window = ctk.CTkToplevel(self)
        lancamento_window.title(f"Lançar Notas - {ra_aluno}")
        lancamento_window.geometry("400x500")
        lancamento_window.transient(self)
        lancamento_window.grab_set()

        frame_lancamento = ctk.CTkFrame(lancamento_window)
        frame_lancamento.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Informações do aluno
        info_aluno = ctk.CTkLabel(
            frame_lancamento,
            text=f"Aluno: {aluno_info['ra']}\n{aluno_info['nome']} {aluno_info['sobrenome']}",
            font=("Arial", 14, "bold"),
            justify="center"
        )
        info_aluno.pack(pady=10)

        disciplina_label = ctk.CTkLabel(
            frame_lancamento,
            text=f"Disciplina: {self.usuario_logado['disciplina']}",
            font=("Arial", 12),
            text_color="blue"
        )
        disciplina_label.pack(pady=5)

        # Informação sobre limite de faltas
        info_faltas = ctk.CTkLabel(
            frame_lancamento,
            text="💡 Limite: máximo 35 faltas por bimestre (70% de 50 aulas)",
            font=("Arial", 10),
            text_color="orange"
        )
        info_faltas.pack(pady=5)

        # Frame para bimestres
        frame_bimestres = ctk.CTkFrame(frame_lancamento)
        frame_bimestres.pack(fill="both", expand=True, pady=10)

        # Variáveis para notas e faltas
        self.notas_entries = []
        self.faltas_entries = []
        
        # Criar campos para cada bimestre
        for bimestre in range(1, 5):
            frame_bim = ctk.CTkFrame(frame_bimestres)
            frame_bim.pack(fill="x", pady=5)
            
            label_bim = ctk.CTkLabel(frame_bim, text=f"Bimestre {bimestre}:", font=("Arial", 12))
            label_bim.pack(side="left", padx=5)
            
            # Campo de nota
            entry_nota = ctk.CTkEntry(
                frame_bim,
                placeholder_text="Nota (0-10)",
                width=80
            )
            entry_nota.pack(side="left", padx=5)
            self.notas_entries.append(entry_nota)
            
            label_sep = ctk.CTkLabel(frame_bim, text="|")
            label_sep.pack(side="left", padx=5)
            
            # Campo de faltas
            entry_faltas = ctk.CTkEntry(
                frame_bim,
                placeholder_text="Faltas (0-35)",
                width=80
            )
            entry_faltas.pack(side="left", padx=5)
            self.faltas_entries.append(entry_faltas)
        
        # Botões
        frame_botoes = ctk.CTkFrame(frame_lancamento)
        frame_botoes.pack(fill="x", pady=10)
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="💾 Salvar Notas",
            command=lambda: self.salvar_notas_aluno(ra_aluno, lancamento_window),
            fg_color="#27AE60",
            hover_color="#219955"
        )
        btn_salvar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="❌ Cancelar",
            command=lancamento_window.destroy,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        btn_cancelar.pack(side="left", padx=5)

    def salvar_notas_aluno(self, ra_aluno, window):
        """Salva as notas e faltas do aluno"""
        try:
            # Validar dados
            notas = []
            faltas = []
            
            # NOVO: Definir total de aulas por bimestre (valor fixo)
            TOTAL_AULAS_BIMESTRE = 50
            LIMITE_FALTAS = TOTAL_AULAS_BIMESTRE * 0.7  # 70% do total
            
            for i, (entry_nota, entry_faltas) in enumerate(zip(self.notas_entries, self.faltas_entries)):
                nota_text = entry_nota.get().strip()
                faltas_text = entry_faltas.get().strip()
                
                # Se ambos vazios, pular
                if not nota_text and not faltas_text:
                    notas.append(None)
                    faltas.append(None)
                    continue
                
                # Validar nota
                if nota_text:
                    nota = float(nota_text)
                    if nota < 0 or nota > 10:
                        messagebox.showerror("Erro", f"Nota do bimestre {i+1} deve ser entre 0 e 10!")
                        return
                    notas.append(nota)
                else:
                    notas.append(None)
                
                # Validar faltas - COM NOVA VALIDAÇÃO DE 70%
                if faltas_text:
                    falta = int(faltas_text)
                    if falta < 0:
                        messagebox.showerror("Erro", f"Faltas do bimestre {i+1} não podem ser negativas!")
                        return
                    
                    # NOVA VALIDAÇÃO: Verificar se faltas não ultrapassam 70% do total de aulas
                    if falta > LIMITE_FALTAS:
                        messagebox.showerror(
                            "Erro", 
                            f"🚫 Faltas do bimestre {i+1} não podem ultrapassar 70% do total de aulas!\n\n"
                            f"• Total de aulas no bimestre: {TOTAL_AULAS_BIMESTRE}\n"
                            f"• Limite máximo de faltas: {LIMITE_FALTAS:.0f}\n"
                            f"• Faltas informadas: {falta}"
                        )
                        return
                    faltas.append(falta)
                else:
                    faltas.append(None)
            
            # Salvar no CSV
            self.salvar_notas_csv(ra_aluno, self.usuario_logado['disciplina'], notas, faltas)
            
            messagebox.showinfo("Sucesso", "Notas e faltas salvas com sucesso!")
            window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar notas: {e}")

    def salvar_notas_csv(self, ra_aluno, disciplina, notas, faltas):
        """Salva as notas no arquivo CSV"""
        try:
            # Carregar dados existentes
            if not self.df_notas.empty:
                df = self.df_notas.copy()
            else:
                # Criar DataFrame vazio
                colunas = ['RA_Aluno', 'RA_Professor', 'Disciplina']
                for i in range(1, 5):
                    colunas.extend([f'Nota_Bimestre_{i}', f'Faltas_Bimestre_{i}'])
                df = pd.DataFrame(columns=colunas)
            
            # Verificar se já existe registro para este aluno/professor/disciplina
            mascara = (df['RA_Aluno'] == ra_aluno) & (df['RA_Professor'] == self.usuario_logado['ra']) & (df['Disciplina'] == disciplina)
            
            if mascara.any():
                # Atualizar registro existente
                idx = df[mascara].index[0]
                for i in range(4):
                    if notas[i] is not None:
                        df.at[idx, f'Nota_Bimestre_{i+1}'] = notas[i]
                    if faltas[i] is not None:
                        df.at[idx, f'Faltas_Bimestre_{i+1}'] = faltas[i]
            else:
                # Criar novo registro
                novo_registro = {
                    'RA_Aluno': ra_aluno,
                    'RA_Professor': self.usuario_logado['ra'],
                    'Disciplina': disciplina
                }
                
                for i in range(4):
                    novo_registro[f'Nota_Bimestre_{i+1}'] = notas[i] if notas[i] is not None else 0.0
                    novo_registro[f'Faltas_Bimestre_{i+1}'] = faltas[i] if faltas[i] is not None else 0
                
                df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
            
            # Salvar CSV
            df.to_csv('dados_notas.csv', index=False)
            self.df_notas = df  # Atualizar DataFrame em memória
            print(f"✅ Notas salvas para {ra_aluno} em {disciplina}")
            
        except Exception as e:
            raise Exception(f"Erro ao salvar CSV: {e}")

    # ===============================
    # FUNÇÕES ORIGINAIS (COM CORREÇÕES)
    # ===============================

    def mostrar_alunos_professor(self, parent):
        """Mostra alunos para o professor - CORREÇÃO 2: Adicionado campo de pesquisa"""
        # Frame de pesquisa
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(search_frame, text="🔍 Pesquisar:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.search_consultar_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Digite RA, nome ou sobrenome...",
            width=300
        )
        self.search_consultar_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.search_consultar_entry.bind("<KeyRelease>", self.filtrar_alunos_consulta)
        
        # Frame principal com scroll
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.scroll_consultar_frame = ctk.CTkScrollableFrame(main_frame)
        self.scroll_consultar_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Carregar lista inicial
        self.carregar_alunos_consulta()

    def carregar_alunos_consulta(self):
        """Carrega a lista completa de alunos para consulta"""
        self.lista_consulta_completa = []
        
        alunos_df = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
        
        for _, aluno in alunos_df.iterrows():
            self.lista_consulta_completa.append({
                'ra': aluno['RA'],
                'nome': aluno['Nome'],
                'sobrenome': aluno['Sobrenome']
            })
        
        # Ordenar por RA
        self.lista_consulta_completa.sort(key=lambda x: x['ra'])
        self.mostrar_alunos_consulta(self.lista_consulta_completa)

    def filtrar_alunos_consulta(self, event=None):
        """Filtra alunos na consulta baseado no texto da pesquisa"""
        texto_pesquisa = self.search_consultar_entry.get().strip().upper()
        
        if not texto_pesquisa:
            self.mostrar_alunos_consulta(self.lista_consulta_completa)
            return
        
        alunos_filtrados = []
        for aluno in self.lista_consulta_completa:
            if (texto_pesquisa in aluno['ra'] or
                texto_pesquisa in aluno['nome'].upper() or
                texto_pesquisa in aluno['sobrenome'].upper()):
                alunos_filtrados.append(aluno)
        
        self.mostrar_alunos_consulta(alunos_filtrados)

    def mostrar_alunos_consulta(self, alunos):
        """Mostra a lista de alunos na consulta - NOVA FUNCIONALIDADE: Botões clicáveis"""
        # Limpar frame atual
        for widget in self.scroll_consultar_frame.winfo_children():
            widget.destroy()
        
        if not alunos:
            label_vazio = ctk.CTkLabel(
                self.scroll_consultar_frame,
                text="Nenhum aluno encontrado com o filtro aplicado.",
                text_color="gray"
            )
            label_vazio.pack(pady=20)
            return
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(self.scroll_consultar_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(header_frame, text="RA", font=("Arial bold", 12), width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Nome", font=("Arial bold", 12), width=200).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Sobrenome", font=("Arial bold", 12), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Ação", font=("Arial bold", 12), width=100).pack(side="left", padx=5)

        # Lista de alunos como botões clicáveis
        for aluno in alunos:
            aluno_frame = ctk.CTkFrame(self.scroll_consultar_frame)
            aluno_frame.pack(fill="x", pady=2)
            
            # Informações do aluno
            ctk.CTkLabel(aluno_frame, text=aluno['ra'], width=100).pack(side="left", padx=5)
            ctk.CTkLabel(aluno_frame, text=aluno['nome'], width=200).pack(side="left", padx=5)
            ctk.CTkLabel(aluno_frame, text=aluno['sobrenome'], width=150).pack(side="left", padx=5)
            
            # Botão para ver detalhes
            btn_detalhes = ctk.CTkButton(
                aluno_frame,
                text="📊 Ver Detalhes",
                command=lambda ra=aluno['ra']: self.abrir_detalhes_aluno(ra),
                width=100,
                height=25,
                font=("Arial", 10)
            )
            btn_detalhes.pack(side="left", padx=5)

        # Informação do total
        total_frame = ctk.CTkFrame(self.scroll_consultar_frame, fg_color="transparent")
        total_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(total_frame, text=f"Total de alunos: {len(alunos)}", font=("Arial", 12)).pack()

    def abrir_detalhes_aluno(self, ra_aluno):
        """NOVA FUNCIONALIDADE: Abre janela com detalhes completos do aluno"""
        # Buscar informações do aluno
        aluno_info = None
        for aluno in self.lista_consulta_completa:
            if aluno['ra'] == ra_aluno:
                aluno_info = aluno
                break
        
        if not aluno_info:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return
        
        # Buscar notas do aluno em todas as disciplinas
        notas_aluno = self.df_notas[self.df_notas['RA_Aluno'] == ra_aluno]
        
        # Criar janela de detalhes
        detalhes_window = ctk.CTkToplevel(self)
        detalhes_window.title(f"Detalhes do Aluno - {ra_aluno}")
        detalhes_window.geometry("600x500")
        detalhes_window.transient(self)
        detalhes_window.grab_set()

        frame_detalhes = ctk.CTkFrame(detalhes_window)
        frame_detalhes.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Informações do aluno
        info_aluno = ctk.CTkLabel(
            frame_detalhes,
            text=f"👤 {aluno_info['nome']} {aluno_info['sobrenome']}\n📋 RA: {aluno_info['ra']}",
            font=("Arial", 16, "bold"),
            justify="center"
        )
        info_aluno.pack(pady=10)

        # Frame com scroll para disciplinas
        scroll_frame = ctk.CTkScrollableFrame(frame_detalhes)
        scroll_frame.pack(fill="both", expand=True, pady=10)

        if notas_aluno.empty:
            # Sem notas registradas
            sem_dados_label = ctk.CTkLabel(
                scroll_frame,
                text="📝 Nenhuma nota registrada para este aluno.",
                font=("Arial", 14),
                text_color="gray"
            )
            sem_dados_label.pack(pady=20)
        else:
            # Mostrar dados de cada disciplina
            for idx, disciplina in notas_aluno.iterrows():
                disc_frame = ctk.CTkFrame(scroll_frame)
                disc_frame.pack(fill="x", padx=5, pady=5)

                # Título da disciplina
                title = ctk.CTkLabel(
                    disc_frame, 
                    text=f"📚 {disciplina['Disciplina']}",
                    font=("Arial bold", 14)
                )
                title.pack(anchor="w", pady=(10, 5))

                # Cabeçalho da tabela
                header_frame = ctk.CTkFrame(disc_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10)
                
                ctk.CTkLabel(header_frame, text="Bimestre", font=("Arial bold", 11), width=100).pack(side="left")
                ctk.CTkLabel(header_frame, text="Nota", font=("Arial bold", 11), width=80).pack(side="left")
                ctk.CTkLabel(header_frame, text="Faltas", font=("Arial bold", 11), width=80).pack(side="left")

                # Dados dos bimestres
                notas = []
                faltas_totais = 0
                
                for i in range(4):
                    bim_frame = ctk.CTkFrame(disc_frame, fg_color="transparent")
                    bim_frame.pack(fill="x", padx=10)
                    
                    nota_col = f'Nota_Bimestre_{i+1}'
                    faltas_col = f'Faltas_Bimestre_{i+1}'
                    
                    nota = disciplina[nota_col] if nota_col in disciplina and pd.notna(disciplina[nota_col]) else 0
                    faltas = disciplina[faltas_col] if faltas_col in disciplina and pd.notna(disciplina[faltas_col]) else 0
                    
                    # Considerar apenas notas válidas para cálculo
                    if nota > 0:
                        notas.append(nota)
                    faltas_totais += faltas
                    
                    nota_text = f"{nota:.1f}" if nota > 0 else "--"
                    faltas_text = f"{faltas}" if faltas > 0 else "--"
                    
                    ctk.CTkLabel(bim_frame, text=f"{i+1}°", width=100).pack(side="left")
                    ctk.CTkLabel(bim_frame, text=nota_text, width=80).pack(side="left")
                    ctk.CTkLabel(bim_frame, text=faltas_text, width=80).pack(side="left")

                # Resumo da disciplina
                if notas:
                    media = sum(notas) / len(notas)
                    status = "✅ APROVADO" if media >= 6.0 else "❌ REPROVADO"
                    cor_status = "green" if media >= 6.0 else "red"
                    
                    resumo_frame = ctk.CTkFrame(disc_frame)
                    resumo_frame.pack(fill="x", padx=10, pady=5)
                    
                    resumo_text = f"📈 Média: {media:.1f} | 📅 Faltas: {faltas_totais} | {status}"
                    resumo_label = ctk.CTkLabel(
                        resumo_frame, 
                        text=resumo_text, 
                        font=("Arial bold", 12),
                        text_color=cor_status
                    )
                    resumo_label.pack(pady=5)
                else:
                    # Disciplina sem notas lançadas
                    resumo_frame = ctk.CTkFrame(disc_frame)
                    resumo_frame.pack(fill="x", padx=10, pady=5)
                    
                    resumo_label = ctk.CTkLabel(
                        resumo_frame, 
                        text="⏳ Aguardando lançamento de notas", 
                        font=("Arial", 11),
                        text_color="orange"
                    )
                    resumo_label.pack(pady=5)

        # Botão fechar
        btn_fechar = ctk.CTkButton(
            frame_detalhes,
            text="Fechar",
            command=detalhes_window.destroy,
            fg_color="#3498DB"
        )
        btn_fechar.pack(pady=10)

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