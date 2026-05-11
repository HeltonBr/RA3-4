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

## Checkpoint 6 - Relatorio de execucao e conformidade

- `teste1.txt`, `teste2.txt` e `teste3.txt` publicados tambem na raiz do codigo-fonte.
- CLI passou a imprimir relatorio de validacao com lexico, sintatico, semantico, cobertura detectada e status do Assembly.
- Arvore sintatica pode ser exibida por `--mostrar-arvore` ou `--relatorio-completo`.
- Assembly permanece apenas em arquivo, com confirmacao de geracao ou bloqueio no console.

## Checkpoint 7 - Matriz e cobertura dos testes

- `teste1.txt`, `teste2.txt` e `teste3.txt` ampliados para cobrir todos os operadores aritmeticos, relacionais e logicos.
- Os tres programas validos passaram a cobrir `IF`, `IFELSE`, `WHILE`, `SEQ`, `RES`, leitura/escrita de memoria e todos os tipos.
- `teste4_semantico_invalido.txt` adicionado na raiz para erros semanticos intencionais com lexico e sintaxe validos.
- `docs/matriz_cobertura_requisitos.md` criada para rastrear requisitos, evidencias e testes automatizados.
