# Automação Geekie

Kit privado de automação para rotinas administrativas no Geekie One, incluindo correção de turmas, criação de contas e auditoria de alunos.

## Funcionalidades

- correção de turma e ativação de material;
- criação e ajuste de contas;
- auditoria de login, senha e turma;
- correção dos registros pendentes;
- seleção interativa de planilha, aba e linha inicial;
- geração de resultados de auditoria.

## Arquivos principais

| Arquivo | Finalidade |
| --- | --- |
| `geekie.bat` | inicia o menu principal |
| `menu_geekie.py` | seleciona planilha, aba e operação |
| `geekie_automation.py` | executa correções e criação de contas |
| `auditoria_geekie.py` | audita os dados dos alunos |
| `corrigir_pendentes.py` | tenta corrigir pendências encontradas |

## Como usar

1. mantenha os arquivos `.xlsx` de trabalho apenas na pasta local;
2. execute `geekie.bat`;
3. escolha a operação;
4. selecione a planilha e a aba;
5. confirme a linha inicial — normalmente `2`;
6. acompanhe o processamento pelo terminal.

Ao iniciar, o `geekie.bat` pergunta qual senha padrao deve ser usada naquela execucao.

Se o Geekie solicitar autenticação, faça login na janela do Chrome aberta pela automação e retorne ao terminal.

## Dados locais

Os seguintes itens não devem ser enviados ao GitHub:

- planilhas com dados de alunos;
- perfis do Chrome e sessões autenticadas;
- resultados de auditoria;
- arquivos antigos ou temporários;
- senhas e credenciais.

Esses caminhos estão cobertos pelo `.gitignore`. Não documente senhas reais ou padrão no repositório.

## Requisitos

- Windows;
- Python 3;
- Google Chrome;
- dependências Python utilizadas pelos scripts.

> Repositório privado com finalidade administrativa. Revise os dados antes de compartilhar arquivos ou conceder acesso.
