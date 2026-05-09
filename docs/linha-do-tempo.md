# Linha do Tempo - Fase 3

## Checkpoint 1 - Migracao da base

- Base Python da fase anterior copiada para o workspace.
- Historico Git antigo nao foi importado.
- Ponto de entrada `AnalisadorSemantico.py` criado.

## Checkpoint 2 - Inconformidades

- Dossie analisado.
- Decisoes registradas em `docs/decisoes_inconformidades_fase3.md`.
- Regras controversas formalizadas: `RES`, comentarios, bool, reatribuicao e bloqueio de Assembly.

## Checkpoint 3 - Implementacao semantica

- Lexer adaptado para comentarios `*{ ... }*`.
- Literais `TRUE`/`FALSE` e operadores `AND`/`OR`/`NOT` adicionados.
- Tabela de simbolos implementada.
- Sistema de tipos implementado.
- Arvore sintatica atribuida implementada.

## Checkpoint 4 - Testes e artefatos

- Tres arquivos validos atualizados para Fase 3.
- Casos invalidos lexicos, sintaticos e semanticos adicionados.
- Suite local executada com 28 testes aprovados.
- Artefatos finais regenerados com:

```powershell
python AnalisadorSemantico.py tests/teste3.txt
```

## Checkpoint 5 - Entrada e comentarios

- Cobertura reforcada para comentario multilinha valido entre declaracoes.
- Caso invalido explicito para palavra reservada usada como nome de memoria.
- README e checklist atualizados para remover pendencia administrativa ja superada.
