import customtkinter as ctk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
from PIL import Image
import numpy as np

# Configuração de tema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# ===============================
# CLASSE FAQWindow (MANTIDA)
# ===============================
class FAQWindow(ctk.CTkToplevel):
    """Janela de FAQ com abas para cada tipo de usuário"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("📚 FAQ - Perguntas Frequentes")
        self.geometry("600x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.center_window()
        self.setup_ui()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_frame,
            text="📚 Guia de Acesso - SiGA 2.0",
            font=("Arial bold", 20),
            text_color="#3498DB"
        )
        title.pack(pady=(0, 10))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="Informações de login para cada tipo de usuário",
            font=("Arial", 12),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 20))
        
        tabview = ctk.CTkTabview(main_frame)
        tabview.pack(fill="both", expand=True, padx=10)
        
        tabview.add("👨‍🎓 Aluno")
        self.setup_aba_aluno(tabview.tab("👨‍🎓 Aluno"))
        
        tabview.add("👨‍🏫 Professor")
        self.setup_aba_professor(tabview.tab("👨‍🏫 Professor"))
        
        tabview.add("👨‍💼 Admin")
        self.setup_aba_admin(tabview.tab("👨‍💼 Admin"))
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        btn_fechar = ctk.CTkButton(
            btn_frame,
            text="Fechar",
            command=self.destroy,
            width=120,
            fg_color="#3498DB",
            hover_color="#2980B9"
        )
        btn_fechar.pack()
    
    def setup_aba_aluno(self, parent):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        login_frame = ctk.CTkFrame(content_frame)
        login_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            login_frame,
            text="🔑 INFORMAÇÕES DE LOGIN",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        login_info = """RA: ALUN## (ex: ALUN01, ALUN15)
Senha: Seu sobrenome (minúsculas)

Exemplo:
RA: ALUN03
Senha: silva"""
        
        ctk.CTkLabel(
            login_frame,
            text=login_info,
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))
        
        func_frame = ctk.CTkFrame(content_frame)
        func_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            func_frame,
            text="🎯 FUNCIONALIDADES DISPONÍVEIS",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        func_list = """✅ Consultar notas e faltas
✅ Ver médias por disciplina
✅ Verificar situação acadêmica
✅ Visualizar dados pessoais"""
        
        ctk.CTkLabel(
            func_frame,
            text=func_list,
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))
    
    def setup_aba_professor(self, parent):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        login_frame = ctk.CTkFrame(content_frame)
        login_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            login_frame,
            text="🔑 INFORMAÇÕES DE LOGIN",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        login_info = """RA: PROF## (ex: PROF01, PROF05)
Senha: Seu sobrenome (minúsculas)

Exemplo:
RA: PROF02
Senha: santos"""
        
        ctk.CTkLabel(
            login_frame,
            text=login_info,
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))
        
        func_frame = ctk.CTkFrame(content_frame)
        func_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            func_frame,
            text="🎯 FUNCIONALIDADES DISPONÍVEIS",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        func_list = """✅ Lançar notas e faltas
✅ Consultar todos os alunos
✅ Cadastrar novos alunos
✅ Dashboard com gráficos
✅ Ver detalhes dos alunos"""
        
        ctk.CTkLabel(
            func_frame,
            text=func_list,
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))
    
    def setup_aba_admin(self, parent):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        login_frame = ctk.CTkFrame(content_frame)
        login_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            login_frame,
            text="🔑 INFORMAÇÕES DE LOGIN",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        login_info = """RA: ADM### (ex: ADM001, ADM010)
Senha: Seu sobrenome (minúsculas)

Exemplo:
RA: ADM001
Senha: admin"""
        
        ctk.CTkLabel(
            login_frame,
            text=login_info,
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))
        
        func_frame = ctk.CTkFrame(content_frame)
        func_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            func_frame,
            text="🎯 FUNCIONALIDADES DISPONÍVEIS",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(anchor="w", pady=(10, 5))
        
        func_list = """✅ Visualizar estatísticas gerais
