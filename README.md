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

A Fase 3 integra analise lexica, parser LL(1), analise semantica, tabela de simbolos, verificacao de tipos estaticos e fortes, arvore sintatica atribuida e geracao de Assembly ARMv7 para o CPulator. O programa recebe um arquivo-fonte bruto por argumento e executa todo o pipeline da entrega atual.

## Execucao

Apos clonar ou abrir o repositorio, todos os comandos devem ser executados na raiz do projeto, isto e, na pasta que contem `AnalisadorSemantico.py`.

O programa recebe sempre o arquivo-fonte por argumento de linha de comando e nao possui menu interativo.

Os arquivos oficiais da entrega ficam na mesma pasta do codigo-fonte, ao lado de `AnalisadorSemantico.py`:

- `teste1.txt`
- `teste2.txt`
- `teste3.txt`
- `teste4_semantico_invalido.txt`
- `teste5_lexico_invalido.txt`
- `teste6_sintatico_invalido.txt`

Os tres primeiros sao programas semanticamente validos. O `teste4_semantico_invalido.txt` contem erros semanticos intencionais, incluindo condicoes invalidas em estruturas de controle. O `teste5_lexico_invalido.txt` contem erros lexicos intencionais. O `teste6_sintatico_invalido.txt` contem erros sintaticos intencionais. Todos demonstram mensagens claras, varredura completa quando recuperavel e bloqueio de Assembly.

Para executar um arquivo valido da raiz:

```powershell
python AnalisadorSemantico.py teste1.txt
```

Para executar o arquivo semantico invalido oficial:

```powershell
python AnalisadorSemantico.py teste4_semantico_invalido.txt
```

Para executar os arquivos invalidos lexico e sintatico oficiais:

```powershell
python AnalisadorSemantico.py teste5_lexico_invalido.txt
python AnalisadorSemantico.py teste6_sintatico_invalido.txt
```

Para executar o `teste3.txt`, arquivo usado como referencia canonica dos artefatos finais:

```powershell
python AnalisadorSemantico.py teste3.txt
```

A execucao padrao imprime um relatorio de validacao com as fases executadas, caracteristicas detectadas no arquivo, confirmacao dos artefatos e, para todo programa valido que gera Assembly, a arvore sintatica desenhada com ramos e folhas em ASCII. Portanto, ao executar `teste3.txt`, a arvore sintatica ja e exibida automaticamente no console conforme solicitado na atividade. O Assembly nao e impresso no console; o conteudo fica em `generated/ultimo_assembly.s`.

Em qualquer arquivo analisado, valido ou invalido, o analisador procura varrer a entrada ate o final e acumular todos os erros lexicos, sintaticos e semanticos que for capaz de identificar, sem interromper a auditoria no primeiro problema encontrado.

Todos os arquivos-fonte usados como entrada de validacao ficam na raiz do projeto, ao lado de `AnalisadorSemantico.py`. Nao ha separacao em subpastas para entradas validas, invalidas ou complementares.

Na validacao final da entrega, `teste3.txt` deve ser executado por ultimo para deixar os artefatos finais alinhados com um programa semanticamente valido.

Sequencia final de validacao recomendada para os arquivos oficiais da raiz:

```powershell
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py teste5_lexico_invalido.txt
python AnalisadorSemantico.py teste6_sintatico_invalido.txt
python AnalisadorSemantico.py teste3.txt
```

Essa ordem executa os arquivos oficiais validos da raiz, confirma que os arquivos invalidos lexicos, sintaticos e semanticos bloqueiam Assembly, e encerra com `teste3.txt` como base canonica de `generated/ultimo_assembly.s`, `generated/relatorio_execucao_ultima_execucao.txt`, `generated/arvore_ultima_execucao.json` e `generated/arvore_atribuida_ultima_execucao.json`.

As funcoes de teste publicas da Fase 3 ficam em `funcoes_teste_fase3.py`, tambem na raiz. Elas exercitam os arquivos oficiais sem criar subpastas de teste:

```powershell
python funcoes_teste_fase3.py
```

## Linguagem suportada

- Programa completo: `(START)` ate `(END)`.
- Comentarios: `*{ comentario }*`, em linha inteira, fim de linha, entre tokens ou em bloco multilinha entre declaracoes.
- Leitura de memoria: `(NOME)`, por exemplo `(N)` ou `(TOTAL)`.
- Escrita/definicao de memoria: `(V NOME)`, por exemplo `(12 N)`, `(3.25 TAXA)` ou `(TRUE ATIVO)`, onde `V` pode ser `int`, `real` ou `bool`.
- Na nomenclatura do enunciado, `MEM` representa o nome da memoria; na sintaxe concreta do projeto, esse nome aparece como identificador, por exemplo `N`, `TOTAL`, `FLAG` ou `ATIVO`.
- Resultado anterior: `(N RES)`, com `N > 0`. Por decisao semantica do projeto, `0 RES` e rejeitado porque nao referencia uma declaracao anterior.
- Aritmetica: `+`, `-`, `*`, `|`, `/`, `//`, `%`, `^`. O operador `|` representa divisao real; `/` e `//` sao tratados como divisao inteira.
- Relacionais: `>`, `<`, `>=`, `<=`, `==`, `!=`.
- Logicos: `AND`, `OR`, `NOT`.
- Booleanos: `TRUE`, `FALSE`.
- Controle: `IF`, `IFELSE`, `WHILE`, `SEQ`.

