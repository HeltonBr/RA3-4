# Cronograma Escalonado de Commits e Pull Requests - Fase 3

Data final de congelamento: **25/05/2026 as 23:59**. A pasta principal local e o repositorio GitHub devem ficar congelados a partir desse horario.

Janela de desenvolvimento com commits e PRs diarios: **09/05/2026 a 18/05/2026**.  
Janela de auditoria pesada e congelamento: **19/05/2026 a 25/05/2026**.

## Regra operacional

- Cada dia de desenvolvimento deve ter uma branch curta, commits claros e um pull request.
- O PR diario deve ser aberto mesmo em grupo individual, para registrar evolucao e autoria.
- A branch `main` so recebe merge apos testes locais e espelhamento para `GitHubmirror`.
- A pasta `GitHubmirror` deve ser sincronizada todos os dias apos o merge do PR diario.
- A partir de **19/05/2026**, nao entram features novas: apenas testes, evidencias e correcoes pontuais comprovadas.

## Plano diario de evolucao

| Data | Branch sugerida | Objetivo tecnico | Commit principal sugerido | Pull request sugerido | Criterio de aceite |
| --- | --- | --- | --- | --- | --- |
| 09/05/2026 | `feature/01-planejamento-fase3` | Formalizar data final, cronograma, espelho e riscos do dossie. | `docs: define cronograma escalonado da fase 3` | PR 01 - Planejamento e congelamento | Docs revisados e script de espelho criado. |
| 10/05/2026 | `feature/02-entrada-comentarios` | Consolidar lexico com comentarios e palavras reservadas. | `feat: consolida entrada semantica e comentarios` | PR 02 - Entrada e comentarios | Comentarios em linha inteira, fim de linha e entre tokens testados. |
| 10/05/2026 | `feature/03-relatorio-execucao-entrega` | Adiantar conformidade de execucao, testes na raiz e relatorio de validacao. | `feat: adiciona relatorio de validacao do cli` | PR 03 - Relatorio de execucao | CLI resume fases, cobertura e arvore opcional; Assembly fica apenas em arquivo. |
| 11/05/2026 | `feature/04-gramatica-bool-logicos` | Fechar gramatica LL(1) com bool e operadores logicos. | `feat: adiciona bool e operadores logicos a gramatica` | PR 04 - Gramatica aumentada | `docs/gramatica_atribuida.md`, FIRST/FOLLOW e tabela LL(1) atualizados. |
| 12/05/2026 | `feature/05-tabela-simbolos` | Fortalecer tabela de simbolos, definicoes, usos e reatribuicoes. | `feat: implementa tabela de simbolos semantica` | PR 05 - Tabela de simbolos | Uso antes da definicao e troca de tipo rejeitados. |
| 13/05/2026 | `feature/06-verificacao-tipos` | Ampliar verificacao de tipos para aritmetica, relacionais, logicos e controle. | `feat: valida regras de tipos da fase 3` | PR 06 - Sistema de tipos | Matriz de compatibilidade testada com validos e invalidos. |
| 14/05/2026 | `feature/07-arvore-atribuida` | Gerar arvore sintatica atribuida com tipo, status e referencias de simbolo. | `feat: gera arvore sintatica atribuida` | PR 07 - Arvore atribuida | JSON e Markdown da arvore atribuida conferidos. |
| 15/05/2026 | `feature/08-assembly-semantico` | Garantir que Assembly seja gerado apenas a partir de arvore atribuida valida. | `feat: bloqueia assembly em programas invalidos` | PR 08 - Assembly semantico | Assembly gerado para validos e bloqueado para invalidos. |
| 16/05/2026 | `feature/09-testes-obrigatorios` | Completar tres testes validos e suite de invalidos lexicos, sintaticos e semanticos. | `test: amplia cobertura obrigatoria da fase 3` | PR 09 - Testes obrigatorios | Todos os requisitos dos tres arquivos validos auditados. |
| 17/05/2026 | `feature/10-documentacao-defesa` | Fechar README, sequentes, decisoes do dossie, roteiro de defesa e checklist. | `docs: fecha documentacao formal da fase 3` | PR 10 - Documentacao final | README e docs sem referencias antigas conflitantes. |
| 18/05/2026 | `release/11-pre-auditoria` | Rodar suite completa, regenerar artefatos e preparar congelamento de features. | `chore: prepara pre-auditoria final da fase 3` | PR 11 - Pre-auditoria final | `python -m unittest discover -s tests -p "test_*.py" -v` aprovado e espelho atualizado. |

## Padrao diario de trabalho

1. Criar branch do dia.
2. Implementar somente o escopo da etapa.
3. Rodar testes direcionados.
4. Atualizar docs e artefatos se a etapa alterar comportamento.
5. Fazer commit com mensagem clara.
6. Abrir PR do dia.
7. Rodar suite completa antes do merge.
8. Fazer merge.
9. Rodar `.\sincronizar_para_githubmirror.ps1`.
10. Registrar resultado no PR ou em `docs/linha-do-tempo.md`.

## Padrao de commits complementares

- `test: cobre casos invalidos de tipos`
- `docs: atualiza regras de sequentes`
- `fix: corrige mensagem sem linha em erro semantico`
- `chore: regenera artefatos da ultima execucao`
- `ci: documenta comando de auditoria local`