✅ Ver todos os usuários
✅ Gerenciar o sistema completo
✅ Acessar todos os registros"""
        
        ctk.CTkLabel(
            func_frame,
            text=func_list,
            font=("Arial", 11),
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))

# ===============================
# CLASSE DashboardManager (MANTIDA)
# ===============================
class DashboardManager:
    def __init__(self, df_usuarios, df_notas):
        self.df_usuarios = df_usuarios
        self.df_notas = df_notas
        self.setup_estilo_graficos()
    
    def setup_estilo_graficos(self):
        plt.style.use('default')
        self.cores = ['#3498DB', '#2ECC71', '#E74C3C', '#F39C12', '#9B59B6']
    
    def gerar_grafico_evolucao_turma(self, disciplina, professor_ra):
        try:
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return None
            
            medias_bimestres = []
            for bimestre in range(1, 5):
                coluna_nota = f'Nota_Bimestre_{bimestre}'
                notas_bimestre = notas_disciplina[coluna_nota].replace(0, np.nan).dropna()
                if not notas_bimestre.empty:
                    media = notas_bimestre.mean()
                    medias_bimestres.append(media)
                else:
                    medias_bimestres.append(0)
            
            fig, ax = plt.subplots(figsize=(8, 4))
            bimestres = ['1° Bi', '2° Bi', '3° Bi', '4° Bi']
            
            bars = ax.bar(bimestres, medias_bimestres, color=self.cores, alpha=0.8)
            ax.set_ylabel('Média das Notas', fontsize=10, fontweight='bold')
            ax.set_xlabel('Bimestres', fontsize=10, fontweight='bold')
            ax.set_title(f'Evolução da Turma - {disciplina}', fontsize=12, fontweight='bold', pad=15)
            
            for bar, valor in zip(bars, medias_bimestres):
                if valor > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                           f'{valor:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
            
            ax.set_ylim(0, 10)
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            return self.fig_para_imagem(fig)
            
        except Exception as e:
            print(f"Erro ao gerar gráfico de evolução: {e}")
            return None
    
    def gerar_grafico_desempenho_individual(self, disciplina, professor_ra):
        try:
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return None
            
            alunos_medias = []
            for _, row in notas_disciplina.iterrows():
                ra_aluno = row['RA_Aluno']
                notas = [row[f'Nota_Bimestre_{i}'] for i in range(1, 5)]
                notas_validas = [n for n in notas if n > 0]
                
                if notas_validas:
                    media = sum(notas_validas) / len(notas_validas)
                    aluno_info = self.df_usuarios[self.df_usuarios['RA'] == ra_aluno]
                    nome_aluno = aluno_info['Nome'].iloc[0] if not aluno_info.empty else ra_aluno
                    
                    alunos_medias.append({
                        'ra': ra_aluno,
                        'nome': nome_aluno,
                        'media': media,
                        'situacao': 'Aprovado' if media >= 6.0 else 'Reprovado'
                    })
            
            alunos_medias.sort(key=lambda x: x['media'], reverse=True)
            alunos_top = alunos_medias[:10]
            
            if not alunos_top:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 4))
            nomes = [f"{aluno['nome'][:12]}..." if len(aluno['nome']) > 12 else aluno['nome'] 
                    for aluno in alunos_top]
            medias = [aluno['media'] for aluno in alunos_top]
            cores = ['#2ECC71' if aluno['situacao'] == 'Aprovado' else '#E74C3C' 
                    for aluno in alunos_top]
            
            bars = ax.bar(nomes, medias, color=cores, alpha=0.8)
            ax.set_ylabel('Média Final', fontsize=10, fontweight='bold')
            ax.set_xlabel('Alunos', fontsize=10, fontweight='bold')
            ax.set_title(f'Top 10 Alunos - {disciplina}', fontsize=12, fontweight='bold', pad=15)
            
            for bar, valor in zip(bars, medias):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       f'{valor:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
            
            ax.set_ylim(0, 10)
            plt.xticks(rotation=45, ha='right', fontsize=9)
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            
            return self.fig_para_imagem(fig)
            
        except Exception as e:
            print(f"Erro ao gerar gráfico individual: {e}")
            return None
    
    def gerar_grafico_distribuicao_notas(self, disciplina, professor_ra):
        try:
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return None
            
            todas_notas = []
            for _, row in notas_disciplina.iterrows():
                for i in range(1, 5):
                    nota = row[f'Nota_Bimestre_{i}']
                    if nota > 0:
                        todas_notas.append(nota)
            
            if not todas_notas:
                return None
            
            fig, ax = plt.subplots(figsize=(8, 4))
            n, bins, patches = ax.hist(todas_notas, bins=8, range=(0, 10),
                                      color='#3498DB', alpha=0.7, edgecolor='black')
            
            ax.set_xlabel('Notas', fontsize=10, fontweight='bold')
            ax.set_ylabel('Quantidade de Alunos', fontsize=10, fontweight='bold')
            ax.set_title(f'Distribuição de Notas - {disciplina}', fontsize=12, fontweight='bold', pad=15)
            
            media = np.mean(todas_notas)
            ax.axvline(media, color='#E74C3C', linestyle='--', linewidth=1.5, 
                      label=f'Média: {media:.2f}')
            
            ax.axvline(6.0, color='#2ECC71', linestyle='--', linewidth=1.5, 
                      label='Mínimo para Aprovação')
            
            ax.legend(fontsize=9)
            ax.grid(alpha=0.3)
            plt.tight_layout()
            
            return self.fig_para_imagem(fig)
            
        except Exception as e:
            print(f"Erro ao gerar distribuição: {e}")
            return None
    
    def calcular_metricas_turma(self, disciplina, professor_ra):
        try:
            notas_disciplina = self.df_notas[
                (self.df_notas['Disciplina'] == disciplina) & 
                (self.df_notas['RA_Professor'] == professor_ra)
            ]
            
            if notas_disciplina.empty:
                return {}
            
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
                'melhor_nota': max(medias_alunos) if medias_alunos else 0,
                'pior_nota': min(medias_alunos) if medias_alunos else 0
            }
            
        except Exception as e:
            print(f"Erro ao calcular métricas: {e}")
            return {}
    
    def fig_para_imagem(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=90, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        return Image.open(buf)

# ===============================
# CLASSE AdminUserManager (MANTIDA)
# ===============================
class AdminUserManager:
    """Gerenciador de usuários para administradores"""
    
    def __init__(self, df_usuarios):
        self.df_usuarios = df_usuarios
    
    def get_next_ra(self, tipo_usuario):
        """Gera próximo RA sequencial baseado no tipo"""
        if tipo_usuario == "professor":
            prefixo = "PROF"
            usuarios_tipo = self.df_usuarios[self.df_usuarios['RA'].str.startswith(prefixo)]
        elif tipo_usuario == "admin":
            prefixo = "ADM"
            usuarios_tipo = self.df_usuarios[self.df_usuarios['RA'].str.startswith(prefixo)]
        else:
            return None
        
        if usuarios_tipo.empty:
            return f"{prefixo}01" if tipo_usuario == "professor" else f"{prefixo}001"
        
        numeros = []
        for ra in usuarios_tipo['RA']:
            try:
                num = int(ra.replace(prefixo, ""))
                numeros.append(num)
            except:
                continue
        
        next_num = max(numeros) + 1 if numeros else 1
        
        if tipo_usuario == "professor":
            return f"{prefixo}{next_num:02d}"
        else:  # admin
            return f"{prefixo}{next_num:03d}"
    
    def cadastrar_professor(self, nome, sobrenome, disciplina):
        """Cadastra novo professor no sistema"""
        try:
            novo_ra = self.get_next_ra("professor")
            
            # Verificar se RA já existe (proteção extra)
            if novo_ra in self.df_usuarios['RA'].values:
                raise ValueError(f"RA {novo_ra} já existe no sistema")
            
            novo_professor = {
                'RA': novo_ra,
                'Nome': nome.strip(),
                'Sobrenome': sobrenome.strip(),
                'Tipo': 2,  # Tipo 2 = Professor
                'Disciplina': disciplina.strip(),
                'Ativo': 1  # Ativo por padrão
            }
            
            return novo_professor, f"Professor {nome} cadastrado com RA: {novo_ra}"
            
        except Exception as e:
            raise Exception(f"Erro ao cadastrar professor: {e}")
    
    def cadastrar_admin(self, nome, sobrenome):
        """Cadastra novo administrador no sistema"""
        try:
            novo_ra = self.get_next_ra("admin")
            
            # Verificar se RA já existe
            if novo_ra in self.df_usuarios['RA'].values:
                raise ValueError(f"RA {novo_ra} já existe no sistema")
            
            novo_admin = {
                'RA': novo_ra,
                'Nome': nome.strip(),
                'Sobrenome': sobrenome.strip(),
                'Tipo': 3,  # Tipo 3 = Admin
                'Disciplina': "N/A",  # Admin não tem disciplina
                'Ativo': 1  # Ativo por padrão
            }
            
            return novo_admin, f"Administrador {nome} cadastrado com RA: {novo_ra}"
            
        except Exception as e:
            raise Exception(f"Erro ao cadastrar administrador: {e}")
    
    def toggle_status_usuario(self, ra_usuario):
        """Alterna status ativo/inativo de um usuário"""
        try:
            if ra_usuario not in self.df_usuarios['RA'].values:
                raise ValueError(f"RA {ra_usuario} não encontrado")
            
            idx = self.df_usuarios[self.df_usuarios['RA'] == ra_usuario].index[0]
            status_atual = self.df_usuarios.at[idx, 'Ativo']
            novo_status = 0 if status_atual == 1 else 1
            
            # Não permitir desativar último admin ativo
            if self.df_usuarios.at[idx, 'Tipo'] == 3:  # Se for admin
                admins_ativos = self.df_usuarios[
                    (self.df_usuarios['Tipo'] == 3) & 
                    (self.df_usuarios['Ativo'] == 1)
                ]
                if len(admins_ativos) == 1 and novo_status == 0:
                    raise ValueError("Não é possível desativar o último administrador ativo")
            
            self.df_usuarios.at[idx, 'Ativo'] = novo_status
            
            tipo_usuario = self.df_usuarios.at[idx, 'Tipo']
            nome = self.df_usuarios.at[idx, 'Nome']
            
            status_text = "ativado" if novo_status == 1 else "desativado"
            tipo_text = {1: "aluno", 2: "professor", 3: "administrador"}[tipo_usuario]
            
            return f"{tipo_text.capitalize()} {nome} ({ra_usuario}) {status_text} com sucesso"
            
        except Exception as e:
            raise Exception(f"Erro ao alterar status: {e}")
    
    def buscar_usuario(self, filtro=""):
        """Busca usuários com filtro"""
        try:
            if not filtro:
                return self.df_usuarios.copy()
            
            filtro = filtro.strip().upper()
            
            # Buscar por RA, Nome ou Sobrenome
            mascara = (
                self.df_usuarios['RA'].str.contains(filtro, na=False) |
                self.df_usuarios['Nome'].str.upper().str.contains(filtro, na=False) |
                self.df_usuarios['Sobrenome'].str.upper().str.contains(filtro, na=False)
            )
            
            return self.df_usuarios[mascara].copy()
            
        except Exception as e:
            print(f"Erro na busca: {e}")
            return self.df_usuarios.copy()
    
    def get_estatisticas(self):
        """Retorna estatísticas dos usuários"""
        try:
            total_usuarios = len(self.df_usuarios)
            
            alunos = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
            professores = self.df_usuarios[self.df_usuarios['Tipo'] == 2]
            admins = self.df_usuarios[self.df_usuarios['Tipo'] == 3]
            
            alunos_ativos = alunos[alunos['Ativo'] == 1]
            professores_ativos = professores[professores['Ativo'] == 1]
            admins_ativos = admins[admins['Ativo'] == 1]
            
            return {
                'total': total_usuarios,
                'alunos': len(alunos),
                'alunos_ativos': len(alunos_ativos),
                'professores': len(professores),
                'professores_ativos': len(professores_ativos),
                'admins': len(admins),
                'admins_ativos': len(admins_ativos)
            }
            
        except Exception as e:
            print(f"Erro ao calcular estatísticas: {e}")
            return {}

# ===============================
# CLASSE PRINCIPAL App (ATUALIZADA)
# ===============================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão Acadêmica (SiGA)")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Configurar responsividade
        self.responsive_state = "normal"
        self.bind("<Configure>", self.on_resize)
        
        # Carregar dados
        self.carregar_dados()
        
        # Inicializar Dashboard Manager
        self.dashboard_manager = DashboardManager(self.df_usuarios, self.df_notas)
        
        # Variáveis do sistema
        self.usuario_logado = None
        self.current_frame = None
        
        # Exibir login
        self.show_login_frame()

    def on_resize(self, event):
        if event.widget == self:
            self.after(200, self.check_window_size)

    def check_window_size(self):
        width = self.winfo_width()
        
        if width < 700:
            new_state = "mobile"
        elif width < 1000:
            new_state = "compact"
        else:
            new_state = "normal"
        
        if new_state != self.responsive_state:
            self.responsive_state = new_state
            # Aqui você pode adicionar lógica para atualizar a interface

    def carregar_dados(self):
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
        
        # Título
        title_size = 28 if self.responsive_state == "normal" else 24 if self.responsive_state == "compact" else 22
        title = ctk.CTkLabel(login_frame, text="Sistema de Gestão Acadêmica (SiGA)", 
                           font=("Arial bold", title_size))
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(login_frame, text="Login de Acesso", 
                              font=("Arial", 14), text_color="gray")
        subtitle.pack(pady=(0, 20))

        # Campos de entrada
        input_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        input_frame.pack(pady=20)

        ctk.CTkLabel(input_frame, text="RA:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.ra_entry = ctk.CTkEntry(input_frame, placeholder_text="Digite seu RA", width=250)
        self.ra_entry.grid(row=0, column=1, padx=10, pady=5)
        self.ra_entry.bind("<Return>", lambda event: self.login())

        ctk.CTkLabel(input_frame, text="Senha:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.senha_entry = ctk.CTkEntry(input_frame, placeholder_text="Senha", show="*", width=250)
        self.senha_entry.grid(row=1, column=1, padx=10, pady=5)
        self.senha_entry.bind("<Return>", lambda event: self.login())

        # Botões
        button_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        login_button = ctk.CTkButton(button_frame, text="Entrar", command=self.login, width=120)
        login_button.pack(pady=10)

        # Botão FAQ
        help_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        help_frame.pack(side="bottom", anchor="se", padx=20, pady=20)
        
        faq_button = ctk.CTkButton(
            help_frame,
            text="📚 FAQ / Ajuda",
            command=self.abrir_faq,
            width=120,
            height=35,
            fg_color="transparent",
            border_width=1,
            border_color="#3498DB",
            text_color="#3498DB",
            hover_color="#EBF5FB"
        )
        faq_button.pack(side="right")
        
        help_label = ctk.CTkLabel(
            help_frame,
            text="Precisa de ajuda para acessar?",
            font=("Arial", 10),
            text_color="gray"
        )
        help_label.pack(side="right", padx=(0, 10))

        self.switch_frame(login_frame)

    def abrir_faq(self):
        if hasattr(self, 'faq_window') and self.faq_window.winfo_exists():
            self.faq_window.lift()
            self.faq_window.focus()
        else:
            self.faq_window = FAQWindow(self)

    def login(self):
        ra = self.ra_entry.get().strip().upper()
        senha = self.senha_entry.get().strip()

        if not ra or not senha:
            messagebox.showwarning("Login", "Por favor, preencha RA e senha!")
            return

        if self.df_usuarios.empty:
            messagebox.showerror("Erro", "Nenhum usuário cadastrado no sistema!")
            return

        usuario_encontrado = self.df_usuarios[self.df_usuarios['RA'] == ra]

        if usuario_encontrado.empty:
            messagebox.showerror("Login", "RA não encontrado!")
            return

        usuario = usuario_encontrado.iloc[0]
        sobrenome_correto = str(usuario['Sobrenome']).strip().lower()

        if senha.lower() != sobrenome_correto:
            messagebox.showerror("Login", "Senha incorreta!")
            return

        self.usuario_logado = {
            'ra': usuario['RA'],
            'nome': usuario['Nome'],
            'sobrenome': usuario['Sobrenome'],
            'tipo': usuario['Tipo'],
            'disciplina': usuario['Disciplina'] if 'Disciplina' in usuario and pd.notna(usuario['Disciplina']) else "N/A"
        }

        tipo_usuario = {1: "Aluno", 2: "Professor", 3: "Administrador"}[usuario['Tipo']]
        messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario['Nome']}!\nTipo: {tipo_usuario}")

        self.ra_entry.delete(0, 'end')
        self.senha_entry.delete(0, 'end')
        self.redirecionar_por_tipo()

    def redirecionar_por_tipo(self):
        tipo = self.usuario_logado['tipo']
        
        if tipo == 1:
            self.show_aluno_frame()
        elif tipo == 2:
            self.show_professor_frame()
        elif tipo == 3:
            self.show_admin_frame()

    def show_aluno_frame(self):
        aluno_frame = ctk.CTkFrame(self)
        
        header_frame = ctk.CTkFrame(aluno_frame, fg_color="transparent")
        header_frame.pack(pady=20)
        
        title = ctk.CTkLabel(header_frame, text=f"🎓 Área do Aluno", font=("Arial bold", 24))
        title.pack()
        
        user_info = ctk.CTkLabel(header_frame,
                                text=f"{self.usuario_logado['nome']} {self.usuario_logado['sobrenome']} - {self.usuario_logado['ra']}",
                                font=("Arial", 14), text_color="gray")
        user_info.pack(pady=5)

        tabview = ctk.CTkTabview(aluno_frame)
        tabview.pack(expand=True, fill="both", padx=20, pady=10)
        
        tabview.add("Notas e Faltas")
        tabview.add("Dados Pessoais")

        self.mostrar_notas_aluno(tabview.tab("Notas e Faltas"))
        
        dados_frame = tabview.tab("Dados Pessoais")
        info_text = f"""👤 DADOS PESSOAIS

