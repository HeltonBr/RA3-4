# Auditoria Semantica e Tipos - Fase 3

## Escopo

Esta auditoria corresponde ao PR 07 planejado para a Fase 3. O objetivo e reduzir risco em regras semanticas, matriz de tipos, uso de memoria, `RES`, comandos de controle, potenciacao e acumulacao de diagnosticos.

## Pontos auditados nesta primeira rodada

| Ponto | Tratamento adotado | Evidencia |
| --- | --- | --- |
| Matriz numerica valida | `int + real` promove para `real`; `/`, `//` e `%` exigem `int`; `|` retorna `real`; `^` preserva tipo numerico da base. | `tests/test_auditoria_semantica_tipos.py` |
| Operadores invalidos | Aritmetica com `bool`, logicos sem `bool`, relacionais incompativeis e igualdade de tipos incompativeis geram erro semantico. | `test_matriz_invalida_acumula_erros_semanticos_de_tipos` |
| Controle | `IF`, `IFELSE` e `WHILE` exigem condicao `bool`; `WHILE` e `IF` sem `ELSE` retornam `void`. | `type_system.py`, `tests/test_auditoria_semantica_tipos.py` |
| `RES` | `N=0`, historico fora do alcance e referencia a comando `void` sao rejeitados. | `test_res_reatribuicao_e_comando_sem_valor_sao_rejeitados` |
| Potenciacao | Expoente deve ser `int`; por orientacao do professor, expoente literal `0` e aceito como inteiro positivo. | `type_system.py`, `docs/regras_tipos_sequentes.md` |

## Decisao sobre INC-17

Com a orientacao do professor, o analisador aceita `^` com expoente literal inteiro `0`, tratando esse valor como inteiro positivo para este projeto. A regra estatica implementavel fica assim:

```text
Gamma |- A : numeric    Gamma |- B : int
-----------------------------------------
Gamma |- (A B ^) : tipo(A)
```

Quando o expoente vem de memoria ou expressao, o analisador verifica o tipo `int`. Essa decisao evita falso bloqueio para programas que dependem de valores definidos em tempo de execucao e preserva a convencao confirmada de que `0` e inteiro positivo.

## Pendencias ainda abertas para o PR 07

- Ampliar testes de `IFELSE` com ramos numericos mistos e ramos incompativeis.
- Conferir mensagens do CLI para arquivo com muitos erros semanticos exclusivos.
- Atualizar matriz de cobertura final ligando cada regra semantica ao teste correspondente.
