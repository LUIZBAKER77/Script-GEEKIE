# Automacao Geekie

Esta pasta e o kit para repetir o processo em outras turmas/planilhas.

## Como usar

Abra o arquivo:

```bat
geekie.bat
```

O menu pergunta primeiro o que voce quer fazer:

1. Corrigir turma / criar contas
2. Auditar alunos
3. Corrigir pendentes da auditoria

Depois ele mostra as planilhas `.xlsx` que estao nesta pasta, detecta as abas de anos/series da planilha escolhida e pergunta qual aba voce quer usar.

Tambem pergunta a linha inicial. Normalmente deixe `2`.

## Arquivos principais

- `geekie.bat`: menu principal.
- `menu_geekie.py`: detecta planilhas/abas e chama o script certo.
- `geekie_automation.py`: corrige turma, ativa material e cria/ajusta contas.
- `auditoria_geekie.py`: audita login, senha e turma.
- `corrigir_pendentes.py`: tenta corrigir os erros encontrados na auditoria.
- `Códigos para o Geekie Teste.xlsx`: planilha local atual.
- `chrome_profile`: perfil usado pelo Chrome do script. Nao apague se quiser manter login.
- `resultados`: onde ficam os arquivos de auditoria gerados.
- `arquivo_antigo`: tentativas antigas e arquivos temporarios.

## Observacoes

- Se trocar a planilha, coloque o novo `.xlsx` nesta pasta.
- Se pedir login, faca login na janela do Chrome aberta pelo script e pressione Enter no terminal.
- A senha padrao usada pelo script e `REMOVIDO`.
- Os scripts salvam a planilha original depois de cada aluno concluido.
