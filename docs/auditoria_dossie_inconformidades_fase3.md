# Auditoria do Dossie de Inconformidades - Fase 3

Fonte revisada: `Dossie_Inconformidades_Fase3_Analisador_Semantico.docx`.

Objetivo: registrar, em linguagem de entrega, como cada inconformidade do dossie foi tratada no projeto, qual evidencia existe no repositorio e quais pontos ainda devem ser confirmados com o professor durante a auditoria.

## Perguntas prioritarias para o professor

Situacao apos a conversa de 15/05/2026: `//` foi confirmado como operador aceito de divisao inteira, e `0` foi confirmado como inteiro positivo para a regra de potenciacao. Os itens abaixo permanecem como rastreio do que foi perguntado ou ainda merece confirmacao fina.

1. **INC-03 - memoria nao definida:** na Fase 3, a regra de "variavel deve ser definida antes do uso" deve prevalecer sobre a regra historica de `(MEM)` retornar `0` quando nao inicializada?
2. **INC-05 - booleanos/logicos:** a escolha `TRUE`, `FALSE`, `AND`, `OR`, `NOT` e operadores relacionais simbolicos e aceitavel como convencao documentada pelo grupo?
3. **INC-06 - controle:** a sintaxe pos-fixada herdada da Fase 2 para `IF`, `IFELSE`, `WHILE` e `SEQ` e suficiente para a prova de autoria?
4. **INC-07 - arquivos de teste:** a interpretacao correta e manter tres arquivos validos completos e arquivos invalidos separados, em vez de misturar erros em todos os arquivos?
5. **INC-11 - `RES`:** `N=0` deve ser erro semantico, ja que nao referencia linha anterior?
6. **INC-12 - comentarios:** comentarios `*{ ... }*` devem ser nao aninhados, com erro lexico quando nao fechados?
7. **INC-17 - potenciacao:** resolvido parcialmente; `0` e aceito como inteiro positivo. Para expoente vindo de memoria ou expressao, o codigo garante estaticamente o tipo `int`.
8. **INC-18 - entrada:** a entrega final deve priorizar arquivo-fonte bruto por argumento, mantendo tokens serializados apenas como compatibilidade?

## Quadro ponto a ponto

### INC-01 - Operadores de divisao

- **Risco do dossie:** Fase 1 usava `/` e `//`, enquanto Fase 2/3 usam `|` para divisao real e `/` para divisao inteira.
- **Tratamento adotado:** codigo-fonte bruto da Fase 3 usa `|` para divisao real e aceita `/` e `//` como divisao inteira. O parser normaliza `//` para a mesma operacao de `/` na AST.
- **Evidencia:** `README.md`, `docs/regras_tipos_sequentes.md`, `src/analisador_sintatico_ll1/tokens.py`, `src/analisador_sintatico_ll1/parser_ll1.py`, `tests/test_auditoria_semantica_tipos.py`.
- **Duvida residual:** resolvida por orientacao do professor em 15/05/2026.

### INC-02 - Vocabulario lexico ampliado

- **Risco do dossie:** a Fase 3 exige mais tokens que a Fase 1, mas destaca apenas comentarios.
- **Tratamento adotado:** lexer reconhece `START`, `END`, `RES`, `SEQ`, `IF`, `IFELSE`, `WHILE`, `TRUE`, `FALSE`, `AND`, `OR`, `NOT`, operadores relacionais e comentarios.
- **Evidencia:** `tokens.py`, `docs/gramatica_atribuida.md`, `tests/test_fase2_pipeline.py`, `tests/test_variacoes_formato.py`.
- **Duvida residual:** baixa; manter na auditoria de 13/05 para entradas externas do professor.

### INC-03 - Variavel antes da definicao versus retorno zero

- **Risco do dossie:** o texto antigo de `(MEM)` retornar `0` conflita com a regra semantica de definicao obrigatoria.
- **Tratamento adotado:** na Fase 3, variavel nunca definida e erro semantico; a regra de retorno `0` nao autoriza uso sem definicao.
- **Evidencia:** `docs/decisoes_inconformidades_fase3.md`, `type_system.py`, `tests/invalidos/semantico_variavel_nao_definida.txt`.
- **Duvida residual:** confirmar com o professor que a regra nova de semantica forte prevalece sobre a heranca operacional antiga.

