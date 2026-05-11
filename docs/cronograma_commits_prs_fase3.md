# Cronograma Escalonado de Commits e Pull Requests - Fase 3

Data final de congelamento: **25/05/2026 as 23:59**. A pasta principal local e o repositorio GitHub devem ficar congelados a partir desse horario.

Janela de desenvolvimento com commits e PRs diarios: **09/05/2026 a 18/05/2026**.  
Janela de auditoria pesada e congelamento: **19/05/2026 a 25/05/2026**.

Este planejamento foi atualizado em **11/05/2026**, apos o merge do **PR 04 - Cobertura e matriz de testes** na `main`. A implementacao central ja cobre entrada, parser LL(1), semantica, relatorio de execucao, arquivos oficiais na raiz, arvore sintatica desenhada, diagnosticos acumulados e matriz de requisitos. As proximas etapas devem priorizar endurecimento, evidencias e reducao de risco.

## Estado consolidado ate 11/05/2026

| Data | Marco | Branch/PR | Resultado |
| --- | --- | --- | --- |
| 09/05/2026 | Planejamento e congelamento | PR 01 | Cronograma, espelho e documentos de apoio criados. |
| 10/05/2026 | Entrada e comentarios | PR 02 | Comentarios, palavras reservadas e variacoes de formato reforcadas. |
| 10/05/2026 | Relatorio de execucao | PR 03 | CLI passou a relatar fases, cobertura detectada e status do Assembly. |
| 11/05/2026 | Cobertura e matriz de testes | PR 04 | Arquivos oficiais na raiz, cobertura completa dos validos, arvore desenhada por padrao, diagnosticos estruturados e README de entrega atualizados. |

## Regra operacional

- Cada dia de desenvolvimento deve ter uma branch curta, commits claros e um pull request.
- A branch `main` so recebe merge apos testes locais, validacao manual e sincronizacao para `GitHubmirror`.
- A pasta `GitHubmirror` deve ser sincronizada todos os dias apos o merge do PR diario.
- A partir de **19/05/2026**, nao entram features novas: apenas testes, evidencias e correcoes pontuais comprovadas.
- Ao final de cada etapa, os artefatos devem ser regenerados com um programa valido canonico, preferencialmente `teste3.txt`.

## Plano atualizado ate a pre-auditoria

| Data | Branch sugerida | Objetivo tecnico | Commit principal sugerido | Pull request sugerido | Criterio de aceite |
| --- | --- | --- | --- | --- | --- |
| 12/05/2026 | `feature/05-planejamento-pre-auditoria` | Ajustar cronograma pos-PR 04, checklist e roteiro de validacao ate a semana de testes. | `docs: atualiza planejamento pre-auditoria` | PR 05 - Planejamento pre-auditoria | Cronograma refletindo o estado real da `main`, sem etapas ja superadas. |
| 13/05/2026 | `feature/06-auditoria-gramatica-parser` | Auditar gramatica LL(1), FIRST/FOLLOW, tabela LL(1), recuperacao sintatica e mensagens de erro. | `test: reforca auditoria da gramatica ll1` | PR 06 - Auditoria gramatical | Casos de `START`, `END`, expressoes vazias, linhas malformadas, reservadas e aninhamento validados. |
| 14/05/2026 | `feature/07-auditoria-semantica-tipos` | Expandir testes de tipos para todas as combinacoes relevantes de aritmetica, relacionais, logicos, controle, `RES` e reatribuicao. | `test: amplia matriz semantica de tipos` | PR 07 - Auditoria semantica | Mensagens com tipo, linha, coluna e detalhe; arquivo inteiro varrido sem parar no primeiro erro. |
| 15/05/2026 | `feature/08-auditoria-assembly-cpulator` | Revisar geracao ARMv7, bloqueio de Assembly em invalidos, artefatos gerados e roteiro CPulator. | `test: audita assembly e artefatos` | PR 08 - Assembly e artefatos | Validos geram Assembly, invalidos bloqueiam, `generated/ultimo_assembly.s` fica canonico e documentado. |
| 16/05/2026 | `feature/09-robustez-entradas-professor` | Simular entradas diferentes das entregues, como na prova de autoria: formatos variados, nomes novos, comentarios e erros mistos. | `test: adiciona cenarios de autoria externos` | PR 09 - Robustez para autoria | Testes mostram generalizacao alem dos quatro arquivos oficiais. |
| 17/05/2026 | `feature/10-documentacao-defesa-final` | Revisar README, sequentes, decisoes do dossie, matriz de cobertura e roteiro de demonstracao. | `docs: fecha documentacao de defesa` | PR 10 - Documentacao de defesa | Documentos sem combinados internos e coerentes com o comportamento real do CLI. |
| 18/05/2026 | `release/11-pre-auditoria-final` | Rodar suite completa, validar manualmente arquivos oficiais, regenerar artefatos e fechar congelamento de features. | `chore: prepara pre-auditoria final` | PR 11 - Pre-auditoria final | Suite completa OK, README conferido na `main`, `GitHubmirror` sincronizado e nenhuma feature pendente. |

## Semana pesada de testes

| Data | Foco | Saida esperada |
| --- | --- | --- |
| 19/05/2026 | Regressao completa | Suite `unittest` OK; `teste1.txt`, `teste2.txt`, `teste3.txt` gerando Assembly; `teste4_semantico_invalido.txt` bloqueando Assembly. |
| 20/05/2026 | Lexico e comentarios | Comentarios em linha inteira, fim de linha, entre tokens, multilinha e nao fechados verificados com linha/coluna. |
| 21/05/2026 | Parser LL(1) | Gramatica, FIRST/FOLLOW, tabela LL(1), recuperacao de erro e mensagens sintaticas revisadas. |
| 22/05/2026 | Semantica e tipos | Variaveis, reatribuicao, `RES`, operadores, controle e acumulacao de erros auditados. |
| 23/05/2026 | Entradas externas | Arquivos novos simulando prova do professor processados, com validos e invalidos nao copiados da suite. |
| 24/05/2026 | Assembly e CPulator | `generated/ultimo_assembly.s` revisado e executado no CPulator ARMv7 DE1-SoC. |
| 25/05/2026 | Auditoria final | README, arquivos oficiais na raiz, docs, GitHub, `GitHubmirror`, suite completa e congelamento as 23:59. |

## Padrao diario de trabalho

1. Criar branch do dia.
2. Implementar somente o escopo da etapa.
3. Rodar testes direcionados.
4. Atualizar docs e artefatos se a etapa alterar comportamento.
5. Fazer commit com mensagem clara.
6. Abrir PR do dia.
7. Rodar suite completa antes do merge.
8. Fazer merge na `main`.
9. Sincronizar `GitHubmirror`.
10. Registrar resultado no PR ou em `docs/linha-do-tempo.md`.

## Comandos canonicos

```powershell
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste3.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python -m unittest discover -s tests -p "test_*.py" -v
.\sincronizar_para_githubmirror.ps1
```
