#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Headers específicos para cada sistema
#ifdef _WIN32
#include <conio.h>
#else
#include <termios.h>
#include <unistd.h>
#endif

// Constantes do sistema
#define MAX_USUARIOS 100
#define MAX_ALUNOS 50
#define MAX_PROFESSORES 20
#define TAM_RA 7
#define TAM_NOME 50
#define TAM_SOBRENOME 50
#define TAM_DISCIPLINA 50
#define ARQUIVO_CSV "dados_usuarios.csv"
#define ARQUIVO_NOTAS "dados_notas.csv"
#define BIMESTRES 4
#define SENHA_ADMIN "admin123"  // Senha fixa para o admin

// Estrutura para notas e faltas
typedef struct {
    float notas[BIMESTRES];     // Notas dos 4 bimestres
    int faltas[BIMESTRES];      // Faltas por bimestre
    char disciplina[TAM_DISCIPLINA]; // Disciplina relacionada
    char ra_aluno[TAM_RA];      // RA do aluno
    char ra_professor[TAM_RA];  // RA do professor que lancou
} NotasFaltas;

// Estrutura do usuario - MODIFICADA: campo 'ativo' adicionado
typedef struct {
    char ra[TAM_RA];
    char nome[TAM_NOME];
    char sobrenome[TAM_SOBRENOME];
    char disciplina[TAM_DISCIPLINA];
    int tipo; // 1=Aluno, 2=Professor, 3=Admin
    int ativo; // 1=Ativo, 0=Inativo - NOVO CAMPO
} Usuario;

// Variaveis globais
Usuario usuarios[MAX_USUARIOS];
NotasFaltas registros[MAX_ALUNOS * BIMESTRES];
int totalUsuarios = 0;
int totalRegistros = 0;

// Disciplinas disponiveis
const char *disciplinas[] = {
    "Matematica",
    "Portugues",
    "Ciencias",
    "Geografia"
};
const int total_disciplinas = 4;

// ===============================
// FUNCAO GETCH MULTIPLATAFORMA
// ===============================

#ifndef _WIN32
// Implementacao do getch
char getch() {
    char buf = 0;
    struct termios old = {0};
    if (tcgetattr(0, &old) < 0)
        perror("tcsetattr()");
    old.c_lflag &= ~ICANON;
    old.c_lflag &= ~ECHO;
    old.c_cc[VMIN] = 1;
    old.c_cc[VTIME] = 0;
    if (tcsetattr(0, TCSANOW, &old) < 0)
        perror("tcsetattr ICANON");
    if (read(0, &buf, 1) < 0)
        perror("read()");
    old.c_lflag |= ICANON;
    old.c_lflag |= ECHO;
    if (tcsetattr(0, TCSADRAIN, &old) < 0)
        perror("tcsetattr ~ICANON");
    return buf;
}
#endif

// ===============================
// SISTEMA DE SENHA
// ===============================

// Verificar senha do Admin
int verificarSenhaAdmin() {
    char senha[50];
    int tentativas = 0;
    const int max_tentativas = 3;
    
    printf("\n=== ACESSO ADMINISTRATIVO ===\n");
    
    while (tentativas < max_tentativas) {
        printf("\nTentativa %d de %d\n", tentativas + 1, max_tentativas);
        printf("Digite a senha de administrador: ");
        
        // Ler senha sem eco (para seguranca)
        int i = 0;
        char ch;
        while ((ch = getch()) != '\r' && ch != '\n' && i < 49) {
            if (ch == 8 || ch == 127) { // Backspace (Windows=8, Linux=127)
                if (i > 0) {
                    i--;
                    printf("\b \b");
                }
            } else {
                senha[i++] = ch;
                printf("*");
            }
        }
        senha[i] = '\0';
        printf("\n");
        
        if (strcmp(senha, SENHA_ADMIN) == 0) {
            printf("\n=== ACESSO PERMITIDO ===\n");
            return 1; // Senha correta
        } else {
            tentativas++;
            printf("Senha incorreta!\n");
            
            if (tentativas < max_tentativas) {
                printf("Tente novamente.\n");
            }
        }
    }
    
    printf("\n=== ACESSO BLOQUEADO ===\n");
    printf("Numero maximo de tentativas excedido.\n");
    return 0; // Senha incorreta
}