### INC-04 - `(V MEM)` e tipos estaticos

- **Risco do dossie:** o texto fala em armazenar real, mas a Fase 3 exige `int`, `real` e `bool`.
- **Tratamento adotado:** `(V MEM)` define o tipo pelo valor `V`; reatribuicao so e aceita com o mesmo tipo.
- **Evidencia:** `docs/regras_tipos_sequentes.md`, `type_system.py`, `tests/invalidos/semantico_redefinicao_tipo.txt`.
- **Duvida residual:** confirmar se a inferencia pelo valor e suficiente, ja que a linguagem nao fornece declaracao explicita de tipo.

### INC-05 - Sintaxe de bool, logicos e relacionais

- **Risco do dossie:** a Fase 3 exige bool/logicos, mas nao padroniza lexemas.
- **Tratamento adotado:** literais `TRUE` e `FALSE`; logicos `AND`, `OR`, `NOT`; relacionais `>`, `<`, `>=`, `<=`, `==`, `!=`; todos em pos-fixo.
- **Evidencia:** `README.md`, `docs/sintaxe_controle.md`, `docs/regras_tipos_sequentes.md`, `tests/teste1.txt`, `tests/teste2.txt`, `tests/teste3.txt`.
- **Duvida residual:** confirmar se o professor aceita essa convencao lexical em testes externos.

### INC-06 - Estruturas de controle

- **Risco do dossie:** decisao/laco dependem da sintaxe definida pelo grupo, mas a Fase 3 cobra semantica e Assembly.
- **Tratamento adotado:** sintaxe pos-fixada: `(<expr> <stmt> IF)`, `(<expr> <stmt> <stmt> IFELSE)`, `(<expr> <stmt> WHILE)`, `(<stmt> <stmt> SEQ)`.
- **Evidencia:** `docs/sintaxe_controle.md`, `docs/gramatica_atribuida.md`, `ast_nodes.py`, `codegen_arm.py`, arquivos `teste*.txt`.
- **Duvida residual:** confirmar se comandos de controle devem produzir valor ou apenas fluxo; hoje `IF` e `WHILE` sao tratados como `void`, `IFELSE` pode propagar tipo compativel.

### INC-07 - Conflito nos arquivos de teste

- **Risco do dossie:** um trecho sugere erros em cada arquivo, outro exige ao menos um arquivo semanticamente valido.
- **Tratamento adotado:** tres arquivos oficiais validos completos na raiz e um arquivo oficial invalido semantico separado; suite complementar cobre lexicos/sintaticos/semanticos.
- **Evidencia:** `teste1.txt`, `teste2.txt`, `teste3.txt`, `teste4_semantico_invalido.txt`, `docs/matriz_cobertura_requisitos.md`.
- **Duvida residual:** confirmar que os erros podem estar no conjunto da bateria, e nao necessariamente dentro de cada arquivo valido.

### INC-08 - Assembly para validos versus invalidos

- **Risco do dossie:** algumas secoes pedem Assembly, outras bloqueiam Assembly em erro.
- **Tratamento adotado:** Assembly so e gerado quando nao ha erro lexico, sintatico ou semantico; invalidos recebem relatorio e marcador textual no arquivo de Assembly.
- **Evidencia:** `main.py`, `tests/test_auditoria_entrega.py`, `tests/test_fase2_pipeline.py`, `generated/ultimo_assembly.s`.
- **Duvida residual:** baixa; manter a mensagem de bloqueio muito clara para avaliacao.

### INC-09 - Momento de geracao de Assembly

- **Risco do dossie:** texto alterna entre gerar durante parser e gerar apos arvore atribuida.
- **Tratamento adotado:** pipeline separa fases: lexico, parser, tabela, tipos, arvore atribuida e so depois Assembly.
- **Evidencia:** `main.py`, `core.py`, `attributed_ast.py`, `codegen_arm.py`.
- **Duvida residual:** baixa; justificar que isso evita emissao parcial de codigo invalido.

