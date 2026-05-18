# Auditoria Semantica e de Tipos - Fase 3

Esta auditoria registra a situacao final da validacao semantica, com foco em tipos estaticos e fortes.

## Pontos verificados

| Regra | Evidencia |
| --- | --- |
| Variavel deve ser definida antes do uso | `teste4_semantico_invalido.txt` |
| Reatribuicao so e aceita com o mesmo tipo | `teste4_semantico_invalido.txt` |
| Operadores aritmeticos rejeitam combinacoes invalidas com `bool` | `teste4_semantico_invalido.txt` |
| `%`, `/` e `//` exigem operandos inteiros | `docs/regras_tipos_sequentes.md` e `teste4_semantico_invalido.txt` |
| `IF`, `IFELSE` e `WHILE` exigem condicao `bool` | `docs/regras_tipos_sequentes.md` |
| `RES` exige deslocamento positivo e referencia declaracao anterior valida | `docs/regras_tipos_sequentes.md` |
| Potenciacao aceita expoente inteiro; literal `0` e caso neutro/valido conforme orientacao do professor | `docs/regras_tipos_sequentes.md` |

## Decisao

Programas com erro lexico, sintatico ou semantico nao geram Assembly. A execucao invalida oficial deve acumular os erros recuperaveis e preservar o ultimo Assembly valido.