// ===============================
// FUNCOES PRINCIPAIS
// ===============================

// Gera RA automatico
void gerarRA(char *ra, int tipo) {
    int count = 0;
    for (int i = 0; i < totalUsuarios; i++) {
        if (usuarios[i].tipo == tipo) {
            count++;
        }
    }
    switch (tipo) {
        case 1: sprintf(ra, "ALUN%02d", count + 1); break;
        case 2: sprintf(ra, "PROF%02d", count + 1); break;
        case 3: sprintf(ra, "ADM%03d", count + 1); break;
    }
}

// Verifica se RA existe
int RAExiste(const char *ra) {
    for (int i = 0; i < totalUsuarios; i++) {
        if (strcmp(usuarios[i].ra, ra) == 0) {
            return 1;
        }
    }
    return 0;
}

// Exibe menu de disciplinas
void mostrarDisciplinas() {
    printf("\nDisciplinas disponiveis:\n");
    for (int i = 0; i < total_disciplinas; i++) {
        printf("%d. %s\n", i + 1, disciplinas[i]);
    }
}

// Escolhe disciplina
void escolherDisciplina(char *disciplina) {
    int opcao;
    do {
        mostrarDisciplinas();
        printf("Escolha a disciplina (1-%d): ", total_disciplinas);
        scanf("%d", &opcao);
        getchar();
        if (opcao >= 1 && opcao <= total_disciplinas) {
            strcpy(disciplina, disciplinas[opcao - 1]);
            break;
        } else {
            printf("Opcao invalida! Tente novamente.\n");
        }
    } while (1);
}

// Salvar usuarios em CSV - MODIFICADA: campo 'ativo' adicionado
void salvarCSV() {
    FILE *arquivo = fopen(ARQUIVO_CSV, "w");
    if (arquivo == NULL) {
        printf("Erro ao criar arquivo CSV!\n");
        return;
    }

    fprintf(arquivo, "RA,Nome,Sobrenome,Tipo,Disciplina,Ativo\n"); // NOVO CAMPO

    for (int i = 0; i < totalUsuarios; i++) {
        fprintf(arquivo, "%s,%s,%s,%d,%s,%d\n",
                usuarios[i].ra,
                usuarios[i].nome,
                usuarios[i].sobrenome,
                usuarios[i].tipo,
                usuarios[i].disciplina,
                usuarios[i].ativo); // NOVO CAMPO
    }

    fclose(arquivo);
    printf("Dados salvos em '%s'\n", ARQUIVO_CSV);
}

// Carregar usuarios do CSV - MODIFICADA: campo 'ativo' adicionado
void carregarCSV() {
    FILE *arquivo = fopen(ARQUIVO_CSV, "r");
    if (arquivo == NULL) {
        return;
    }

    char linha[256];
    int primeira_linha = 1;

    while (fgets(linha, sizeof(linha), arquivo) && totalUsuarios < MAX_USUARIOS) {
        if (primeira_linha) {
            primeira_linha = 0;
            continue;
        }

        linha[strcspn(linha, "\n")] = 0;

        char *token;
        int campo = 0;

        token = strtok(linha, ",");
        while (token != NULL && campo < 6) { // Aumentado para 6 campos
            switch (campo) {
                case 0: strcpy(usuarios[totalUsuarios].ra, token); break;
                case 1: strcpy(usuarios[totalUsuarios].nome, token); break;
                case 2: strcpy(usuarios[totalUsuarios].sobrenome, token); break;
                case 3: usuarios[totalUsuarios].tipo = atoi(token); break;
                case 4: strcpy(usuarios[totalUsuarios].disciplina, token); break;
                case 5: usuarios[totalUsuarios].ativo = atoi(token); break; // NOVO CAMPO
            }
            token = strtok(NULL, ",");
            campo++;
        }
        
        // Se o campo ativo nao existir (arquivo antigo), definir como ativo por padrao
        if (campo < 6) {
            usuarios[totalUsuarios].ativo = 1;
        }
        
        totalUsuarios++;
    }

    fclose(arquivo);
}

