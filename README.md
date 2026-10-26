# Script-GEEKIE

Automação em Python + Selenium para manter as contas dos alunos em dia no Geekie One: cria contas, coloca cada aluno na turma certa, ativa o material da série e, no fim, confere tudo e gera uma planilha de auditoria.

A entrada é a planilha de matrículas da escola. O script percorre as linhas, faz o trabalho no navegador e registra o que deu certo e o que ficou pendente, para que só as pendências precisem de outra passada.

## O que ele faz

- cria as contas que ainda não existem e corrige as que estão na turma errada;
- ativa o material da série do aluno;
- audita login, senha e turma de cada linha e gera `auditoria_geekie_resultado.xlsx`;
- reprocessa só as linhas que a auditoria marcou como pendentes.

## Como rodar

Requisitos: Windows, Python 3 e Google Chrome.

```bat
pip install -r requirements.txt
copy config.example.bat config.local.bat
geekie.bat
```

Em `config.local.bat`, preencha `GEEKIE_EMAIL_TAG` com o sufixo que a escola usa nos e-mails dos alunos (`nome.sobrenome-TAG@dominio`). A senha padrão das contas não fica no repositório: ou ela vai em `config.local.bat`, que o git ignora, ou o `geekie.bat` pergunta ao iniciar.

Depois é escolher a operação, a planilha, a aba e a linha inicial (normalmente `2`). Se o Geekie pedir login, entre pela janela do Chrome que a automação abriu e volte ao terminal.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `geekie.bat` | ponto de entrada; carrega a configuração e mostra o menu |
| `menu_geekie.py` | escolhe planilha, aba e linha inicial |
| `geekie_automation.py` | criação de contas, troca de turma e ativação de material |
| `auditoria_geekie.py` | confere cada aluno e gera o relatório |
| `corrigir_pendentes.py` | reprocessa o que a auditoria apontou |
| `fechar_chrome_automacao.ps1` | fecha o Chrome da automação quando ele trava e remove o lockfile |

## Dados dos alunos

Planilhas, relatórios, CSVs e o perfil do Chrome ficam só na máquina local e estão no `.gitignore`. Nenhum dado de aluno vai para o repositório.
