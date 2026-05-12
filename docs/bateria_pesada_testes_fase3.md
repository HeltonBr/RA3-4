# Bateria Pesada de Testes - 7 Dias Finais

Periodo reservado: **19/05/2026 a 25/05/2026 23:59**.

Objetivo: detectar inconsistencias penalizantes antes do congelamento da pasta principal e do GitHub. Nesta janela nao entram features novas; so correcoes pontuais com evidencia de teste.

## Regras da janela final

- Sempre rodar a suite completa antes e depois de qualquer correcao.
- Regenerar artefatos com `teste3.txt` apos cada correcao.
- Sincronizar `GitHubmirror` apos cada estado aprovado.
- Nao alterar regra semantica sem atualizar `docs/regras_tipos_sequentes.md` e testes correspondentes.
- Nao deixar `generated/ultimo_assembly.s` vindo de execucao invalida.

## Plano diario

| Data | Foco | Comandos e verificacoes |
| --- | --- | --- |
| 19/05/2026 | Regressao geral | `python -m unittest discover -s tests -p "test_*.py" -v`; executar `teste1.txt`, `teste2.txt`, `teste3.txt` e `teste4_semantico_invalido.txt`; conferir `generated/`. |
| 20/05/2026 | Lexico e comentarios | Testar comentario em linha inteira, fim de linha, entre tokens, multiline e nao fechado; verificar linha/coluna dos erros. |
| 21/05/2026 | Parser LL(1) | Revisar gramatica, FIRST/FOLLOW e tabela LL(1); testar expressoes vazias, END ausente e declaracoes na mesma linha. |
| 22/05/2026 | Semantica de variaveis e tipos | Testar uso antes da definicao, reatribuicao incompativel, `RES` invalido, `%`/`/` com real, bool em aritmetica e condicao nao bool. |
| 23/05/2026 | Controle e aninhamento | Testar `IF`, `IFELSE`, `WHILE`, `SEQ`, aninhamento profundo e sequencias longas; procurar falsos positivos e falsos negativos. |
| 24/05/2026 | Assembly e CPulator | Verificar que validos geram Assembly e invalidos bloqueiam; abrir `generated/ultimo_assembly.s` no CPulator ARMv7 DE1-SoC. |
| 25/05/2026 | Auditoria final e congelamento | Rodar suite completa, regenerar artefatos, revisar README/docs/checklist, sincronizar `GitHubmirror`, conferir GitHub e congelar as pastas as 23:59. |

## Checklist pesado

- [ ] Erro lexico sem traceback.
- [ ] Erro sintatico sem traceback.
- [ ] Erro semantico sem traceback.
- [ ] Arquivo com multiplos erros e varrido ate o fim, sem parar no primeiro problema.
- [ ] Toda mensagem possui tipo, linha, coluna e causa.
- [ ] Comentario `*{ ... }*` nao desloca linhas dos erros.
- [ ] START e END nao sao aceitos como memoria.
- [ ] TRUE/FALSE nao sao aceitos como memoria.
- [ ] AND/OR/NOT nao sao aceitos como memoria.
- [ ] Variavel usada antes da definicao e rejeitada.
- [ ] Reatribuicao com mesmo tipo aceita.
- [ ] Reatribuicao com tipo diferente rejeitada.
- [ ] `/` e `%` rejeitam real e bool.
- [ ] `|` aceita int/real e retorna real.
- [ ] `^` exige expoente int.
- [ ] Condicoes de `IF`, `IFELSE` e `WHILE` exigem bool.
- [ ] `RES` com N=0 rejeitado.
- [ ] `RES` fora do historico rejeitado.
- [ ] `RES` apontando para comando sem valor rejeitado.
- [ ] Tabela de simbolos registra definicao, usos e tipo.
- [ ] Arvore atribuida registra tipos em todos os nos relevantes.
- [ ] Assembly nao e gerado para programa invalido.
- [ ] Assembly e gerado para os tres programas validos.
- [ ] README explica execucao, testes, linguagem e CPulator.
- [ ] `docs/decisoes_inconformidades_fase3.md` cobre todas as inconformidades.
- [ ] GitHubmirror esta identico a pasta principal apos a ultima sincronizacao.

## Comandos canonicos

```powershell
python AnalisadorSemantico.py tests/teste1.txt
python AnalisadorSemantico.py tests/teste2.txt
python AnalisadorSemantico.py tests/teste3.txt
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste3.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py tests/invalidos/lexico_comentario_nao_fechado.txt
python AnalisadorSemantico.py tests/invalidos/sintaxe_sem_end.txt
python AnalisadorSemantico.py tests/invalidos/semantico_variavel_nao_definida.txt
python AnalisadorSemantico.py tests/invalidos/semantico_tipo_incompativel.txt
python AnalisadorSemantico.py tests/invalidos/semantico_condicao_nao_bool.txt
python -m unittest discover -s tests -p "test_*.py" -v
.\sincronizar_para_githubmirror.ps1
```