// Encontrar usuario por RA
Usuario* encontrarUsuarioPorRA(const char *ra) {
    for (int i = 0; i < totalUsuarios; i++) {
        if (strcmp(usuarios[i].ra, ra) == 0) {
            return &usuarios[i];
        }
    }
    return NULL;
}

// Listar alunos - MODIFICADA: mostra apenas alunos ativos
void listarAlunos() {
    printf("\n=== LISTA DE ALUNOS ATIVOS ===\n");
    int encontrou = 0;
    for (int i = 0; i < totalUsuarios; i++) {
        if (usuarios[i].tipo == 1 && usuarios[i].ativo == 1) { // Apenas alunos ativos
            printf("RA: %s | Nome: %s %s | Status: %s\n",
                   usuarios[i].ra, 
                   usuarios[i].nome, 
                   usuarios[i].sobrenome,
                   usuarios[i].ativo ? "ATIVO" : "INATIVO");
            encontrou = 1;
        }
    }
    if (!encontrou) {
        printf("Nenhum aluno ativo cadastrado.\n");
    }
}

// Listar alunos inativos - NOVA FUNCAO
void listarAlunosInativos() {
    printf("\n=== LISTA DE ALUNOS INATIVOS ===\n");
    int encontrou = 0;
    for (int i = 0; i < totalUsuarios; i++) {
        if (usuarios[i].tipo == 1 && usuarios[i].ativo == 0) { // Apenas alunos inativos
            printf("RA: %s | Nome: %s %s | Status: INATIVO\n",
                   usuarios[i].ra, 
                   usuarios[i].nome, 
                   usuarios[i].sobrenome);
            encontrou = 1;
        }
    }
    if (!encontrou) {
        printf("Nenhum aluno inativo encontrado.\n");
    }
}

// Listar todos os alunos (incluindo inativos) - NOVA FUNCAO
void listarTodosAlunos() {
    printf("\n=== LISTA COMPLETA DE ALUNOS ===\n");
    int encontrou = 0;
    for (int i = 0; i < totalUsuarios; i++) {
        if (usuarios[i].tipo == 1) {
            printf("RA: %s | Nome: %s %s | Status: %s\n",
                   usuarios[i].ra, 
                   usuarios[i].nome, 
                   usuarios[i].sobrenome,
                   usuarios[i].ativo ? "ATIVO" : "INATIVO");
            encontrou = 1;
        }
    }
    if (!encontrou) {
        printf("Nenhum aluno cadastrado.\n");
    }
}

// Listar professores
void listarProfessores() {
    printf("\n=== LISTA DE PROFESSORES ===\n");
    int encontrou = 0;
    for (int i = 0; i < totalUsuarios; i++) {
        if (usuarios[i].tipo == 2) {
            printf("RA: %s | Nome: %s %s | Disciplina: %s\n",
                   usuarios[i].ra, usuarios[i].nome, usuarios[i].sobrenome, usuarios[i].disciplina);
            encontrou = 1;
        }
    }
    if (!encontrou) {
        printf("Nenhum professor cadastrado.\n");
    }
}