📋 RA: {self.usuario_logado['ra']}
🧑‍🎓 Nome: {self.usuario_logado['nome']}
📛 Sobrenome: {self.usuario_logado['sobrenome']}
🎯 Tipo: Aluno

💡 Funcionalidades:
• Consultar notas e faltas
• Visualizar médias
• Verificar situação"""
        
        dados_label = ctk.CTkLabel(dados_frame, text=info_text, font=("Arial", 12), justify="left")
        dados_label.pack(pady=20)

        logout_button = ctk.CTkButton(aluno_frame, text="🚪 Sair", command=self.logout, fg_color="#E74C3C")
        logout_button.pack(pady=10)

        self.switch_frame(aluno_frame)

    def mostrar_notas_aluno(self, parent):
        if self.df_notas.empty:
            lbl_sem_dados = ctk.CTkLabel(parent, text="📝 Nenhuma nota registrada ainda.", font=("Arial", 14))
            lbl_sem_dados.pack(expand=True)
            return
        
        notas_aluno = self.df_notas[self.df_notas['RA_Aluno'] == self.usuario_logado['ra']]
        
        if notas_aluno.empty:
            lbl_sem_dados = ctk.CTkLabel(parent, text="📝 Nenhuma nota encontrada para seu RA.", font=("Arial", 14))
            lbl_sem_dados.pack(expand=True)
            return

        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        for idx, disciplina in notas_aluno.iterrows():
            disc_frame = ctk.CTkFrame(scroll_frame)
            disc_frame.pack(fill="x", padx=5, pady=5)

            title = ctk.CTkLabel(disc_frame, text=f"📚 {disciplina['Disciplina']}", font=("Arial bold", 14))
            title.pack(anchor="w", pady=(10, 5))

            header_frame = ctk.CTkFrame(disc_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=10)
            
            ctk.CTkLabel(header_frame, text="Bimestre", font=("Arial bold", 11), width=80).pack(side="left")
            ctk.CTkLabel(header_frame, text="Nota", font=("Arial bold", 11), width=60).pack(side="left")
            ctk.CTkLabel(header_frame, text="Faltas", font=("Arial bold", 11), width=60).pack(side="left")

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

            media = sum(notas) / len(notas) if notas else 0
            status = "✅ APROVADO" if media >= 6.0 else "❌ REPROVADO"
            cor_status = "green" if media >= 6.0 else "red"
            
            resumo_frame = ctk.CTkFrame(disc_frame)
            resumo_frame.pack(fill="x", padx=10, pady=5)
            
            resumo_text = f"📈 Média: {media:.1f} | 📅 Faltas: {faltas_totais} | {status}"
            resumo_label = ctk.CTkLabel(resumo_frame, text=resumo_text, font=("Arial bold", 12), text_color=cor_status)
            resumo_label.pack(pady=5)

    def show_professor_frame(self):
        professor_frame = ctk.CTkFrame(self)
        
        header_frame = ctk.CTkFrame(professor_frame, fg_color="transparent")
        header_frame.pack(pady=20)
        
        title = ctk.CTkLabel(header_frame, text=f"👨‍🏫 Área do Professor", font=("Arial bold", 24))
        title.pack()
        
        user_info = ctk.CTkLabel(header_frame,
                                text=f"{self.usuario_logado['nome']} {self.usuario_logado['sobrenome']} - {self.usuario_logado['disciplina']}",
                                font=("Arial", 14), text_color="gray")
        user_info.pack(pady=5)

        tabview = ctk.CTkTabview(professor_frame)
        tabview.pack(expand=True, fill="both", padx=20, pady=10)
        
        tabview.add("Lançar Notas")
        tabview.add("Consultar Alunos")
        tabview.add("Cadastrar Aluno")
        tabview.add("Dashboard")
        tabview.add("Estatísticas")

        self.mostrar_lancar_notas(tabview.tab("Lançar Notas"))
        self.mostrar_alunos_professor(tabview.tab("Consultar Alunos"))
        self.mostrar_cadastrar_aluno(tabview.tab("Cadastrar Aluno"))
        self.mostrar_dashboard_professor(tabview.tab("Dashboard"))
        self.mostrar_estatisticas_professor(tabview.tab("Estatísticas"))

        logout_button = ctk.CTkButton(professor_frame, text="🚪 Sair", command=self.logout, fg_color="#E74C3C")
        logout_button.pack(pady=10)

        self.switch_frame(professor_frame)

    # ===============================
    # DASHBOARD OTIMIZADO
    # ===============================

    def mostrar_dashboard_professor(self, parent):
        """Dashboard compacto e responsivo"""
        main_scroll = ctk.CTkScrollableFrame(parent)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        container = ctk.CTkFrame(main_scroll, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        # Título
        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 15))
        
        title_size = 18 if self.responsive_state == "normal" else 16
        title = ctk.CTkLabel(
            title_frame,
            text=f"📊 Dashboard - {self.usuario_logado['disciplina']}",
            font=("Arial bold", title_size),
            text_color="#3498DB"
        )
        title.pack()
        
        info_size = 12 if self.responsive_state == "normal" else 11
        professor_info = ctk.CTkLabel(
            title_frame,
            text=f"Professor: {self.usuario_logado['nome']} | RA: {self.usuario_logado['ra']}",
            font=("Arial", info_size),
            text_color="gray"
        )
        professor_info.pack(pady=5)
        
        # Métricas
        metricas = self.dashboard_manager.calcular_metricas_turma(
            self.usuario_logado['disciplina'], 
            self.usuario_logado['ra']
        )
        
        if metricas:
            self.mostrar_metricas_compactas(container, metricas)
        
        # Gráficos
        graficos_frame = ctk.CTkFrame(container, fg_color="transparent")
        graficos_frame.pack(fill="both", expand=True, pady=(15, 10))
        
        self.mostrar_graficos_compactos(graficos_frame)
        
        # Alunos em risco
        if metricas and metricas.get('alunos_risco'):
            self.mostrar_alunos_risco_colapsavel(container, metricas['alunos_risco'])

    def mostrar_metricas_compactas(self, parent, metricas):
        """Métricas em cards compactos"""
        metricas_frame = ctk.CTkFrame(parent, corner_radius=10)
        metricas_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            metricas_frame,
            text="📈 MÉTRICAS DA TURMA",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(pady=(10, 15))
        
        grid_frame = ctk.CTkFrame(metricas_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Card 1: Total de Alunos
        card1 = ctk.CTkFrame(grid_frame, height=70, corner_radius=8, 
                           fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card1, text="👥", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card1, text="TOTAL ALUNOS", font=("Arial bold", 9), text_color="gray").pack()
        ctk.CTkLabel(card1, text=f"{metricas['total_alunos']}", font=("Arial bold", 16), 
                    text_color="#3498DB").pack()
        
        # Card 2: Média Geral
        card2 = ctk.CTkFrame(grid_frame, height=70, corner_radius=8,
                           fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card2, text="📊", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card2, text="MÉDIA GERAL", font=("Arial bold", 9), text_color="gray").pack()
        ctk.CTkLabel(card2, text=f"{metricas['media_geral']:.1f}", font=("Arial bold", 16), 
                    text_color="#2ECC71").pack()
        
        # Card 3: Taxa de Aprovação
        card3 = ctk.CTkFrame(grid_frame, height=70, corner_radius=8,
                           fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card3, text="✅", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card3, text="APROVAÇÃO", font=("Arial bold", 9), text_color="gray").pack()
        ctk.CTkLabel(card3, text=f"{metricas['taxa_aprovacao']:.1f}%", font=("Arial bold", 16), 
                    text_color="#27AE60").pack()
        
        # Card 4: Alunos em Risco
        card4 = ctk.CTkFrame(grid_frame, height=70, corner_radius=8,
                           fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card4, text="⚠️", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card4, text="EM RISCO", font=("Arial bold", 9), text_color="gray").pack()
        ctk.CTkLabel(card4, text=f"{len(metricas['alunos_risco'])}", font=("Arial bold", 16), 
                    text_color="#E74C3C").pack()
        
        # Configurar grid
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

    def mostrar_graficos_compactos(self, parent):
        """Gráficos compactos"""
        try:
            # Ajustar tamanho
            if self.responsive_state == "normal":
                graph_width, graph_height = 500, 250
            elif self.responsive_state == "compact":
                graph_width, graph_height = 450, 225
            else:
                graph_width, graph_height = 400, 200
            
            # Gráfico 1: Evolução da Turma
            evolucao_img = self.dashboard_manager.gerar_grafico_evolucao_turma(
                self.usuario_logado['disciplina'], 
                self.usuario_logado['ra']
            )
            
            if evolucao_img:
                evolucao_img = evolucao_img.resize((graph_width, graph_height), Image.Resampling.LANCZOS)
                evolucao_tk = ctk.CTkImage(light_image=evolucao_img, dark_image=evolucao_img, 
                                          size=(graph_width, graph_height))
                
                frame_evolucao = ctk.CTkFrame(parent)
                frame_evolucao.pack(fill="x", pady=5, padx=10)
                
                ctk.CTkLabel(frame_evolucao, text="📈 Evolução da Turma", 
                            font=("Arial bold", 12)).pack(pady=5)
                
                ctk.CTkLabel(frame_evolucao, image=evolucao_tk, text="").pack(pady=5)

            # Gráfico 2: Distribuição de Notas
            distribuicao_img = self.dashboard_manager.gerar_grafico_distribuicao_notas(
                self.usuario_logado['disciplina'], 
                self.usuario_logado['ra']
            )
            
            if distribuicao_img:
                distribuicao_img = distribuicao_img.resize((graph_width, graph_height), Image.Resampling.LANCZOS)
                distribuicao_tk = ctk.CTkImage(light_image=distribuicao_img, dark_image=distribuicao_img, 
                                              size=(graph_width, graph_height))
                
                frame_distribuicao = ctk.CTkFrame(parent)
                frame_distribuicao.pack(fill="x", pady=5, padx=10)
                
                ctk.CTkLabel(frame_distribuicao, text="📊 Distribuição de Notas", 
                            font=("Arial bold", 12)).pack(pady=5)
                
                ctk.CTkLabel(frame_distribuicao, image=distribuicao_tk, text="").pack(pady=5)

        except Exception as e:
            error_label = ctk.CTkLabel(parent, text=f"Erro ao gerar gráficos: {str(e)[:50]}...", 
                                      text_color="red", font=("Arial", 10))
            error_label.pack(pady=10)

    def mostrar_alunos_risco_colapsavel(self, parent, alunos_risco):
        """Lista de alunos em risco colapsável"""
        risco_frame = ctk.CTkFrame(parent, corner_radius=8, 
                                  fg_color="#FFF3CD", border_width=1, border_color="#FFEEBA")
        risco_frame.pack(fill="x", pady=10, padx=10)
        
        header_frame = ctk.CTkFrame(risco_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=8)
        
        titulo = ctk.CTkLabel(
            header_frame,
            text=f"⚠️ ALUNOS QUE PRECISAM DE ATENÇÃO ({len(alunos_risco)})",
            font=("Arial bold", 12),
            text_color="#856404"
        )
        titulo.pack(side="left")
        
        self.toggle_risco_btn = ctk.CTkButton(
            header_frame,
            text="▼ Mostrar",
            command=lambda: self.toggle_lista_alunos_risco(risco_frame, alunos_risco),
            width=70,
            height=24,
            font=("Arial", 9),
            fg_color="transparent",
            hover_color="#FFEAA7",
            text_color="#856404",
            border_width=1,
            border_color="#856404"
        )
        self.toggle_risco_btn.pack(side="right")
        
        self.risco_content = ctk.CTkFrame(risco_frame)
        self.risco_content.pack_forget()

    def toggle_lista_alunos_risco(self, parent_frame, alunos_risco):
        """Alterna visibilidade da lista"""
        if self.risco_content.winfo_ismapped():
            self.risco_content.pack_forget()
            self.toggle_risco_btn.configure(text="▶ Mostrar")
        else:
            self.risco_content.pack(fill="x", padx=15, pady=(0, 10))
            self.toggle_risco_btn.configure(text="▼ Ocultar")
            
            for widget in self.risco_content.winfo_children():
                widget.destroy()
            
            for aluno in alunos_risco[:8]:
                aluno_frame = ctk.CTkFrame(self.risco_content, fg_color="transparent")
                aluno_frame.pack(fill="x", pady=2)
                
                nome = aluno['nome']
                if len(nome) > 20:
                    nome = nome[:17] + "..."
                
                ctk.CTkLabel(
                    aluno_frame,
                    text=f"• {nome}",
                    font=("Arial", 10),
                    anchor="w"
                ).pack(side="left", padx=(10, 0))
                
                ctk.CTkLabel(
                    aluno_frame,
                    text=f"Média: {aluno['media']:.1f}",
                    font=("Arial", 10, "bold"),
                    text_color="#E74C3C"
                ).pack(side="right", padx=(0, 10))
            
            if len(alunos_risco) > 8:
                ctk.CTkLabel(
                    self.risco_content,
                    text=f"... e mais {len(alunos_risco) - 8} aluno(s)",
                    font=("Arial", 9, "italic"),
                    text_color="gray"
                ).pack(pady=(5, 0))

    # ===============================
    # FUNÇÕES ORIGINAIS (SIMPLIFICADAS)
    # ===============================

    def mostrar_lancar_notas(self, parent):
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title = ctk.CTkLabel(
            main_frame,
            text=f"📝 Lançar Notas - {self.usuario_logado['disciplina']}",
            font=("Arial bold", 18)
        )
        title.pack(pady=10)

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

        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, pady=10, padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(list_frame, height=200)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=10, padx=10)

        info_text = ctk.CTkLabel(
            info_frame,
            text="💡 Selecione um aluno da lista para lançar notas e faltas",
            font=("Arial", 11),
            text_color="gray"
        )
        info_text.pack()

        self.carregar_alunos_lancamento()

    def carregar_alunos_lancamento(self):
        self.lista_alunos_completa = []
        
        alunos_df = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
        
        for _, aluno in alunos_df.iterrows():
            self.lista_alunos_completa.append({
                'ra': aluno['RA'],
                'nome': aluno['Nome'],
                'sobrenome': aluno['Sobrenome']
            })
        
        self.lista_alunos_completa.sort(key=lambda x: x['ra'])
        self.mostrar_alunos_lancamento(self.lista_alunos_completa)

    def filtrar_alunos_lancamento(self, event=None):
        texto_pesquisa = self.search_entry.get().strip().upper()
        
        if not texto_pesquisa:
            self.mostrar_alunos_lancamento(self.lista_alunos_completa)
            return
        
        alunos_filtrados = []
        for aluno in self.lista_alunos_completa:
            if (texto_pesquisa in aluno['ra'] or
                texto_pesquisa in aluno['nome'].upper() or
                texto_pesquisa in aluno['sobrenome'].upper()):
                alunos_filtrados.append(aluno)
        
        self.mostrar_alunos_lancamento(alunos_filtrados)

    def mostrar_alunos_lancamento(self, alunos):
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
                text_color=("black", "white"),
                anchor="w"
            )
            btn_aluno.pack(fill="x", padx=5, pady=2)

    def abrir_lancamento_aluno(self, ra_aluno):
        aluno_info = None
        for aluno in self.lista_alunos_completa:
            if aluno['ra'] == ra_aluno:
                aluno_info = aluno
                break
        
        if not aluno_info:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return
        
        lancamento_window = ctk.CTkToplevel(self)
        lancamento_window.title(f"Lançar Notas - {ra_aluno}")
        lancamento_window.geometry("400x500")
        lancamento_window.transient(self)
        lancamento_window.grab_set()

        frame_lancamento = ctk.CTkFrame(lancamento_window)
        frame_lancamento.pack(fill="both", expand=True, padx=20, pady=20)
        
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

        info_faltas = ctk.CTkLabel(
            frame_lancamento,
            text="💡 Limite: máximo 35 faltas por bimestre (70% de 50 aulas)",
            font=("Arial", 10),
            text_color="orange"
        )
        info_faltas.pack(pady=5)

        frame_bimestres = ctk.CTkFrame(frame_lancamento)
        frame_bimestres.pack(fill="both", expand=True, pady=10)

        self.notas_entries = []
        self.faltas_entries = []
        
        for bimestre in range(1, 5):
            frame_bim = ctk.CTkFrame(frame_bimestres)
            frame_bim.pack(fill="x", pady=5)
            
            label_bim = ctk.CTkLabel(frame_bim, text=f"Bimestre {bimestre}:", font=("Arial", 12))
            label_bim.pack(side="left", padx=5)
            
            entry_nota = ctk.CTkEntry(
                frame_bim,
                placeholder_text="Nota (0-10)",
                width=80
            )
            entry_nota.pack(side="left", padx=5)
            self.notas_entries.append(entry_nota)
            
            label_sep = ctk.CTkLabel(frame_bim, text="|")
            label_sep.pack(side="left", padx=5)
            
            entry_faltas = ctk.CTkEntry(
                frame_bim,
                placeholder_text="Faltas (0-35)",
                width=80
            )
            entry_faltas.pack(side="left", padx=5)
            self.faltas_entries.append(entry_faltas)
        
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
        try:
            notas = []
            faltas = []
            
            TOTAL_AULAS_BIMESTRE = 50
            LIMITE_FALTAS = TOTAL_AULAS_BIMESTRE * 0.7
            
            for i, (entry_nota, entry_faltas) in enumerate(zip(self.notas_entries, self.faltas_entries)):
                nota_text = entry_nota.get().strip()
                faltas_text = entry_faltas.get().strip()
                
                if not nota_text and not faltas_text:
                    notas.append(None)
                    faltas.append(None)
                    continue
                
                if nota_text:
                    nota = float(nota_text)
                    if nota < 0 or nota > 10:
                        messagebox.showerror("Erro", f"Nota do bimestre {i+1} deve ser entre 0 e 10!")
                        return
                    notas.append(nota)
                else:
                    notas.append(None)
                
                if faltas_text:
                    falta = int(faltas_text)
                    if falta < 0:
                        messagebox.showerror("Erro", f"Faltas do bimestre {i+1} não podem ser negativas!")
                        return
                    
                    if falta > LIMITE_FALTAS:
                        messagebox.showerror(
                            "Erro", 
                            f"🚫 Faltas do bimestre {i+1} não podem ultrapassar 70% do total de aulas!\n\n"
                            f"• Total de aulas: {TOTAL_AULAS_BIMESTRE}\n"
                            f"• Limite máximo: {LIMITE_FALTAS:.0f}\n"
                            f"• Faltas informadas: {falta}"
                        )
                        return
                    faltas.append(falta)
                else:
                    faltas.append(None)
            
            self.salvar_notas_csv(ra_aluno, self.usuario_logado['disciplina'], notas, faltas)
            
            messagebox.showinfo("Sucesso", "Notas e faltas salvas com sucesso!")
            window.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar notas: {e}")

    def salvar_notas_csv(self, ra_aluno, disciplina, notas, faltas):
        try:
            if not self.df_notas.empty:
                df = self.df_notas.copy()
            else:
                colunas = ['RA_Aluno', 'RA_Professor', 'Disciplina']
                for i in range(1, 5):
                    colunas.extend([f'Nota_Bimestre_{i}', f'Faltas_Bimestre_{i}'])
                df = pd.DataFrame(columns=colunas)
            
            mascara = (df['RA_Aluno'] == ra_aluno) & (df['RA_Professor'] == self.usuario_logado['ra']) & (df['Disciplina'] == disciplina)
            
            if mascara.any():
                idx = df[mascara].index[0]
                for i in range(4):
                    if notas[i] is not None:
                        df.at[idx, f'Nota_Bimestre_{i+1}'] = notas[i]
                    if faltas[i] is not None:
                        df.at[idx, f'Faltas_Bimestre_{i+1}'] = faltas[i]
            else:
                novo_registro = {
                    'RA_Aluno': ra_aluno,
                    'RA_Professor': self.usuario_logado['ra'],
                    'Disciplina': disciplina
                }
                
                for i in range(4):
                    novo_registro[f'Nota_Bimestre_{i+1}'] = notas[i] if notas[i] is not None else 0.0
                    novo_registro[f'Faltas_Bimestre_{i+1}'] = faltas[i] if faltas[i] is not None else 0
                
                df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
            
            df.to_csv('dados_notas.csv', index=False)
            self.df_notas = df
            print(f"✅ Notas salvas para {ra_aluno} em {disciplina}")
            
        except Exception as e:
            raise Exception(f"Erro ao salvar CSV: {e}")

    def mostrar_alunos_professor(self, parent):
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
        
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.scroll_consultar_frame = ctk.CTkScrollableFrame(main_frame)
        self.scroll_consultar_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.carregar_alunos_consulta()

    def carregar_alunos_consulta(self):
        self.lista_consulta_completa = []
        
        alunos_df = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
        
        for _, aluno in alunos_df.iterrows():
            self.lista_consulta_completa.append({
                'ra': aluno['RA'],
                'nome': aluno['Nome'],
                'sobrenome': aluno['Sobrenome']
            })
        
        self.lista_consulta_completa.sort(key=lambda x: x['ra'])
        self.mostrar_alunos_consulta(self.lista_consulta_completa)

    def filtrar_alunos_consulta(self, event=None):
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
        
        header_frame = ctk.CTkFrame(self.scroll_consultar_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(header_frame, text="RA", font=("Arial bold", 12), width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Nome", font=("Arial bold", 12), width=200).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Sobrenome", font=("Arial bold", 12), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Ação", font=("Arial bold", 12), width=100).pack(side="left", padx=5)

        for aluno in alunos:
            aluno_frame = ctk.CTkFrame(self.scroll_consultar_frame)
            aluno_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(aluno_frame, text=aluno['ra'], width=100).pack(side="left", padx=5)
            ctk.CTkLabel(aluno_frame, text=aluno['nome'], width=200).pack(side="left", padx=5)
            ctk.CTkLabel(aluno_frame, text=aluno['sobrenome'], width=150).pack(side="left", padx=5)
            
            btn_detalhes = ctk.CTkButton(
                aluno_frame,
                text="📊 Ver Detalhes",
                command=lambda ra=aluno['ra']: self.abrir_detalhes_aluno(ra),
                width=100,
                height=25,
                font=("Arial", 10)
            )
            btn_detalhes.pack(side="left", padx=5)

        total_frame = ctk.CTkFrame(self.scroll_consultar_frame, fg_color="transparent")
        total_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(total_frame, text=f"Total de alunos: {len(alunos)}", font=("Arial", 12)).pack()

    def abrir_detalhes_aluno(self, ra_aluno):
        aluno_info = None
        for aluno in self.lista_consulta_completa:
            if aluno['ra'] == ra_aluno:
                aluno_info = aluno
                break
        
        if not aluno_info:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            return
        
        notas_aluno = self.df_notas[self.df_notas['RA_Aluno'] == ra_aluno]
        
        detalhes_window = ctk.CTkToplevel(self)
        detalhes_window.title(f"Detalhes do Aluno - {ra_aluno}")
        detalhes_window.geometry("600x500")
        detalhes_window.transient(self)
        detalhes_window.grab_set()

        frame_detalhes = ctk.CTkFrame(detalhes_window)
        frame_detalhes.pack(fill="both", expand=True, padx=20, pady=20)
        
        info_aluno = ctk.CTkLabel(
            frame_detalhes,
            text=f"👤 {aluno_info['nome']} {aluno_info['sobrenome']}\n📋 RA: {aluno_info['ra']}",
            font=("Arial", 16, "bold"),
            justify="center"
        )
        info_aluno.pack(pady=10)

        scroll_frame = ctk.CTkScrollableFrame(frame_detalhes)
        scroll_frame.pack(fill="both", expand=True, pady=10)

        if notas_aluno.empty:
            sem_dados_label = ctk.CTkLabel(
                scroll_frame,
                text="📝 Nenhuma nota registrada para este aluno.",
                font=("Arial", 14),
                text_color="gray"
            )
            sem_dados_label.pack(pady=20)
        else:
            for idx, disciplina in notas_aluno.iterrows():
                disc_frame = ctk.CTkFrame(scroll_frame)
                disc_frame.pack(fill="x", padx=5, pady=5)

                title = ctk.CTkLabel(
                    disc_frame, 
                    text=f"📚 {disciplina['Disciplina']}",
                    font=("Arial bold", 14)
                )
                title.pack(anchor="w", pady=(10, 5))

                header_frame = ctk.CTkFrame(disc_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10)
                
                ctk.CTkLabel(header_frame, text="Bimestre", font=("Arial bold", 11), width=100).pack(side="left")
                ctk.CTkLabel(header_frame, text="Nota", font=("Arial bold", 11), width=80).pack(side="left")
                ctk.CTkLabel(header_frame, text="Faltas", font=("Arial bold", 11), width=80).pack(side="left")

                notas = []
                faltas_totais = 0
                
                for i in range(4):
                    bim_frame = ctk.CTkFrame(disc_frame, fg_color="transparent")
                    bim_frame.pack(fill="x", padx=10)
                    
                    nota_col = f'Nota_Bimestre_{i+1}'
                    faltas_col = f'Faltas_Bimestre_{i+1}'
                    
                    nota = disciplina[nota_col] if nota_col in disciplina and pd.notna(disciplina[nota_col]) else 0
                    faltas = disciplina[faltas_col] if faltas_col in disciplina and pd.notna(disciplina[faltas_col]) else 0
                    
                    if nota > 0:
                        notas.append(nota)
                    faltas_totais += faltas
                    
                    nota_text = f"{nota:.1f}" if nota > 0 else "--"
                    faltas_text = f"{faltas}" if faltas > 0 else "--"
                    
                    ctk.CTkLabel(bim_frame, text=f"{i+1}°", width=100).pack(side="left")
                    ctk.CTkLabel(bim_frame, text=nota_text, width=80).pack(side="left")
                    ctk.CTkLabel(bim_frame, text=faltas_text, width=80).pack(side="left")

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
                    resumo_frame = ctk.CTkFrame(disc_frame)
                    resumo_frame.pack(fill="x", padx=10, pady=5)
                    
                    resumo_label = ctk.CTkLabel(
                        resumo_frame, 
                        text="⏳ Aguardando lançamento de notas", 
                        font=("Arial", 11),
                        text_color="orange"
                    )
                    resumo_label.pack(pady=5)

        btn_fechar = ctk.CTkButton(
            frame_detalhes,
            text="Fechar",
            command=detalhes_window.destroy,
            fg_color="#3498DB"
        )
        btn_fechar.pack(pady=10)

    def mostrar_cadastrar_aluno(self, parent):
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            main_frame,
            text="👨‍🎓 Cadastrar Novo Aluno",
            font=("Arial bold", 20)
        )
        title.pack(pady=10)

        info_professor = ctk.CTkLabel(
            main_frame,
            text=f"Professor: {self.usuario_logado['nome']} | Disciplina: {self.usuario_logado['disciplina']}",
            font=("Arial", 12),
            text_color="blue"
        )
        info_professor.pack(pady=5)

        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", pady=20, padx=50)

        ctk.CTkLabel(form_frame, text="Nome do Aluno:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        self.nome_aluno_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Digite o nome do aluno",
            width=300
        )
        self.nome_aluno_entry.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(form_frame, text="Sobrenome do Aluno:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        self.sobrenome_aluno_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Digite o sobrenome do aluno",
            width=300
        )
        self.sobrenome_aluno_entry.pack(fill="x", pady=5, padx=10)

        info_auto_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        info_auto_frame.pack(fill="x", pady=10, padx=10)

        info_text = """💡 Informações que serão geradas automaticamente:
