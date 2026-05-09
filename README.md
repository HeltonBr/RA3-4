# Analisador Semantico - Fase 3

Projeto da disciplina de Linguagens Formais e Compiladores da Pontificia Universidade Catolica do Parana (PUC-PR), ano 2026.

## Informacoes institucionais

- Instituicao: Pontificia Universidade Catolica do Parana (PUC-PR)
- Ano: 2026
- Disciplina: Linguagens Formais e Compiladores
- Professor: Frank Coelho de Alcantara
- Integrante: Helton Tessari Brandao - `HeltonBr`
- Grupo no Canvas: `RA3-4`

## Objetivo

A Fase 3 reaproveita a base da Fase 2 e acrescenta analise semantica. O programa le um arquivo-fonte, executa o lexico, o parser LL(1), constroi a tabela de simbolos, verifica tipos estaticos e fortes, gera a arvore sintatica atribuida e so entao emite Assembly ARMv7 para o CPulator.

## Execucao

```powershell
python AnalisadorSemantico.py teste1.txt
```

Tambem e possivel manter compatibilidade com o nome antigo:

```powershell
python AnalisadorSintatico.py teste1.txt
```

A execucao padrao imprime um relatorio de validacao com as fases executadas, caracteristicas detectadas no arquivo e confirmacao dos artefatos. A arvore sintatica pode ser mostrada no console quando necessario:

```powershell
python AnalisadorSemantico.py teste3.txt --mostrar-arvore
python AnalisadorSemantico.py teste3.txt --relatorio-completo
```

O Assembly ARMv7 nao e despejado no console; o programa apenas confirma se ele foi gerado ou bloqueado, e o conteudo fica em `generated/ultimo_assembly.s`.

## Testes

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Linguagem suportada

- Programa completo: `(START)` ate `(END)`.
- Comentarios: `*{ comentario }*`, em linha inteira, fim de linha, entre tokens ou em bloco multilinha entre declaracoes.
- Leitura de memoria: `(MEM)`.
- Escrita/definicao de memoria: `(V MEM)`, onde `V` pode ser `int`, `real` ou `bool`.
- Resultado anterior: `(N RES)`, com `N > 0`.
- Aritmetica: `+`, `-`, `*`, `|`, `/`, `%`, `^`.
- Relacionais: `>`, `<`, `>=`, `<=`, `==`, `!=`.
- Logicos: `AND`, `OR`, `NOT`.
- Booleanos: `TRUE`, `FALSE`.
- Controle: `IF`, `IFELSE`, `WHILE`, `SEQ`.

## Regras semanticas principais

- Toda variavel deve ser definida antes do uso.
- Uma variavel pode ser reatribuida somente com o mesmo tipo.
- `int + real` promove o resultado para `real`.
- `/` e `%` aceitam apenas `int` e `int`.
- `|` aceita operandos numericos e retorna `real`.
- `^` exige base numerica e expoente `int`.
- Relacionais de ordem aceitam apenas numeros.
- `==` e `!=` aceitam numeros compativeis ou `bool` com `bool`.
- `IF`, `IFELSE` e `WHILE` exigem condicao `bool`.
- Assembly nao e gerado para programas com erro lexico, sintatico ou semantico.
- A analise do CLI varre o arquivo inteiro e acumula erros lexicos, sintaticos e semanticos; ela nao para no primeiro problema encontrado.

As regras formais em calculo de sequentes estao em `docs/regras_tipos_sequentes.md`.

## Artefatos gerados

- `generated/tokens_ultima_execucao.txt`
- `generated/arvore_ultima_execucao.json`
- `generated/tabela_simbolos_ultima_execucao.json`
- `generated/arvore_atribuida_ultima_execucao.json`
- `generated/relatorio_erros_ultima_execucao.txt`
- `generated/relatorio_execucao_ultima_execucao.txt`
- `generated/ultimo_assembly.s`

## Documentacao

- `docs/decisoes_inconformidades_fase3.md`: tratamento das inconsistencias do dossie.
- `docs/gramatica_atribuida.md`: gramatica LL(1) aumentada.
- `docs/first_follow.md`: conjuntos FIRST/FOLLOW.
- `docs/tabela_ll1.md`: tabela LL(1).
- `docs/regras_tipos_sequentes.md`: sistema de tipos em calculo de sequentes.
- `docs/estrategia_diagnosticos_acumulados.md`: varredura completa e acumulacao de erros.
- `docs/tabela_simbolos.md`: tabela de simbolos da ultima execucao.
- `docs/arvore_atribuida_ultima_execucao.md`: arvore sintatica atribuida.
- `docs/relatorio_erros_semanticos.md`: erros semanticos da ultima execucao.
- `docs/relatorio_validacao_arquivos_teste.md`: roteiro de validacao dos arquivos de teste.

## CPulator

O Assembly e emitido para ARMv7 DE1-SoC com `.syntax unified`, `.arch armv7-a`, `.fpu vfpv3`, ponto de entrada `_start` e rotinas JTAG UART para saida. Referencia do simulador: https://cpulator.01xz.net/?sys=arm-de1soc

## Rastreabilidade

O repositorio deve ser publico, nomeado com o grupo exato do Canvas e trabalhado por branches e pull requests. Mesmo em grupo individual, os PRs documentam autoria, revisao e integracao.

## Cronograma e congelamento

- Data final de congelamento da pasta principal e do GitHub: **25/05/2026 as 23:59**.
- Desenvolvimento com commits e pull requests diarios: `docs/cronograma_commits_prs_fase3.md`.
- Bateria pesada dos 7 dias finais: `docs/bateria_pesada_testes_fase3.md`.
- Espelho local exato ate o congelamento: `GitHubmirror`, atualizado por:

```powershell
.\sincronizar_para_githubmirror.ps1
```