// Listar administradores - NOVA FUNCAO
void listarAdministradores() {
    printf("\n=== LISTA DE ADMINISTRADORES ===\n");
    int encontrou = 0;
    for (int i = 0; i < totalUsuarios; i++) {
        if (usuarios[i].tipo == 3) {
            printf("RA: %s | Nome: %s %s\n",
                   usuarios[i].ra, usuarios[i].nome, usuarios[i].sobrenome);
            encontrou = 1;
        }
    }
    if (!encontrou) {
        printf("Nenhum administrador cadastrado.\n");
    }
}

// Salvar notas em CSV
void salvarNotasCSV() {
    FILE *arquivo = fopen(ARQUIVO_NOTAS, "w");
    if (arquivo == NULL) {
        printf("Erro ao criar arquivo de notas!\n");
        return;
    }

    fprintf(arquivo, "RA_Aluno,RA_Professor,Disciplina");
    for (int i = 0; i < BIMESTRES; i++) {
        fprintf(arquivo, ",Nota_Bimestre_%d,Faltas_Bimestre_%d", i + 1, i + 1);
    }
    fprintf(arquivo, "\n");

    for (int i = 0; i < totalRegistros; i++) {
        fprintf(arquivo, "%s,%s,%s",
                registros[i].ra_aluno,
                registros[i].ra_professor,
                registros[i].disciplina);

        for (int j = 0; j < BIMESTRES; j++) {
            fprintf(arquivo, ",%.1f,%d", registros[i].notas[j], registros[i].faltas[j]);
        }
        fprintf(arquivo, "\n");
    }

    fclose(arquivo);
    printf("Dados de notas salvos em '%s'\n", ARQUIVO_NOTAS);
}

// Carregar notas do CSV
void carregarNotasCSV() {
    FILE *arquivo = fopen(ARQUIVO_NOTAS, "r");
    if (arquivo == NULL) {
        return;
    }

    char linha[512];
    int primeira_linha = 1;

    while (fgets(linha, sizeof(linha), arquivo) && totalRegistros < MAX_ALUNOS * BIMESTRES) {
        if (primeira_linha) {
            primeira_linha = 0;
            continue;
        }

        linha[strcspn(linha, "\n")] = 0;

        char *token;
        int campo = 0;

        token = strtok(linha, ",");
        while (token != NULL) {
            switch (campo) {
                case 0: strcpy(registros[totalRegistros].ra_aluno, token); break;
                case 1: strcpy(registros[totalRegistros].ra_professor, token); break;
                case 2: strcpy(registros[totalRegistros].disciplina, token); break;
                case 3: case 5: case 7: case 9:
                    registros[totalRegistros].notas[(campo-3)/2] = atof(token); break;
                case 4: case 6: case 8: case 10:
                    registros[totalRegistros].faltas[(campo-4)/2] = atoi(token); break;
            }
            token = strtok(NULL, ",");
            campo++;
        }
        totalRegistros++;
    }

    fclose(arquivo);
}

