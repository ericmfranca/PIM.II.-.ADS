#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

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

// Estrutura para notas e faltas
typedef struct {
    float notas[BIMESTRES];     // Notas dos 4 bimestres
    int faltas[BIMESTRES];      // Faltas por bimestre
    char disciplina[TAM_DISCIPLINA]; // Disciplina relacionada
    char ra_aluno[TAM_RA];      // RA do aluno
    char ra_professor[TAM_RA];  // RA do professor que lan�ou
} NotasFaltas;

// Estrutura do usu�rio
typedef struct {
    char ra[TAM_RA];
    char nome[TAM_NOME];
    char sobrenome[TAM_SOBRENOME];
    char disciplina[TAM_DISCIPLINA];
    int tipo; // 1=Aluno, 2=Professor, 3=Admin
} Usuario;

// Vari�veis globais
Usuario usuarios[MAX_USUARIOS];
NotasFaltas registros[MAX_ALUNOS * BIMESTRES];
int totalUsuarios = 0;
int totalRegistros = 0;

// Disciplinas dispon�veis
const char *disciplinas[] = {
    "Matematica",
    "Portugues",
    "Ciencias",
    "Geografia"
};
const int total_disciplinas = 4;

// ===============================
// FUN��ES PRINCIPAIS
// ===============================

// Gera RA autom�tico
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

// Salvar usu�rios em CSV
void salvarCSV() {
    FILE *arquivo = fopen(ARQUIVO_CSV, "w");
    if (arquivo == NULL) {
        printf("Erro ao criar arquivo CSV!\n");
        return;
    }

    fprintf(arquivo, "RA,Nome,Sobrenome,Tipo,Disciplina\n");

    for (int i = 0; i < totalUsuarios; i++) {
        fprintf(arquivo, "%s,%s,%s,%d,%s\n",
                usuarios[i].ra,
                usuarios[i].nome,
                usuarios[i].sobrenome,
                usuarios[i].tipo,
                usuarios[i].disciplina);
    }

    fclose(arquivo);
    printf("Dados salvos em '%s'\n", ARQUIVO_CSV);
}

// Carregar usu�rios do CSV
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
        while (token != NULL && campo < 5) {
            switch (campo) {
                case 0: strcpy(usuarios[totalUsuarios].ra, token); break;
                case 1: strcpy(usuarios[totalUsuarios].nome, token); break;
                case 2: strcpy(usuarios[totalUsuarios].sobrenome, token); break;
                case 3: usuarios[totalUsuarios].tipo = atoi(token); break;
                case 4: strcpy(usuarios[totalUsuarios].disciplina, token); break;
            }
            token = strtok(NULL, ",");
            campo++;
        }
        totalUsuarios++;
    }

    fclose(arquivo);
}

// Encontrar usu�rio por RA
Usuario* encontrarUsuarioPorRA(const char *ra) {
    for (int i = 0; i < totalUsuarios; i++) {
        if (strcmp(usuarios[i].ra, ra) == 0) {
            return &usuarios[i];
        }
    }
    return NULL;
}

// Listar alunos
void listarAlunos() {
    printf("\n=== LISTA DE ALUNOS ===\n");
    int encontrou = 0;
    for (int i = 0; i < totalUsuarios; i++) {
        if (usuarios[i].tipo == 1) {
            printf("RA: %s | Nome: %s %s\n",
                   usuarios[i].ra, usuarios[i].nome, usuarios[i].sobrenome);
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

// Lan�ar notas e faltas
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

    listarAlunos();

    printf("\nDigite o RA do aluno: ");
    scanf("%6s", ra_aluno);
    getchar();

    Usuario *aluno = encontrarUsuarioPorRA(ra_aluno);
    if (aluno == NULL || aluno->tipo != 1) {
        printf("ERRO: Aluno nao encontrado!\n");
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

        // Valida��o da NOTA (0-10)
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

        // Valida��o das FALTAS (n�o negativas)
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

// Consultar notas e faltas
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

    printf("\nAluno: %s %s\n", aluno->nome, aluno->sobrenome);

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
// CADASTROS
// ===============================

// Cadastrar Aluno
void cadastrarAluno() {
    if (totalUsuarios >= MAX_USUARIOS) {
        printf("Limite maximo de usuarios atingido!\n");
        return;
    }

    Usuario novo;

    printf("\n=== CADASTRO DE ALUNO ===\n");

    gerarRA(novo.ra, 1);
    novo.tipo = 1;

    printf("RA gerado automaticamente: %s\n", novo.ra);

    printf("Digite o nome: ");
    fgets(novo.nome, TAM_NOME, stdin);
    novo.nome[strcspn(novo.nome, "\n")] = 0;

    printf("Digite o sobrenome: ");
    fgets(novo.sobrenome, TAM_SOBRENOME, stdin);
    novo.sobrenome[strcspn(novo.sobrenome, "\n")] = 0;

    strcpy(novo.disciplina, "");

    usuarios[totalUsuarios++] = novo;
    printf("Aluno cadastrado com sucesso!\n");

    salvarCSV();
}

// Cadastrar Professor
void cadastrarProfessor() {
    if (totalUsuarios >= MAX_USUARIOS) {
        printf("Limite maximo de usuarios atingido!\n");
        return;
    }

    Usuario novo;

    printf("\n=== CADASTRO DE PROFESSOR ===\n");

    gerarRA(novo.ra, 2);
    novo.tipo = 2;

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

// Cadastrar Admin
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

// Menu do Professor
void menuProfessor() {
    int opcao;

    do {
        printf("\n=== MENU PROFESSOR ===\n");
        printf("1. Lancar notas e faltas\n");
        printf("2. Consultar notas e faltas\n");
        printf("3. Listar alunos\n");
        printf("0. Voltar\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1: lancarNotasFaltas(); break;
            case 2: consultarNotasFaltas(); break;
            case 3: listarAlunos(); break;
            case 0: printf("Voltando...\n"); break;
            default: printf("Opcao invalida!\n");
        }
    } while (opcao != 0);
}

// Menu do Admin
void menuAdmin() {
    int opcao;

    do {
        printf("\n=== MENU ADMINISTRADOR ===\n");
        printf("1. Cadastrar Professor\n");
        printf("2. Cadastrar Administrador\n");
        printf("3. Listar alunos\n");
        printf("4. Listar professores\n");
        printf("0. Voltar\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1: cadastrarProfessor(); break;
            case 2: cadastrarAdmin(); break;
            case 3: listarAlunos(); break;
            case 4: listarProfessores(); break;
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
        printf("\n=== SISTEMA ACADEMICO ===\n");
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
    printf("=== SISTEMA DE GESTAO ACADEMICA ===\n");
    printf("RA automatico: ALUN##, PROF##, ADM###\n");
    printf("Disciplinas: Matematica, Portugues, Ciencias, Geografia\n");

    menuPrincipal();

    return 0;
}