### INC-10 - FIRST/FOLLOW e tabela LL(1)

- **Risco do dossie:** a Fase 3 pede gramatica LL(1), mas nao explicita FIRST/FOLLOW/tabela atualizados.
- **Tratamento adotado:** projeto gera e versiona gramatica, FIRST/FOLLOW e tabela LL(1) da linguagem aumentada.
- **Evidencia:** `docs/gramatica_atribuida.md`, `docs/first_follow.md`, `docs/tabela_ll1.md`, `tests/test_fase2_pipeline.py`.
- **Duvida residual:** baixa; PR 06 deve auditar conflitos e entradas externas.

### INC-11 - Semantica de `(N RES)`

- **Risco do dossie:** falta definir `N=0`, estouro de historico e comandos sem valor.
- **Tratamento adotado:** `N > 0`; referencia apenas declaracao de topo anterior com valor utilizavel; `void` e erro nao podem ser usados.
- **Evidencia:** `docs/regras_tipos_sequentes.md`, `type_system.py`, `tests/invalidos/semantico_res_invalido.txt`.
- **Duvida residual:** confirmar se `RES` deve contar apenas declaracoes de topo, como hoje, ou tambem comandos internos de `IF`, `WHILE` e `SEQ`.

### INC-12 - Comentarios e conflito com `*`

- **Risco do dossie:** comentario comeca em `*{`, mas `*` tambem e multiplicacao.
- **Tratamento adotado:** scanner testa `*{` antes de `*`, descarta comentarios sem perder linha/coluna, aceita multilinha e rejeita comentario nao fechado.
- **Evidencia:** `tokens.py`, `tests/variacoes/comentario_multilinha.txt`, `tests/invalidos/lexico_comentario_nao_fechado.txt`.
- **Duvida residual:** confirmar que comentarios aninhados nao sao exigidos; hoje nao sao suportados como aninhamento.

### INC-13 - Palavras reservadas

- **Risco do dossie:** apenas `RES` e explicitamente reservada, mas ha outros lexemas estruturais.
- **Tratamento adotado:** `START`, `END`, `RES`, `SEQ`, `IF`, `IFELSE`, `WHILE`, `TRUE`, `FALSE`, `AND`, `OR`, `NOT` sao reservadas.
- **Evidencia:** `tokens.py`, `tests/invalidos/sintaxe_palavra_reservada_memoria.txt`, `tests/test_variacoes_formato.py`.
- **Duvida residual:** baixa; manter cobertura para nomes reservados nos testes externos.

### INC-14 - Artefatos do GitHub

- **Risco do dossie:** lista de artefatos mistura sintatico/semantico e omite alguns itens.
- **Tratamento adotado:** README lista artefatos gerados; docs incluem tabela de simbolos, arvore atribuida, relatorio de erros, matriz, gramatica, sequentes e Assembly.
- **Evidencia:** `README.md`, `docs/`, `generated/`, `tests/test_auditoria_entrega.py`.
- **Duvida residual:** baixa; antes do congelamento conferir que a ultima execucao canonica e valida.

### INC-15 - Secao de testes ainda fala em parser

- **Risco do dossie:** a Fase 3 mistura foco sintatico e semantico.
- **Tratamento adotado:** suite cobre os dois: parser robusto e semantica forte, incluindo prova de autoria com entradas externas planejada para PR 09.
- **Evidencia:** `tests/test_fase2_pipeline.py`, `tests/test_auditoria_entrega.py`, `docs/cronograma_commits_prs_fase3.md`.
- **Duvida residual:** media; PR 09 deve criar arquivos novos nao oficiais para simular codigo fornecido pelo professor.

### INC-16 - Matriz de compatibilidade de tipos