// Lancar notas e faltas - MODIFICADA: verifica se aluno esta ativo
void lancarNotasFaltas() {
    char ra_professor[TAM_RA];
    char ra_aluno[TAM_RA];
    char disciplina[TAM_DISCIPLINA];

    printf("\n=== LANCAR NOTAS E FALTAS ===\n");

    printf("Digite seu RA (professor): ");
    scanf("%6s", ra_professor);
    getchar();

    Usuario *professor = encontrarUsuarioPorRA(ra_professor);
    if (professor == NULL || professor->tipo != 2) {
        printf("ERRO: Professor nao encontrado!\n");
        return;
    }

    strcpy(disciplina, professor->disciplina);
    printf("Professor: %s %s | Disciplina: %s\n",
           professor->nome, professor->sobrenome, disciplina);

    listarAlunos(); // Mostra apenas alunos ativos

    printf("\nDigite o RA do aluno: ");
    scanf("%6s", ra_aluno);
    getchar();

    Usuario *aluno = encontrarUsuarioPorRA(ra_aluno);
    if (aluno == NULL || aluno->tipo != 1) {
        printf("ERRO: Aluno nao encontrado!\n");
        return;
    }
    
    // Verificar se aluno esta ativo
    if (aluno->ativo == 0) {
        printf("ERRO: Este aluno esta INATIVO e nao pode receber lancamentos!\n");
        return;
    }

    printf("Aluno: %s %s\n", aluno->nome, aluno->sobrenome);

    int registro_existente = -1;
    for (int i = 0; i < totalRegistros; i++) {
        if (strcmp(registros[i].ra_aluno, ra_aluno) == 0 &&
            strcmp(registros[i].ra_professor, ra_professor) == 0 &&
            strcmp(registros[i].disciplina, disciplina) == 0) {
            registro_existente = i;
            break;
        }
    }

    if (registro_existente == -1) {
        if (totalRegistros >= MAX_ALUNOS * BIMESTRES) {
            printf("Limite de registros atingido!\n");
            return;
        }
        registro_existente = totalRegistros;
        strcpy(registros[registro_existente].ra_aluno, ra_aluno);
        strcpy(registros[registro_existente].ra_professor, ra_professor);
        strcpy(registros[registro_existente].disciplina, disciplina);
        totalRegistros++;
    }

    printf("\n=== NOTAS E FALTAS DOS 4 BIMESTRES ===\n");
    for (int i = 0; i < BIMESTRES; i++) {
        printf("\n--- %do BIMESTRE ---\n", i + 1);

        // Validacao da NOTA (0-10)
        do {
            printf("Nota (0-10): ");
            scanf("%f", &registros[registro_existente].notas[i]);
            getchar();

            if (registros[registro_existente].notas[i] < 0 || registros[registro_existente].notas[i] > 10) {
                printf("ERRO: Nota deve ser entre 0 e 10! Tente novamente.\n");
            } else {
                break;
            }
        } while (1);

        // Validacao das FALTAS (nao negativas)
        do {
            printf("Faltas: ");
            scanf("%d", &registros[registro_existente].faltas[i]);
            getchar();

            if (registros[registro_existente].faltas[i] < 0) {
                printf("ERRO: Faltas nao podem ser negativas! Tente novamente.\n");
            } else {
                break;
            }
        } while (1);
    }

    printf("\nNotas e faltas lancadas com sucesso!\n");
    salvarNotasCSV();
}

// Consultar notas e faltas - MODIFICADA: verifica se aluno esta ativo
void consultarNotasFaltas() {
    char ra_aluno[TAM_RA];

    printf("\n=== CONSULTAR NOTAS E FALTAS ===\n");

    printf("Digite o RA do aluno: ");
    scanf("%6s", ra_aluno);
    getchar();

    Usuario *aluno = encontrarUsuarioPorRA(ra_aluno);
    if (aluno == NULL || aluno->tipo != 1) {
        printf("ERRO: Aluno nao encontrado!\n");
        return;
    }
    
    // Verificar se aluno esta ativo
    if (aluno->ativo == 0) {
        printf("AVISO: Este aluno esta INATIVO.\n");
    }

    printf("\nAluno: %s %s | Status: %s\n", 
           aluno->nome, aluno->sobrenome,
           aluno->ativo ? "ATIVO" : "INATIVO");

    int encontrou = 0;
    for (int i = 0; i < totalRegistros; i++) {
        if (strcmp(registros[i].ra_aluno, ra_aluno) == 0) {
            encontrou = 1;
            printf("\n--- Disciplina: %s ---\n", registros[i].disciplina);

            printf("Bimestre |   Nota  | Faltas\n");
            printf("---------|---------|--------\n");
            for (int j = 0; j < BIMESTRES; j++) {
                printf("    %d    |   %.1f   |   %d\n", j + 1, registros[i].notas[j], registros[i].faltas[j]);
            }

            float soma_notas = 0;
            int total_faltas = 0;
            for (int j = 0; j < BIMESTRES; j++) {
                soma_notas += registros[i].notas[j];
                total_faltas += registros[i].faltas[j];
            }
            printf("---------|---------|--------\n");
            printf(" Media   |   %.1f   | Total: %d\n", soma_notas / BIMESTRES, total_faltas);
        }
    }

    if (!encontrou) {
        printf("Nenhum registro encontrado para este aluno.\n");
    }
}

