# Auditoria Gramatical e Sintatica - Fase 3

Esta auditoria registra a situacao final da gramatica LL(1) usada pela entrega.

## Pontos verificados

| Item | Evidencia |
| --- | --- |
| Programa completo delimitado por `(START)` e `(END)` | `docs/gramatica_atribuida.md`, `docs/first_follow.md`, `docs/tabela_ll1.md` |
| Operadores aritmeticos, relacionais, logicos, memoria, `RES` e controle | `teste1.txt`, `teste2.txt`, `teste3.txt` |
| Arquivo invalido oficial reconhecido sintaticamente antes da analise semantica | `teste4_semantico_invalido.txt` |
| Arvore sintatica desenhada no console para programas validos | Execucao de `python AnalisadorSemantico.py teste3.txt` |
| Comentarios descartados pelo lexico sem interferir na AST | Arquivos validos oficiais e relatorio de execucao |

## Decisao

A sintaxe de controle permanece pos-fixada: `IF`, `IFELSE`, `WHILE` e `SEQ` aparecem ao final das respectivas expressoes ou comandos. A validacao publica usa apenas os arquivos oficiais da raiz.
