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
- A arvore sintatica passou a ser desenhada por padrao no console para todo programa valido que gera Assembly.

## Checkpoint 8 - Planejamento de pre-auditoria

- PR 04 integrado na `main`, atualizando a pagina principal do GitHub com README e arquivos oficiais na raiz.
- Cronograma replanejado apos a cobertura central ja implementada, evitando etapas duplicadas.
- Dossie de inconformidades relido e convertido em quadro de auditoria com decisoes, evidencias e perguntas ao professor.
- Proximas etapas reorganizadas para auditoria gramatical, semantica, Assembly, entradas externas, documentacao de defesa e pre-auditoria final.
- Semana pesada de testes mantida de 19/05/2026 a 25/05/2026, sem novas features e com foco em regressao, evidencias e congelamento.

## Checkpoint 9 - Auditoria gramatical

- Gramatica LL(1), FIRST/FOLLOW e tabela LL(1) auditados em documento proprio.
- Testes adicionados para recuperacao sintatica, expressoes vazias, declaracoes malformadas, `START`/`END` e comentarios sem regex.
- PR 06 integrado na `main` antes do inicio da auditoria semantica.

## Checkpoint 10 - Auditoria semantica e tipos

- Matriz de tipos reforcada para aritmetica, relacionais, logicos, controle, reatribuicao e `RES`.
- Dossie atualizado com orientacoes do professor: `//` aceito como divisao inteira e `0` aceito como inteiro positivo em potenciacao.
- PR 07 integrado na `main` em 15/05/2026 com suite completa aprovada.

## Checkpoint 11 - Assembly e CPulator

- Auditoria especifica criada em `docs/auditoria_assembly_cpulator_fase3.md`.
- Testes confirmam que programas validos geram Assembly ARMv7 com `_start`, JTAG UART e rotinas de runtime.
- Testes confirmam que programa invalido bloqueia Assembly executavel e grava marcador textual em `generated/ultimo_assembly.s`.