• RA do aluno (ALUN##)
• Status: Ativo
• Tipo: Aluno
• Disciplina vinculada: A mesma do professor"""
        
        ctk.CTkLabel(
            info_auto_frame,
            text=info_text,
            font=("Arial", 10),
            text_color="green",
            justify="left"
        ).pack(anchor="w")

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
        nome = self.nome_aluno_entry.get().strip()
        sobrenome = self.sobrenome_aluno_entry.get().strip()

        if not nome or not sobrenome:
            messagebox.showwarning("Cadastro", "Por favor, preencha nome e sobrenome!")
            return

        if len(nome) < 2 or len(sobrenome) < 2:
            messagebox.showwarning("Cadastro", "Nome e sobrenome devem ter pelo menos 2 caracteres!")
            return

        try:
            alunos_existentes = self.df_usuarios[self.df_usuarios['Tipo'] == 1]
            novo_numero = len(alunos_existentes) + 1
            novo_ra = f"ALUN{novo_numero:02d}"

            while novo_ra in self.df_usuarios['RA'].values:
                novo_numero += 1
                novo_ra = f"ALUN{novo_numero:02d}"

            novo_aluno = {
                'RA': novo_ra,
                'Nome': nome,
                'Sobrenome': sobrenome,
                'Tipo': 1,
                'Disciplina': self.usuario_logado['disciplina'],
                'Ativo': 1
            }

            novo_df = pd.DataFrame([novo_aluno])
            self.df_usuarios = pd.concat([self.df_usuarios, novo_df], ignore_index=True)

            self.df_usuarios.to_csv('dados_usuarios.csv', index=False)

            mensagem = f"""✅ Aluno cadastrado com sucesso!

📋 RA: {novo_ra}
🧑‍🎓 Nome: {nome} {sobrenome}
📚 Disciplina: {self.usuario_logado['disciplina']}
🟢 Status: Ativo

💡 O aluno já pode receber notas e faltas!"""
            
            messagebox.showinfo("Sucesso", mensagem)

            self.limpar_campos_cadastro()
            self.carregar_dados()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {e}")

    def limpar_campos_cadastro(self):
        self.nome_aluno_entry.delete(0, 'end')
        self.sobrenome_aluno_entry.delete(0, 'end')

    def mostrar_estatisticas_professor(self, parent):
        total_alunos = len(self.df_usuarios[self.df_usuarios['Tipo'] == 1])
        total_registros = len(self.df_notas) if not self.df_notas.empty else 0
        
        info_text = f"""📊 ESTATÍSTICAS DO SISTEMA

👨‍🎓 Total de Alunos: {total_alunos}
📝 Registros de Notas: {total_registros}
📚 Sua Disciplina: {self.usuario_logado['disciplina']}

💡 Funcionalidades disponíveis:
• Consultar todos os alunos
• Visualizar estatísticas
• Acompanhar desempenho"""
        
        info_label = ctk.CTkLabel(parent, text=info_text, font=("Arial", 12), justify="left")
        info_label.pack(pady=20)

    # ===============================
    # ÁREA DO ADMINISTRADOR (ATUALIZADA)
    # ===============================

    def show_admin_frame(self):
        admin_frame = ctk.CTkFrame(self)
        
        header_frame = ctk.CTkFrame(admin_frame, fg_color="transparent")
        header_frame.pack(pady=20)
        
        title = ctk.CTkLabel(header_frame, text=f"👨‍💼 Área do Administrador", font=("Arial bold", 24))
        title.pack()
        
        user_info = ctk.CTkLabel(header_frame,
                                text=f"{self.usuario_logado['nome']} {self.usuario_logado['sobrenome']}",
                                font=("Arial", 14), text_color="gray")
        user_info.pack(pady=5)

        # TABVIEW COM NOVA ABA
        tabview = ctk.CTkTabview(admin_frame)
        tabview.pack(expand=True, fill="both", padx=20, pady=10)
        
        # ABA NOVA ADICIONADA AQUI 👇
        tabview.add("👥 Gestão de Usuários")
        tabview.add("Estatísticas Gerais")
        tabview.add("Todos os Usuários")

        # CONTEÚDO DAS ABAS
        self.mostrar_gestao_usuarios(tabview.tab("👥 Gestão de Usuários"))
        self.mostrar_estatisticas_admin(tabview.tab("Estatísticas Gerais"))
        self.mostrar_todos_usuarios(tabview.tab("Todos os Usuários"))

        logout_button = ctk.CTkButton(admin_frame, text="🚪 Sair", command=self.logout, fg_color="#E74C3C")
        logout_button.pack(pady=10)

        self.switch_frame(admin_frame)

    # ===============================
    # NOVO MÉTODO: mostrar_gestao_usuarios (SEM BUSCA)
    # ===============================
    def mostrar_gestao_usuarios(self, parent):
        """Exibe interface de gestão de usuários"""
        # Inicializar gerenciador
        self.admin_user_manager = AdminUserManager(self.df_usuarios)
        
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # TÍTULO
        title = ctk.CTkLabel(
            main_frame,
            text="👥 GESTÃO DE USUÁRIOS",
            font=("Arial bold", 20),
            text_color="#2C3E50"
        )
        title.pack(pady=10)
        
        # BOTÕES DE AÇÃO RÁPIDA
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            action_frame,
            text="⚡ Ações Rápidas:",
            font=("Arial bold", 13)
        ).pack(anchor="w", pady=(0, 10))
        
        # BOTÕES EM GRADE
        grid_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        grid_frame.pack(fill="x")
        
        # Cadastrar Professor
        btn_cad_prof = ctk.CTkButton(
            grid_frame,
            text="👨‍🏫 Cadastrar Professor",
            command=self.abrir_cadastro_professor,
            width=180,
            height=40,
            fg_color="#3498DB",
            hover_color="#2980B9",
            font=("Arial", 12, "bold")
        )
        btn_cad_prof.grid(row=0, column=0, padx=5, pady=5)
        
        # Cadastrar Admin
        btn_cad_admin = ctk.CTkButton(
            grid_frame,
            text="👨‍💼 Cadastrar Administrador",
            command=self.abrir_cadastro_admin,
            width=180,
            height=40,
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            font=("Arial", 12, "bold")
        )
        btn_cad_admin.grid(row=0, column=1, padx=5, pady=5)
        
        # Desativar/Ativar Aluno
        btn_toggle_aluno = ctk.CTkButton(
            grid_frame,
            text="⏸️ Gerenciar Aluno",
            command=lambda: self.abrir_gerenciar_usuario("aluno"),
            width=180,
            height=40,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            font=("Arial", 12, "bold")
        )
        btn_toggle_aluno.grid(row=1, column=0, padx=5, pady=5)
        
        # Desativar/Ativar Professor
        btn_toggle_prof = ctk.CTkButton(
            grid_frame,
            text="⏸️ Gerenciar Professor",
            command=lambda: self.abrir_gerenciar_usuario("professor"),
            width=180,
            height=40,
            fg_color="#F39C12",
            hover_color="#D68910",
            font=("Arial", 12, "bold")
        )
        btn_toggle_prof.grid(row=1, column=1, padx=5, pady=5)
        
        # ESTATÍSTICAS RÁPIDAS
        stats_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        stats_frame.pack(fill="x", pady=15, padx=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 ESTATÍSTICAS DO SISTEMA",
            font=("Arial bold", 14),
            text_color="#2C3E50"
        ).pack(pady=(10, 5))
        
        self.stats_labels = {}
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=10, pady=(0, 10))
        
        estatisticas = self.admin_user_manager.get_estatisticas()
        
        # Total de Usuários
        card_total = ctk.CTkFrame(stats_grid, height=60, corner_radius=8,
                                fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card_total.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card_total, text="👥", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card_total, text="TOTAL", font=("Arial bold", 9), text_color="gray").pack()
        self.stats_labels['total'] = ctk.CTkLabel(
            card_total, 
            text=f"{estatisticas.get('total', 0)}", 
            font=("Arial bold", 16), 
            text_color="#3498DB"
        )
        self.stats_labels['total'].pack()
        
        # Alunos
        card_alunos = ctk.CTkFrame(stats_grid, height=60, corner_radius=8,
                                fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card_alunos.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card_alunos, text="👨‍🎓", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card_alunos, text="ALUNOS", font=("Arial bold", 9), text_color="gray").pack()
        self.stats_labels['alunos'] = ctk.CTkLabel(
            card_alunos,
            text=f"{estatisticas.get('alunos_ativos', 0)}/{estatisticas.get('alunos', 0)}",
            font=("Arial bold", 12),
            text_color="#2ECC71"
        )
        self.stats_labels['alunos'].pack()
        
        # Professores
        card_prof = ctk.CTkFrame(stats_grid, height=60, corner_radius=8,
                                fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card_prof.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card_prof, text="👨‍🏫", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card_prof, text="PROFESSORES", font=("Arial bold", 9), text_color="gray").pack()
        self.stats_labels['professores'] = ctk.CTkLabel(
            card_prof,
            text=f"{estatisticas.get('professores_ativos', 0)}/{estatisticas.get('professores', 0)}",
            font=("Arial bold", 12),
            text_color="#E74C3C"
        )
        self.stats_labels['professores'].pack()
        
        # Admins
        card_admins = ctk.CTkFrame(stats_grid, height=60, corner_radius=8,
                                fg_color="#F8F9FA", border_width=1, border_color="#E9ECEF")
        card_admins.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card_admins, text="👨‍💼", font=("Arial", 20)).pack(pady=(10, 2))
        ctk.CTkLabel(card_admins, text="ADMINS", font=("Arial bold", 9), text_color="gray").pack()
        self.stats_labels['admins'] = ctk.CTkLabel(
            card_admins,
            text=f"{estatisticas.get('admins_ativos', 0)}/{estatisticas.get('admins', 0)}",
            font=("Arial bold", 12),
            text_color="#9B59B6"
        )
        self.stats_labels['admins'].pack()
        
        # Configurar grid
        for i in range(4):
            stats_grid.columnconfigure(i, weight=1)

    def abrir_cadastro_professor(self):
        """Abre janela para cadastrar novo professor"""
        janela = ctk.CTkToplevel(self)
        janela.title("👨‍🏫 Cadastrar Novo Professor")
        janela.geometry("500x400")
        janela.transient(self)
        janela.grab_set()
        
        frame = ctk.CTkFrame(janela)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            frame,
            text="📝 CADASTRAR PROFESSOR",
            font=("Arial bold", 18),
            text_color="#2C3E50"
        ).pack(pady=10)
        
        # Formulário
        form_frame = ctk.CTkFrame(frame, fg_color="transparent")
        form_frame.pack(fill="x", pady=15)
        
        # Nome
        ctk.CTkLabel(form_frame, text="Nome:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        entry_nome = ctk.CTkEntry(form_frame, placeholder_text="Nome do professor", width=300)
        entry_nome.pack(fill="x", pady=5)
        
        # Sobrenome
        ctk.CTkLabel(form_frame, text="Sobrenome:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        entry_sobrenome = ctk.CTkEntry(form_frame, placeholder_text="Sobrenome do professor", width=300)
        entry_sobrenome.pack(fill="x", pady=5)
        
        # Disciplina
        ctk.CTkLabel(form_frame, text="Disciplina:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        entry_disciplina = ctk.CTkEntry(form_frame, placeholder_text="Ex: Matemática, Português", width=300)
        entry_disciplina.pack(fill="x", pady=5)
        
        # Informações geradas automaticamente
        info_frame = ctk.CTkFrame(frame, corner_radius=8, fg_color="#EBF5FB")
        info_frame.pack(fill="x", pady=10)
        
        info_text = """💡 Informações geradas automaticamente:
• RA do professor (PROF##)
• Senha inicial: sobrenome (minúsculas)
• Status: Ativo"""
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Arial", 10),
            text_color="#2C3E50",
            justify="left"
        ).pack(padx=10, pady=10)
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        
        def cadastrar():
            nome = entry_nome.get().strip()
            sobrenome = entry_sobrenome.get().strip()
            disciplina = entry_disciplina.get().strip()
            
            if not nome or not sobrenome or not disciplina:
                messagebox.showwarning("Campos Obrigatórios", "Preencha todos os campos!")
                return
            
            try:
                professor, mensagem = self.admin_user_manager.cadastrar_professor(nome, sobrenome, disciplina)
                
                # Adicionar ao dataframe
                novo_df = pd.DataFrame([professor])
                self.df_usuarios = pd.concat([self.df_usuarios, novo_df], ignore_index=True)
                
                # Salvar CSV
                self.df_usuarios.to_csv('dados_usuarios.csv', index=False)
                
                messagebox.showinfo("✅ Sucesso", mensagem)
                janela.destroy()
                
                # Atualizar estatísticas
                self.atualizar_estatisticas_gestao()
                
            except Exception as e:
                messagebox.showerror("❌ Erro", str(e))
        
        btn_cadastrar = ctk.CTkButton(
            btn_frame,
            text="✅ Cadastrar Professor",
            command=cadastrar,
            fg_color="#27AE60",
            hover_color="#219955",
            height=40
        )
        btn_cadastrar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=janela.destroy,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            height=40
        )
        btn_cancelar.pack(side="left", padx=5)

    def abrir_cadastro_admin(self):
        """Abre janela para cadastrar novo administrador"""
        janela = ctk.CTkToplevel(self)
        janela.title("👨‍💼 Cadastrar Novo Administrador")
        janela.geometry("500x350")
        janela.transient(self)
        janela.grab_set()
        
        frame = ctk.CTkFrame(janela)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            frame,
            text="🔐 CADASTRAR ADMINISTRADOR",
            font=("Arial bold", 18),
            text_color="#2C3E50"
        ).pack(pady=10)
        
        # Aviso de segurança
        aviso_frame = ctk.CTkFrame(frame, corner_radius=8, fg_color="#FDEDEC")
        aviso_frame.pack(fill="x", pady=(0, 15))
        
        aviso_text = """⚠️ AVISO DE SEGURANÇA:
Esta ação concede acesso completo ao sistema.
Apenas administradores podem cadastrar novos administradores."""
        
        ctk.CTkLabel(
            aviso_frame,
            text=aviso_text,
            font=("Arial", 10, "bold"),
            text_color="#C0392B",
            justify="left"
        ).pack(padx=10, pady=10)
        
        # Formulário
        form_frame = ctk.CTkFrame(frame, fg_color="transparent")
        form_frame.pack(fill="x", pady=10)
        
        # Nome
        ctk.CTkLabel(form_frame, text="Nome:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        entry_nome = ctk.CTkEntry(form_frame, placeholder_text="Nome do administrador", width=300)
        entry_nome.pack(fill="x", pady=5)
        
        # Sobrenome
        ctk.CTkLabel(form_frame, text="Sobrenome:", font=("Arial", 12)).pack(anchor="w", pady=(10, 5))
        entry_sobrenome = ctk.CTkEntry(form_frame, placeholder_text="Sobrenome do administrador", width=300)
        entry_sobrenome.pack(fill="x", pady=5)
        
        # Informações
        info_frame = ctk.CTkFrame(frame, corner_radius=8, fg_color="#EBF5FB")
        info_frame.pack(fill="x", pady=10)
        
        info_text = """💡 Informações geradas automaticamente:
• RA do administrador (ADM###)
• Senha inicial: sobrenome (minúsculas)
• Status: Ativo
• Permissões: Acesso completo"""
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Arial", 10),
            text_color="#2C3E50",
            justify="left"
        ).pack(padx=10, pady=10)
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        
        def cadastrar():
            nome = entry_nome.get().strip()
            sobrenome = entry_sobrenome.get().strip()
            
            if not nome or not sobrenome:
                messagebox.showwarning("Campos Obrigatórios", "Preencha todos os campos!")
                return
            
            # Confirmação extra para cadastro de admin
            confirmacao = messagebox.askyesno(
                "Confirmação Importante",
                f"Tem certeza que deseja cadastrar {nome} {sobrenome} como administrador?\n\n"
                "Esta pessoa terá acesso completo ao sistema."
            )
            
            if not confirmacao:
                return
            
            try:
                admin, mensagem = self.admin_user_manager.cadastrar_admin(nome, sobrenome)
                
                # Adicionar ao dataframe
                novo_df = pd.DataFrame([admin])
                self.df_usuarios = pd.concat([self.df_usuarios, novo_df], ignore_index=True)
                
                # Salvar CSV
                self.df_usuarios.to_csv('dados_usuarios.csv', index=False)
                
                messagebox.showinfo("✅ Sucesso", mensagem)
                janela.destroy()
                
                # Atualizar estatísticas
                self.atualizar_estatisticas_gestao()
                
            except Exception as e:
                messagebox.showerror("❌ Erro", str(e))
        
        btn_cadastrar = ctk.CTkButton(
            btn_frame,
            text="🔐 Cadastrar Admin",
            command=cadastrar,
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            height=40
        )
        btn_cadastrar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=janela.destroy,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            height=40
        )
        btn_cancelar.pack(side="left", padx=5)

    def abrir_gerenciar_usuario(self, tipo_usuario):
        """Abre janela para gerenciar (desativar/ativar) usuário"""
        janela = ctk.CTkToplevel(self)
        janela.title(f"⏸️ Gerenciar {tipo_usuario.capitalize()}")
        janela.geometry("700x550")
        janela.transient(self)
        janela.grab_set()
        
        frame = ctk.CTkFrame(janela)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            frame,
            text=f"⏸️ GERENCIAR {tipo_usuario.upper()}",
            font=("Arial bold", 18),
            text_color="#2C3E50"
        ).pack(pady=10)
        
        # Frame de busca FUNCIONAL
        search_frame = ctk.CTkFrame(frame)
        search_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍 Buscar:",
            font=("Arial", 12)
        ).pack(side="left", padx=5)
        
        # Entry para busca com variável local
        entry_busca = ctk.CTkEntry(
            search_frame,
            placeholder_text=f"Digite RA, nome ou sobrenome do {tipo_usuario}...",
            width=300
        )
        entry_busca.pack(side="left", padx=5, fill="x", expand=True)
        
        # Frame para os resultados
        resultados_container = ctk.CTkFrame(frame)
        resultados_container.pack(fill="both", expand=True, pady=10)
        
        # Scrollable frame para resultados
        scroll_frame = ctk.CTkScrollableFrame(resultados_container, height=300)
        scroll_frame.pack(fill="both", expand=True)
        
        # Filtrar usuários pelo tipo
        tipo_numero = {"aluno": 1, "professor": 2, "admin": 3}[tipo_usuario]
        usuarios_tipo = self.df_usuarios[self.df_usuarios['Tipo'] == tipo_numero].copy()
        
        def atualizar_lista(filtro_texto=""):
            """Atualiza a lista de usuários com base no filtro"""
            # Limpar frame anterior
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            
            # Aplicar filtro se houver texto
            if filtro_texto:
                filtro = filtro_texto.strip().upper()
                usuarios_filtrados = usuarios_tipo[
                    usuarios_tipo['RA'].str.contains(filtro, na=False) |
                    usuarios_tipo['Nome'].str.upper().str.contains(filtro, na=False) |
                    usuarios_tipo['Sobrenome'].str.upper().str.contains(filtro, na=False)
                ]
            else:
                usuarios_filtrados = usuarios_tipo
            
            if usuarios_filtrados.empty:
                ctk.CTkLabel(
                    scroll_frame,
                    text=f"Nenhum {tipo_usuario} encontrado{' com o filtro aplicado' if filtro_texto else ''}.",
                    font=("Arial", 12),
                    text_color="gray"
                ).pack(pady=20)
                return
            
            # Header da tabela
            header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 5))
            
            ctk.CTkLabel(header_frame, text="RA", font=("Arial bold", 11), width=80).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Nome", font=("Arial bold", 11), width=180).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Sobrenome", font=("Arial bold", 11), width=120).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Status", font=("Arial bold", 11), width=80).pack(side="left", padx=5)
            ctk.CTkLabel(header_frame, text="Ação", font=("Arial bold", 11), width=100).pack(side="left", padx=5)
            
            # Lista de usuários
            for _, usuario in usuarios_filtrados.iterrows():
                user_frame = ctk.CTkFrame(scroll_frame)
                user_frame.pack(fill="x", pady=2)
                
                ra = usuario['RA']
                nome = usuario['Nome']
                sobrenome = usuario['Sobrenome']
                status = "✅ Ativo" if usuario['Ativo'] == 1 else "⏸️ Inativo"
                cor_status = "#27AE60" if usuario['Ativo'] == 1 else "#E74C3C"
                
                # Colunas
                ctk.CTkLabel(user_frame, text=ra, width=80).pack(side="left", padx=5)
                ctk.CTkLabel(user_frame, text=nome, width=180).pack(side="left", padx=5)
                ctk.CTkLabel(user_frame, text=sobrenome, width=120).pack(side="left", padx=5)
                ctk.CTkLabel(user_frame, text=status, width=80, text_color=cor_status).pack(side="left", padx=5)
                
                # Botão de ação
                btn_text = "⏸️ Desativar" if usuario['Ativo'] == 1 else "✅ Ativar"
                btn_color = "#E74C3C" if usuario['Ativo'] == 1 else "#27AE60"
                
                btn_acao = ctk.CTkButton(
                    user_frame,
                    text=btn_text,
                    command=lambda ra=ra, tipo=tipo_usuario, jan=janela: self.toggle_status_usuario(ra, tipo, jan),
                    width=100,
                    height=25,
                    fg_color=btn_color,
                    font=("Arial", 10)
                )
                btn_acao.pack(side="left", padx=5)
        
        # Função para atualizar ao digitar
        def on_key_release(event=None):
            filtro = entry_busca.get().strip()
            atualizar_lista(filtro)
        
        # Vincular evento de tecla
        entry_busca.bind("<KeyRelease>", on_key_release)
        
        # Inicializar lista
        atualizar_lista()
        
        # Botões
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        btn_fechar = ctk.CTkButton(
            btn_frame,
            text="Fechar",
            command=janela.destroy,
            width=120
        )
        btn_fechar.pack()

    def toggle_status_usuario(self, ra_usuario, tipo_usuario, janela_pai):
        """Alterna status do usuário"""
        try:
            # Não permitir desativar a si mesmo
            if ra_usuario == self.usuario_logado['ra']:
                messagebox.showwarning(
                    "Ação não permitida",
                    "Você não pode desativar sua própria conta!"
                )
                return
            
            # Confirmação
            usuario_info = self.df_usuarios[self.df_usuarios['RA'] == ra_usuario].iloc[0]
            status_atual = "ativo" if usuario_info['Ativo'] == 1 else "inativo"
            nova_acao = "desativar" if usuario_info['Ativo'] == 1 else "ativar"
            
            confirmacao = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja {nova_acao} o usuário?\n\n"
                f"RA: {ra_usuario}\n"
                f"Nome: {usuario_info['Nome']}\n"
                f"Status atual: {status_atual}"
            )
            
            if not confirmacao:
                return
            
            # Executar ação
            mensagem = self.admin_user_manager.toggle_status_usuario(ra_usuario)
            
            # Atualizar dataframe
            self.df_usuarios = self.admin_user_manager.df_usuarios
            
            # Salvar CSV
            self.df_usuarios.to_csv('dados_usuarios.csv', index=False)
            
            # Recarregar dados
            self.carregar_dados()
            
            messagebox.showinfo("✅ Sucesso", mensagem)
            
            # Atualizar estatísticas
            self.atualizar_estatisticas_gestao()
            
            # Fechar janela atual
            janela_pai.destroy()
            
            # Reabrir janela de gerenciamento com dados atualizados
            self.abrir_gerenciar_usuario(tipo_usuario)
            
        except Exception as e:
            messagebox.showerror("❌ Erro", str(e))

    def atualizar_estatisticas_gestao(self):
        """Atualiza as estatísticas na aba de gestão"""
        if hasattr(self, 'stats_labels') and hasattr(self, 'admin_user_manager'):
            estatisticas = self.admin_user_manager.get_estatisticas()
            
            if 'total' in self.stats_labels:
                self.stats_labels['total'].configure(text=f"{estatisticas.get('total', 0)}")
            
            if 'alunos' in self.stats_labels:
                self.stats_labels['alunos'].configure(
                    text=f"{estatisticas.get('alunos_ativos', 0)}/{estatisticas.get('alunos', 0)}"
                )
            
            if 'professores' in self.stats_labels:
                self.stats_labels['professores'].configure(
                    text=f"{estatisticas.get('professores_ativos', 0)}/{estatisticas.get('professores', 0)}"
                )
            
            if 'admins' in self.stats_labels:
                self.stats_labels['admins'].configure(
                    text=f"{estatisticas.get('admins_ativos', 0)}/{estatisticas.get('admins', 0)}"
                )

    def mostrar_estatisticas_admin(self, parent):
        total_alunos = len(self.df_usuarios[self.df_usuarios['Tipo'] == 1])
        total_professores = len(self.df_usuarios[self.df_usuarios['Tipo'] == 2])
        total_admins = len(self.df_usuarios[self.df_usuarios['Tipo'] == 3])
        total_registros = len(self.df_notas) if not self.df_notas.empty else 0
        
        info_text = f"""📈 ESTATÍSTICAS COMPLETAS

👥 TOTAL DE USUÁRIOS: {len(self.df_usuarios)}
👨‍🎓 Alunos: {total_alunos}
👨‍🏫 Professores: {total_professores}
👨‍💼 Administradores: {total_admins}

📊 REGISTROS ACADÊMICOS:
📝 Registros de notas: {total_registros}

💡 Funcionalidades disponíveis:
• Visualizar todas as estatísticas
• Gerenciar usuários do sistema
• Acessar todos os registros"""
        
        info_label = ctk.CTkLabel(parent, text=info_text, font=("Arial", 12), justify="left")
        info_label.pack(pady=20)

    def mostrar_todos_usuarios(self, parent):
        if self.df_usuarios.empty:
            lbl_sem_dados = ctk.CTkLabel(parent, text="Nenhum usuário cadastrado.", font=("Arial", 14))
            lbl_sem_dados.pack(expand=True)
            return

        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)

        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(header_frame, text="RA", font=("Arial bold", 12), width=80).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Nome", font=("Arial bold", 12), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Sobrenome", font=("Arial bold", 12), width=120).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Tipo", font=("Arial bold", 12), width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header_frame, text="Disciplina", font=("Arial bold", 12), width=120).pack(side="left", padx=5)

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