## Exemplos minimos

Programa valido:

```text
(START)
(12 N)
(4 D)
(TRUE FLAG)
(((N) (D) >=) (FLAG) AND)
(((N) (D) -) N)
(END)
```

Programa invalido semanticamente:

```text
(START)
(TRUE FLAG)
((FLAG) 1 +)
((NAOEXISTE) 2 +)
(END)
```

No exemplo invalido, o analisador rejeita a soma entre `bool` e `int`, detecta o uso de variavel antes da definicao e bloqueia a geracao de Assembly.

## Regras semanticas principais

- Toda variavel deve ser definida antes do uso.
- Uma variavel pode ser reatribuida somente com o mesmo tipo.
- `int + real` promove o resultado para `real`.
- `/`, `//` e `%` aceitam apenas `int` e `int`; `//` e tratado como divisao inteira.
- `|` aceita operandos numericos e retorna `real`.
- `^` exige base numerica e expoente `int`; por orientacao do professor, o literal `0` e aceito como caso neutro/valido da potenciacao.
- Relacionais de ordem aceitam apenas numeros.
- `==` e `!=` aceitam numeros compativeis ou `bool` com `bool`.
- `IF`, `IFELSE` e `WHILE` exigem condicao `bool`.
- Assembly nao e gerado para programas com erro lexico, sintatico ou semantico.
- A analise do CLI varre o arquivo inteiro e acumula erros lexicos, sintaticos e semanticos que for capaz de identificar; ela nao para no primeiro problema encontrado.

As regras formais em calculo de sequentes estao em `docs/regras_tipos_sequentes.md`.

## Tabela de simbolos e arvore atribuida

A tabela de simbolos registra cada identificador de memoria encontrado no programa, seu tipo inferido, categoria, linha e coluna de definicao, usos posteriores, estado de inicializacao, estado de declaracao e eventuais redefinicoes incompativeis. Esse artefato fica salvo em `generated/tabela_simbolos_ultima_execucao.json` e tambem em `docs/tabela_simbolos.md`.

A arvore sintatica atribuida e gerada a partir da arvore sintatica validada pelo parser LL(1), acrescida das informacoes semanticas necessarias para a Fase 3. Cada no relevante recebe anotacoes de tipo inferido, categoria semantica e status de validacao. Esse artefato fica salvo em `generated/arvore_atribuida_ultima_execucao.json` e em `docs/arvore_atribuida_ultima_execucao.md`.

A geracao de Assembly usa a arvore sintatica atribuida como entrada e so ocorre quando nao existem erros lexicos, sintaticos ou semanticos.

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
- `docs/auditoria_dossie_inconformidades_fase3.md`: quadro ponto a ponto das inconformidades, decisoes adotadas e perguntas ao professor.
- `docs/auditoria_gramatica_parser_fase3.md`: auditoria da gramatica LL(1), parser, recuperacao sintatica e comentarios.
- `docs/auditoria_semantica_tipos_fase3.md`: auditoria da matriz semantica, tipos, `RES`, controle e potenciacao.
- `docs/auditoria_assembly_cpulator_fase3.md`: auditoria da geracao ARMv7, bloqueio em invalidos e roteiro CPulator.
- `docs/gramatica_atribuida.md`: gramatica LL(1) aumentada.
- `docs/first_follow.md`: conjuntos FIRST/FOLLOW.
- `docs/tabela_ll1.md`: tabela LL(1).
- `docs/matriz_cobertura_requisitos.md`: rastreabilidade entre enunciado, arquivos-fonte de entrada, implementacao e artefatos.
- `docs/regras_tipos_sequentes.md`: sistema de tipos em calculo de sequentes.
- `docs/estrategia_diagnosticos_acumulados.md`: varredura completa e acumulacao de erros.
- `docs/tabela_simbolos.md`: tabela de simbolos da ultima execucao.
- `docs/arvore_atribuida_ultima_execucao.md`: arvore sintatica atribuida.
- `docs/relatorio_erros_semanticos.md`: erros semanticos da ultima execucao.
- `docs/relatorio_validacao_arquivos_teste.md`: roteiro de validacao dos arquivos-fonte da raiz.

## CPulator

O Assembly e emitido para ARMv7 DE1-SoC com `.syntax unified`, `.arch armv7-a`, `.fpu vfpv3`, ponto de entrada `_start` e rotinas JTAG UART para saida. Referencia do simulador: https://cpulator.01xz.net/?sys=arm-de1soc

Na validacao final, o Assembly produzido por `teste3.txt` foi compilado no CPulator ARMv7 DE1-SoC com sucesso, e a saida JTAG UART foi compativel com os resultados esperados para as linhas executaveis do arquivo.

## Rastreabilidade

Repositorio GitHub: `https://github.com/HeltonBr/RA3-4`.

O desenvolvimento e documentado pelo historico publico de commits, branches e pull requests do GitHub.
