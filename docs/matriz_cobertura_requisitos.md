# Matriz de Cobertura dos Requisitos - Fase 3

Esta matriz registra a cobertura da entrega final usando apenas os arquivos-fonte oficiais que ficam na raiz do projeto, ao lado de `AnalisadorSemantico.py`.

## Arquivos oficiais

| Arquivo | Papel na entrega | Situacao |
| --- | --- | --- |
| `teste1.txt` | Programa semanticamente valido com operadores, memoria, `RES`, controle, tipos e comentarios. | Coberto |
| `teste2.txt` | Programa semanticamente valido com combinacoes alternativas de booleanos, controle e reatribuicoes validas. | Coberto |
| `teste3.txt` | Programa semanticamente valido usado como execucao canonica final dos artefatos. | Coberto |
| `teste4_semantico_invalido.txt` | Programa com erros semanticos intencionais para demonstrar diagnosticos acumulados e bloqueio de Assembly. | Coberto |

## Requisitos principais

| Requisito | Evidencia |
| --- | --- |
| Execucao por argumento, sem menu | `python AnalisadorSemantico.py teste1.txt` e demais arquivos oficiais da raiz |
| Arquivos de entrada no mesmo diretorio do codigo-fonte | `teste1.txt`, `teste2.txt`, `teste3.txt`, `teste4_semantico_invalido.txt` na raiz |
| Comentarios em posicoes diferentes | Arquivos validos oficiais e relatorio de execucao |
| Tabela de simbolos | `generated/tabela_simbolos_ultima_execucao.json` e `docs/tabela_simbolos.md` |
| Arvore sintatica atribuida | `generated/arvore_atribuida_ultima_execucao.json` e `docs/arvore_atribuida_ultima_execucao.md` |
| Arvore sintatica desenhada no console | Saida padrao dos programas validos |
| Diagnosticos acumulados | `teste4_semantico_invalido.txt` lista multiplos erros semanticos |
| Assembly apenas para programa valido | `generated/ultimo_assembly.s`, preservado para a ultima execucao valida |
| Compatibilidade CPulator ARMv7 | `docs/auditoria_assembly_cpulator_fase3.md` e `generated/ultimo_assembly.s` |

## Sequencia oficial de fechamento

```powershell
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py teste3.txt
```

Resultado esperado: `teste1.txt`, `teste2.txt` e `teste3.txt` concluem com lexico, sintatico e semantico `OK`; `teste4_semantico_invalido.txt` acumula erros semanticos e bloqueia Assembly; `teste3.txt` fica por ultimo como base canonica dos artefatos finais.