// ===============================
// NOVAS FUNCOES IMPLEMENTADAS
// ===============================

// Desativar aluno - NOVA FUNCAO
void desativarAluno() {
    char ra_aluno[TAM_RA];
    
    printf("\n=== DESATIVAR ALUNO ===\n");
    
    printf("Digite o RA do aluno a ser desativado: ");
    scanf("%6s", ra_aluno);
    getchar();
    
    Usuario *aluno = encontrarUsuarioPorRA(ra_aluno);
    if (aluno == NULL || aluno->tipo != 1) {
        printf("ERRO: Aluno nao encontrado!\n");
        return;
    }
    
    if (aluno->ativo == 0) {
        printf("Este aluno ja esta INATIVO.\n");
        return;
    }
    
    printf("Aluno encontrado: %s %s\n", aluno->nome, aluno->sobrenome);
    printf("Tem certeza que deseja desativar este aluno? (s/N): ");
    
    char confirmacao;
    scanf("%c", &confirmacao);
    getchar();
    
    if (confirmacao == 's' || confirmacao == 'S') {
        aluno->ativo = 0;
        salvarCSV();
        printf("Aluno desativado com sucesso!\n");
    } else {
        printf("Operacao cancelada.\n");
    }
}

// Reativar aluno - NOVA FUNCAO
void reativarAluno() {
    char ra_aluno[TAM_RA];
    
    printf("\n=== REATIVAR ALUNO ===\n");
    
    printf("Digite o RA do aluno a ser reativado: ");
    scanf("%6s", ra_aluno);
    getchar();
    
    Usuario *aluno = encontrarUsuarioPorRA(ra_aluno);
    if (aluno == NULL || aluno->tipo != 1) {
        printf("ERRO: Aluno nao encontrado!\n");
        return;
    }
    
    if (aluno->ativo == 1) {
        printf("Este aluno ja esta ATIVO.\n");
        return;
    }
    
    printf("Aluno encontrado: %s %s\n", aluno->nome, aluno->sobrenome);
    printf("Tem certeza que deseja reativar este aluno? (s/N): ");
    
    char confirmacao;
    scanf("%c", &confirmacao);
    getchar();
    
    if (confirmacao == 's' || confirmacao == 'S') {
        aluno->ativo = 1;
        salvarCSV();
        printf("Aluno reativado com sucesso!\n");
    } else {
        printf("Operacao cancelada.\n");
    }
}

// Remover usuario (professor ou admin) - NOVA FUNCAO
void removerUsuario() {
    char ra_usuario[TAM_RA];
    
    printf("\n=== REMOVER USUARIO ===\n");
    
    printf("Digite o RA do usuario a ser removido: ");
    scanf("%6s", ra_usuario);
    getchar();
    
    // Buscar usuario
    int indice = -1;
    for (int i = 0; i < totalUsuarios; i++) {
        if (strcmp(usuarios[i].ra, ra_usuario) == 0) {
            indice = i;
            break;
        }
    }
    
    if (indice == -1) {
        printf("ERRO: Usuario nao encontrado!\n");
        return;
    }
    
    // Verificar tipo (nao pode remover alunos por esta funcao)
    if (usuarios[indice].tipo == 1) {
        printf("ERRO: Use a opcao de desativar para alunos!\n");
        return;
    }
    
    printf("Usuario encontrado:\n");
    printf("RA: %s | Nome: %s %s | Tipo: %s\n",
           usuarios[indice].ra,
           usuarios[indice].nome,
           usuarios[indice].sobrenome,
           usuarios[indice].tipo == 2 ? "PROFESSOR" : "ADMINISTRADOR");
    
    printf("Tem certeza que deseja REMOVER PERMANENTEMENTE este usuario? (s/N): ");
    
    char confirmacao;
    scanf("%c", &confirmacao);
    getchar();
    
    if (confirmacao == 's' || confirmacao == 'S') {
        // Remover usuario do vetor
        for (int i = indice; i < totalUsuarios - 1; i++) {
            usuarios[i] = usuarios[i + 1];
        }
        totalUsuarios--;
        
        salvarCSV();
        printf("Usuario removido com sucesso!\n");
    } else {
        printf("Operacao cancelada.\n");
    }
}