- **Risco do dossie:** compatibilidade de tipos nao esta definida no enunciado.
- **Tratamento adotado:** regras formais em sequentes: promocao numeric para `real`, `/` e `%` exigem `int`, `|` retorna `real`, logicos exigem `bool`, relacionais retornam `bool`.
- **Evidencia:** `docs/regras_tipos_sequentes.md`, `type_system.py`, `docs/matriz_cobertura_requisitos.md`.
- **Duvida residual:** PR 07 deve ampliar testes cruzados de combinacoes invalidas para reduzir risco de falso positivo/falso negativo.

### INC-17 - Potenciacao

- **Risco do dossie:** fases anteriores exigiam expoente inteiro positivo; Fase 3 fala apenas em compatibilidade.
- **Tratamento adotado:** expoente deve ser `int`; base deve ser numerica; expoente literal `0` e aceito como inteiro positivo por orientacao do professor. Expoente vindo de memoria ou expressao tem tipo verificado como `int`.
- **Evidencia:** `docs/regras_tipos_sequentes.md`, `docs/auditoria_semantica_tipos_fase3.md`, `type_system.py`, `tests/test_auditoria_semantica_tipos.py`, `README.md`.
- **Duvida residual:** resolvida quanto ao literal `0`; manter apenas revisao geral da matriz de tipos na bateria final.

### INC-18 - Fonte bruto versus tokens serializados

- **Risco do dossie:** fases anteriores falam em tokens salvos; Fase 3 pede rodar os tres analisadores no arquivo.
- **Tratamento adotado:** entrada principal e arquivo-fonte bruto por argumento; tokens serializados seguem aceitos apenas por compatibilidade.
- **Evidencia:** `README.md`, `main.py`, `tokens.py`, `tests/test_fase2_pipeline.py`.
- **Duvida residual:** confirmar que a prova de autoria fornecera fonte bruto, nao arquivo de tokens.

### INC-19 - Cabecalho Python

- **Risco do dossie:** modelo usa `//`, mas Python usa `#`.
- **Tratamento adotado:** arquivos Python usam cabecalho institucional com `#`.
- **Evidencia:** arquivos em `src/`, `AnalisadorSemantico.py`, testes.
- **Duvida residual:** baixa; se houver validador textual rigido, professor deve aceitar adaptacao por linguagem.

### INC-20 - Regex em comentarios

- **Risco do dossie:** Fase 1 proibia regex no lexico; comentarios poderiam ser implementados como pre-processamento irregular.
- **Tratamento adotado:** scanner caractere a caractere trata comentarios; na etapa 06 o inventario de comentarios do relatorio tambem passou a usar varredura manual, sem regex.
- **Evidencia:** `tokens.py`, `main.py`, `tests/test_auditoria_gramatica_parser.py`.
- **Duvida residual:** baixa; manter como decisao documentada para demonstrar aderencia conservadora ao requisito.

### INC-21 - CPulator

- **Risco do dossie:** grafia varia entre Cpulater/Cpulator/CPULATOR.
- **Tratamento adotado:** README e docs usam CPulator como grafia operacional.
- **Evidencia:** `README.md`, `docs/relatorio_validacao_arquivos_teste.md`, `docs/bateria_pesada_testes_fase3.md`.
- **Duvida residual:** baixa.

### INC-22 - Documentacao truncada

- **Risco do dossie:** secao final de README/documentacao esta incompleta.
- **Tratamento adotado:** README foi completado com execucao, linguagem, regras, testes, artefatos, docs, CPulator e rastreabilidade.
- **Evidencia:** `README.md`, `docs/checklist-entrega.md`, `tests/test_auditoria_entrega.py`.
- **Duvida residual:** baixa; revisar visualmente antes do congelamento.

## Pontos que entram nas proximas auditorias

- **PR 06 - Gramatica/parser:** INC-01, INC-02, INC-05, INC-06, INC-10, INC-12, INC-13, INC-18, INC-20.
- **PR 07 - Semantica/tipos:** INC-03, INC-04, INC-11, INC-16, INC-17.
- **PR 08 - Assembly/artefatos:** INC-08, INC-09, INC-14, INC-21.
- **PR 09 - Entradas externas:** INC-05, INC-06, INC-07, INC-15, INC-18.
- **PR 10 - Documentacao de defesa:** INC-07, INC-14, INC-19, INC-22.
