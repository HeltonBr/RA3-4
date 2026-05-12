# Auditoria Gramatical e Sintatica - Fase 3

## Escopo

Esta auditoria corresponde ao PR 06 planejado para a Fase 3. O objetivo e verificar se a gramatica LL(1), os conjuntos FIRST/FOLLOW, a tabela preditiva, o parser e a recuperacao de diagnosticos sintaticos permanecem coerentes com os requisitos do projeto e com o dossie de inconformidades.

## Pontos auditados nesta primeira rodada

| Ponto | Tratamento adotado | Evidencia |
| --- | --- | --- |
| Gramatica LL(1) aumentada | A gramatica canonica continua centralizada em `construirGramatica()` e gera FIRST, FOLLOW e tabela LL(1). | `src/analisador_sintatico_ll1/grammar.py`, `docs/gramatica.md`, `docs/first_follow.md`, `docs/tabela_ll1.md` |
| Tokens criticos da Fase 3 | `START`, `END`, `RES`, `SEQ`, `IF`, `IFELSE`, `WHILE`, booleanos e operadores logicos/relacionais aparecem na tabela LL(1). | `tests/test_auditoria_gramatica_parser.py` |
| Recuperacao sintatica por arquivo | O CLI acumula erros sintaticos estruturais em linhas diferentes, sem encerrar no primeiro problema. | `test_cli_acumula_erros_sintaticos_estruturais_sem_interromper` |
| Comentarios sem regex no inventario | O reconhecimento lexico ja era caractere a caractere; agora o inventario do relatorio tambem usa varredura manual. | `src/analisador_sintatico_ll1/main.py`, `test_inventario_de_comentarios_nao_depende_de_regex` |

## Riscos do dossie tratados aqui

- **INC-01 e INC-02:** tokens novos da Fase 3 e convencoes de booleanos/logicos continuam refletidos na gramatica e tabela LL(1).
- **INC-06:** formas canonicas de controle permanecem pos-fixadas e documentadas em `docs/sintaxe_controle.md`.
- **INC-10:** FIRST/FOLLOW e tabela LL(1) sao gerados e testados contra pontos criticos.
- **INC-12 e INC-20:** comentarios `*{ ... }*` sao processados sem regex no lexico e sem regex no inventario do relatorio.
- **INC-18:** a entrada principal continua aceitando fonte bruto, alem de tokens serializados herdados da Fase 1.

## Pendencias ainda abertas para o PR 06

- Ampliar testes com entradas validas de aninhamento profundo e variacoes sintaticas fora dos quatro arquivos oficiais.
- Conferir se todos os casos de `START`/`END` duplicados, ausentes ou fora de posicao possuem mensagens suficientemente claras.
- Revisar se a tabela LL(1) documentada e regenerada apos cada execucao canonica permanece identica ao comportamento do parser.
- Registrar no fechamento do PR 06 uma matriz curta ligando cada risco gramatical do dossie ao teste correspondente.

