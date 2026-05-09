# Checklist Final de Entrega - Fase 3

## Identificacao

- [ ] Nome do repositorio igual ao grupo Canvas: `RA3-4` ou nome exato confirmado.
- [x] Data final de congelamento documentada: 25/05/2026 as 23:59.
- [x] Ponto de entrada principal: `AnalisadorSemantico.py`.
- [x] Cabecalho obrigatorio nos arquivos principais.
- [x] README com instituicao, disciplina, professor, integrante, execucao e CPulator.
- [x] `teste1.txt`, `teste2.txt` e `teste3.txt` disponiveis na mesma pasta do codigo-fonte.

## Funcoes exigidas

- [x] `prepararEntradaSemantica`
- [x] `construirTabelaSimbolos`
- [x] `verificarTipos`
- [x] `gerarArvoreAtribuida`
- [x] `gerarAssembly`

## Semantica

- [x] Comentarios `*{ ... }*`.
- [x] Variavel definida antes do uso.
- [x] Tabela de simbolos com tipo, definicao e usos.
- [x] Tipos `int`, `real` e `bool`.
- [x] Reatribuicao apenas com mesmo tipo.
- [x] Condicoes de `IF`, `IFELSE` e `WHILE` obrigatoriamente `bool`.
- [x] Bloqueio de Assembly em caso de erro.
- [x] Varredura completa do arquivo com acumulacao de erros; o CLI nao interrompe no primeiro erro.

## Artefatos

- [x] `docs/cronograma_commits_prs_fase3.md`
- [x] `docs/bateria_pesada_testes_fase3.md`
- [x] `docs/gramatica_atribuida.md`
- [x] `docs/regras_tipos_sequentes.md`
- [x] `docs/estrategia_diagnosticos_acumulados.md`
- [x] `docs/tabela_simbolos.md`
- [x] `docs/arvore_atribuida_ultima_execucao.md`
- [x] `docs/relatorio_erros_semanticos.md`
- [x] `docs/relatorio_validacao_arquivos_teste.md`
- [x] `generated/relatorio_execucao_ultima_execucao.txt`
- [x] `generated/ultimo_assembly.s`

## Testes

- [x] Tres programas validos com 10+ linhas.
- [x] Copias dos tres programas validos na raiz sincronizadas com `tests/`.
- [x] Testes invalidos lexicos, sintaticos e semanticos.
- [x] Teste com multiplos erros misturados no mesmo arquivo.
- [x] Comentarios em linha inteira, fim de linha, entre tokens e bloco multilinha.
- [x] Palavras reservadas nao aceitas como identificadores de memoria.
- [x] Todos os operadores aritmeticos nos tres arquivos validos.
- [x] `IF`/`IFELSE`, `WHILE`, `SEQ`, `RES`, leitura e escrita de memoria.

## Validacao local

```powershell
python AnalisadorSemantico.py teste3.txt
python AnalisadorSemantico.py teste3.txt --mostrar-arvore
python -m unittest discover -s tests -p "test_*.py" -v
.\sincronizar_para_githubmirror.ps1
```

## Congelamento

- [ ] PRs diarios planejados ate 18/05/2026.
- [ ] Bateria pesada planejada de 19/05/2026 a 25/05/2026.
- [ ] `GitHubmirror` sincronizado apos cada merge aprovado.
- [ ] Pasta principal local congelada em 25/05/2026 as 23:59.
- [ ] Repositorio GitHub congelado em 25/05/2026 as 23:59.
