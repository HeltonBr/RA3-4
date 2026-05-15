# Decisoes para Inconformidades da Fase 3

Este documento registra como o projeto trata as inconsistencias detectadas no dossie. A regra usada na implementacao deve coincidir com a documentacao e com os testes.

| ID | Decisao adotada |
| --- | --- |
| INC-01 | A Fase 3 usa `|` para divisao real e `/` para divisao inteira. Por orientacao do professor, `//` tambem e aceito como operador de divisao inteira e normalizado para a mesma regra de `/`. |
| INC-02 | O lexico reconhece START, END, RES, SEQ, IF, IFELSE, WHILE, TRUE, FALSE, AND, OR, NOT, relacionais e comentarios. |
| INC-03 | Variavel nunca definida e erro semantico. A regra antiga de retorno 0 fica restrita ao comportamento historico do Assembly, nao ao aceite semantico da Fase 3. |
| INC-04 | `(V MEM)` define ou reatribui memoria com o tipo inferido de `V`: `int`, `real` ou `bool`. Reatribuicao so e aceita com o mesmo tipo. |
| INC-05 | Booleanos literais sao `TRUE` e `FALSE`; logicos sao `AND`, `OR` e `NOT`; relacionais retornam `bool`. |
| INC-06 | Controle segue a sintaxe pos-fixada da Fase 2: `(<expr> <stmt> IF)`, `(<expr> <stmt> <stmt> IFELSE)`, `(<expr> <stmt> WHILE)` e `(<stmt> <stmt> SEQ)`. Condicoes devem ser `bool`. |
| INC-07 | Ha tres arquivos validos completos em `tests/teste1.txt`, `tests/teste2.txt`, `tests/teste3.txt` e arquivos invalidos separados em `tests/invalidos/`. Assim a suite cobre programas semanticamente validos e erros intencionais sem misturar as finalidades. |
| INC-08 | Assembly nao e gerado para programas invalidos. O relatorio explica a interrupcao e `generated/ultimo_assembly.s` recebe apenas um marcador textual quando a ultima execucao falha. |
| INC-09 | O parser constroi AST; a geracao de Assembly ocorre depois da arvore atribuida e da validacao semantica. Isso evita emissao parcial para programa invalido. |
| INC-10 | A documentacao gera gramatica, FIRST/FOLLOW e tabela LL(1) tambem para a versao aumentada. |
| INC-11 | `(N RES)` exige `N > 0` e referencia uma declaracao de topo anterior que produza valor utilizavel. START, END e comentarios nao entram na contagem. |
| INC-12 | O lexico verifica `*{` antes de tratar `*` como multiplicacao, preserva linha/coluna e acusa comentario nao fechado. Comentarios nao sao aninhados. |
| INC-13 | START, END, RES, SEQ, IF, IFELSE, WHILE, TRUE, FALSE, AND, OR e NOT sao reservadas e nao podem ser nomes de memoria. |
| INC-14 | Os artefatos semanticos obrigatorios foram explicitados: tabela de simbolos, arvore atribuida, relatorio de erros e Assembly da ultima execucao valida. |
| INC-15 | Os testes automatizados incluem cenarios lexicos, sintaticos e semanticos, com foco na Fase 3. |
| INC-16 | A matriz de tipos esta documentada em `docs/regras_tipos_sequentes.md` e implementada em `src/analisador_sintatico_ll1/type_system.py`. |
| INC-17 | Potenciacao exige expoente `int`. Por orientacao do professor, o literal `0` e aceito como inteiro positivo nesta linguagem. |
| INC-18 | A entrada principal e o arquivo-fonte bruto. A leitura de tokens serializados foi mantida apenas por compatibilidade com as fases anteriores. |
| INC-19 | Como o projeto e Python, o cabecalho obrigatorio usa `#`. |
| INC-20 | Comentarios foram implementados no scanner caractere a caractere, sem expressoes regulares. |
| INC-21 | A documentacao usa CPulator como grafia operacional do simulador. |
| INC-22 | A lista truncada de documentacao foi completada a partir dos criterios de avaliacao e do kit de continuidade. |

Frase operacional: Assembly nao e gerado para programas invalidos; primeiro vem lexico, parser, tabela de simbolos, verificacao de tipos e arvore sintatica atribuida.

Decisao adicional de robustez: a execucao principal deve varrer o arquivo inteiro e acumular diagnosticos. Um erro em uma linha nao pode impedir a identificacao de outros erros recuperaveis nas linhas seguintes.

Quadro detalhado para defesa e perguntas ao professor: `docs/auditoria_dossie_inconformidades_fase3.md`.
