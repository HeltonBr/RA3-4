# Matriz de Cobertura dos Requisitos - Fase 3

Esta matriz consolida a rastreabilidade entre o enunciado, os arquivos oficiais, a implementacao e os testes automatizados. Ela deve ser revisada a cada etapa que alterar entrada, CLI, testes, semantica, artefatos ou README.

## Arquivos oficiais na raiz

| Arquivo | Papel na entrega | Status |
| --- | --- | --- |
| `teste1.txt` | Programa semanticamente valido com cobertura completa de operadores, memoria, `RES`, controle, tipos e comentarios. | Coberto |
| `teste2.txt` | Programa semanticamente valido com combinacoes alternativas de booleanos, controle e reatribuicoes validas. | Coberto |
| `teste3.txt` | Programa semanticamente valido com expressoes aninhadas de complexidade crescente. | Coberto |
| `teste4_semantico_invalido.txt` | Programa sintaticamente reconhecivel com erros semanticos intencionais acumulados. | Coberto |

Os tres arquivos validos tambem ficam sincronizados em `tests/teste1.txt`, `tests/teste2.txt` e `tests/teste3.txt` para uso da suite automatizada.

## Cobertura por arquivo valido

| Requisito | `teste1.txt` | `teste2.txt` | `teste3.txt` |
| --- | --- | --- | --- |
| 10 ou mais linhas uteis | Sim | Sim | Sim |
| `START` e `END` | Sim | Sim | Sim |
| Operadores aritmeticos `+ - * \| / % ^` | Sim | Sim | Sim |
| Operadores relacionais `> < >= <= == !=` | Sim | Sim | Sim |
| Operadores logicos `AND OR NOT` | Sim | Sim | Sim |
| Literais `int`, `real` e `bool` | Sim | Sim | Sim |
| Leitura de memoria `(MEM)` | Sim | Sim | Sim |
| Escrita de memoria `(V MEM)` | Sim | Sim | Sim |
| Resultado anterior `(N RES)` | Sim | Sim | Sim |
| Tomada de decisao `IF` | Sim | Sim | Sim |
| Tomada de decisao `IFELSE` | Sim | Sim | Sim |
| Laco `WHILE` | Sim | Sim | Sim |
| Sequenciamento `SEQ` | Sim | Sim | Sim |
| Comentarios em linha inteira | Sim | Sim | Sim |
| Comentarios no final de linha | Sim | Sim | Sim |
| Comentarios entre tokens | Sim | Sim | Sim |
| Comentarios multilinha | Sim | Sim | Sim |
| Expressoes aninhadas | Sim | Sim | Sim |
| Gera Assembly sem erros | Sim | Sim | Sim |

## Cobertura de erros

| Tipo de erro | Evidencia | Verificacao |
| --- | --- | --- |
| Lexico | `tests/invalidos/lexico_*.txt` | `tests.test_fase2_pipeline`, `tests.test_variacoes_formato` |
| Sintatico | `tests/invalidos/sintaxe_*.txt` | `tests.test_fase2_pipeline`, `tests.test_variacoes_formato` |
| Semantico | `teste4_semantico_invalido.txt` e `tests/invalidos/semantico_*.txt` | `tests.test_auditoria_entrega`, `tests.test_fase2_pipeline` |
| Multiplos erros no mesmo arquivo | `tests/invalidos/auditoria_multiplos_erros.txt` | `test_cli_varre_arquivo_inteiro_e_lista_multiplos_erros` |

## Requisitos transversais

| Requisito do enunciado | Evidencia no projeto | Trava automatizada |
| --- | --- | --- |
| Execucao por argumento, sem menu | `python AnalisadorSemantico.py teste1.txt` | Suite `unittest` executa CLI por subprocess |
| Arquivos de teste na mesma pasta do codigo-fonte | `teste1.txt`, `teste2.txt`, `teste3.txt`, `teste4_semantico_invalido.txt` na raiz | `test_arquivos_de_teste_obrigatorios_ficam_na_raiz_e_sincronizados` |
| README com instrucoes de execucao e locais dos arquivos | `README.md` | `test_readme_cobre_itens_administrativos_e_semanticos` |
| Varredura completa do arquivo | Diagnosticos acumulados e `docs/estrategia_diagnosticos_acumulados.md` | `test_cli_varre_arquivo_inteiro_e_lista_multiplos_erros` |
| Tabela de simbolos | `generated/tabela_simbolos_ultima_execucao.json` e `docs/tabela_simbolos.md` | `test_pipeline_semantico_end_to_end_em_memoria` |
| Arvore sintatica atribuida | `generated/arvore_atribuida_ultima_execucao.json` e `docs/arvore_atribuida_ultima_execucao.md` | `test_pipeline_semantico_end_to_end_em_memoria` |
| Arvore sintatica desenhada no console | Saida padrao de programas validos imprime raiz, ramos e folhas em ASCII | `test_cli_processa_programa_valido_e_atualiza_artefatos` |
| Assembly apenas para programa valido | `generated/ultimo_assembly.s` | `test_semantico_bloqueia_assembly_com_erro`, `test_programa_invalido_bloqueia_assembly_e_grava_marcador` |
| Assembly nao impresso no console | CLI apenas confirma caminho do arquivo | `test_cli_processa_programa_valido_e_atualiza_artefatos` |
| Compatibilidade CPulator ARMv7 | Diretivas ARMv7, `_start`, JTAG UART e rotinas aritmeticas em `generated/ultimo_assembly.s` | `test_programas_validos_geram_assembly_armv7_cpulator`, `test_operadores_especificos_usam_rotinas_runtime_esperadas` |

## Comando de auditoria

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Resultado esperado para fechamento da etapa: todos os testes `OK`, arquivos validos gerando Assembly e `teste4_semantico_invalido.txt` bloqueando Assembly com erros semanticos claros.