// ===============================
// CADASTROS
// ===============================

// Cadastrar Aluno - MODIFICADA: campo 'ativo' definido como 1
void cadastrarAluno() {
    if (totalUsuarios >= MAX_USUARIOS) {
        printf("Limite maximo de usuarios atingido!\n");
        return;
    }

    Usuario novo;

    printf("\n=== CADASTRO DE ALUNO ===\n");

    gerarRA(novo.ra, 1);
    novo.tipo = 1;
    novo.ativo = 1; // NOVO: aluno cadastrado como ativo por padrao

    printf("RA gerado automaticamente: %s\n", novo.ra);

    printf("Digite o nome: ");
    fgets(novo.nome, TAM_NOME, stdin);
    novo.nome[strcspn(novo.nome, "\n")] = 0;

    printf("Digite o sobrenome: ");
    fgets(novo.sobrenome, TAM_SOBRENOME, stdin);
    novo.sobrenome[strcspn(novo.sobrenome, "\n")] = 0;

    strcpy(novo.disciplina, "");

    usuarios[totalUsuarios++] = novo;
    printf("Aluno cadastrado com sucesso! (Status: ATIVO)\n");

    salvarCSV();
}

// Cadastrar Professor - MODIFICADA: campo 'ativo' definido como 1
void cadastrarProfessor() {
    if (totalUsuarios >= MAX_USUARIOS) {
        printf("Limite maximo de usuarios atingido!\n");
        return;
    }

    Usuario novo;

    printf("\n=== CADASTRO DE PROFESSOR ===\n");

    gerarRA(novo.ra, 2);
    novo.tipo = 2;
    novo.ativo = 1; // NOVO: professor ativo por padrao

    printf("RA gerado automaticamente: %s\n", novo.ra);

    printf("Digite o nome: ");
    fgets(novo.nome, TAM_NOME, stdin);
    novo.nome[strcspn(novo.nome, "\n")] = 0;

    printf("Digite o sobrenome: ");
    fgets(novo.sobrenome, TAM_SOBRENOME, stdin);
    novo.sobrenome[strcspn(novo.sobrenome, "\n")] = 0;

    escolherDisciplina(novo.disciplina);

    usuarios[totalUsuarios++] = novo;
    printf("Professor cadastrado com sucesso!\n");
    printf("Disciplina: %s\n", novo.disciplina);

    salvarCSV();
}

// Cadastrar Admin - MODIFICADA: campo 'ativo' definido como 1
void cadastrarAdmin() {
    if (totalUsuarios >= MAX_USUARIOS) {
        printf("Limite maximo de usuarios atingido!\n");
        return;
    }

    Usuario novo;

    printf("\n=== CADASTRO DE ADMINISTRADOR ===\n");

    gerarRA(novo.ra, 3);
    novo.tipo = 3;
    strcpy(novo.disciplina, "N/A");
    novo.ativo = 1; // NOVO: admin ativo por padrao

    printf("RA gerado automaticamente: %s\n", novo.ra);

    printf("Digite o nome: ");
    fgets(novo.nome, TAM_NOME, stdin);
    novo.nome[strcspn(novo.nome, "\n")] = 0;

    printf("Digite o sobrenome: ");
    fgets(novo.sobrenome, TAM_SOBRENOME, stdin);
    novo.sobrenome[strcspn(novo.sobrenome, "\n")] = 0;

    usuarios[totalUsuarios++] = novo;
    printf("Administrador cadastrado com sucesso!\n");

    salvarCSV();
}

