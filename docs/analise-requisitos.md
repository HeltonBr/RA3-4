# Analise dos Requisitos - Fase 3

## Pipeline

- Ler arquivo-fonte por argumento de linha de comando.
- Executar lexico, parser LL(1), analise semantica, arvore atribuida e Assembly.
- Aceitar tokens serializados apenas como compatibilidade com fases anteriores.

## Linguagem

- Programa entre `(START)` e `(END)`.
- Comentarios `*{ ... }*`.
- Expressoes RPN aninhadas.
- Operadores aritmeticos, relacionais e logicos.
- Tipos `int`, `real` e `bool`.
- Comandos `(V MEM)`, `(MEM)` e `(N RES)`.
- Controle por `IF`, `IFELSE`, `WHILE` e `SEQ`.

## Entregaveis

- Codigo Python com funcoes exigidas.
- Tres arquivos validos e varios invalidos.
- README completo.
- Gramatica atribuida em EBNF.
- Regras de tipos em calculo de sequentes.
- Tabela de simbolos.
- Arvore sintatica atribuida.
- Relatorio de erros semanticos.
- Assembly ARMv7 da ultima execucao valida.

## Decisoes de risco

As ambiguidades do enunciado estao tratadas em `docs/decisoes_inconformidades_fase3.md`. A regra central e: programas invalidos semanticamente nao geram Assembly executavel.