// ===============================
// MENUS
// ===============================

// Menu do Professor - MODIFICADA: opcao de listar alunos inativos adicionada
void menuProfessor() {
    int opcao;

    do {
        printf("\n=== MENU PROFESSOR ===\n");
        printf("1. Lancar notas e faltas\n");
        printf("2. Consultar notas e faltas\n");
        printf("3. Listar alunos ativos\n");
        printf("4. Listar alunos inativos\n"); // NOVA OPCAO
        printf("5. Desativar aluno\n");
        printf("6. Listar todos os alunos (ativos e inativos)\n");
        printf("0. Voltar\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1: lancarNotasFaltas(); break;
            case 2: consultarNotasFaltas(); break;
            case 3: listarAlunos(); break;
            case 4: listarAlunosInativos(); break; // NOVA OPCAO
            case 5: desativarAluno(); break;
            case 6: listarTodosAlunos(); break;
            case 0: printf("Voltando...\n"); break;
            default: printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}

// Menu do Admin (PROTEGIDO POR SENHA) - MODIFICADA: opcoes completas de gerenciamento de alunos
void menuAdmin() {
    // Verifica senha primeiro
    if (!verificarSenhaAdmin()) {
        printf("Acesso ao menu administrativo negado.\n");
        return;
    }

    int opcao;

    do {
        printf("\n=== MENU ADMINISTRADOR ===\n");
        printf("1. Cadastrar Professor\n");
        printf("2. Cadastrar Administrador\n");
        printf("3. Listar alunos ativos\n");
        printf("4. Listar alunos inativos\n"); // NOVA OPCAO
        printf("5. Listar professores\n");
        printf("6. Listar administradores\n");
        printf("7. Remover professor/administrador\n");
        printf("8. Listar todos os alunos (ativos e inativos)\n");
        printf("9. Desativar aluno\n"); // NOVA OPCAO
        printf("10. Reativar aluno\n");
        printf("0. Voltar\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1: cadastrarProfessor(); break;
            case 2: cadastrarAdmin(); break;
            case 3: listarAlunos(); break;
            case 4: listarAlunosInativos(); break; // NOVA OPCAO
            case 5: listarProfessores(); break;
            case 6: listarAdministradores(); break;
            case 7: removerUsuario(); break;
            case 8: listarTodosAlunos(); break;
            case 9: desativarAluno(); break; // NOVA OPCAO
            case 10: reativarAluno(); break;
            case 0: printf("Voltando ao menu principal...\n"); break;
            default: printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}

// Menu principal
void menuPrincipal() {
    int opcao;

    carregarCSV();
    carregarNotasCSV();

    do {
        printf("\n=== Sistema de Gestão Academica (SiGA) ===\n");
        printf("1. Cadastrar Aluno\n");
        printf("2. Menu Professor\n");
        printf("3. Menu Administrador\n");
        printf("0. Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1: cadastrarAluno(); break;
            case 2: menuProfessor(); break;
            case 3: menuAdmin(); break;
            case 0: printf("Saindo do sistema...\n"); break;
            default: printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}

// ===============================
// MAIN
// ===============================

int main() {
    printf("=== Sistema de Gestao Academica (SiGA) ===\n");
    printf("RA automatico: ALUN##, PROF##, ADM###\n");
    printf("Disciplinas: Matematica, Portugues, Ciencias, Geografia\n");
    printf("Novo: Sistema de status ativo/inativo para alunos\n");

    menuPrincipal();

    return 0;
}