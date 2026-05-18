# Auditoria Assembly e CPulator - Fase 3

Esta auditoria registra a regra final para geracao ARMv7.

## Regras

| Item | Evidencia |
| --- | --- |
| Assembly gerado apenas para programas validos | `teste1.txt`, `teste2.txt`, `teste3.txt` |
| Programa invalido bloqueia Assembly | `teste4_semantico_invalido.txt` |
| Ultimo Assembly valido preservado apos execucao invalida | `generated/ultimo_assembly.s` |
| Arquivo gerado usa ARMv7 DE1-SoC | Diretivas em `generated/ultimo_assembly.s` |
| Saida usa JTAG UART | Rotinas e labels em `generated/ultimo_assembly.s` |

## Roteiro CPulator

1. Executar `python AnalisadorSemantico.py teste3.txt`.
2. Abrir `generated/ultimo_assembly.s`.
3. Colar o Assembly no CPulator ARMv7 DE1-SoC.
4. Compilar e executar.
5. Conferir a saida JTAG UART.

Validacao manual registrada: o Assembly produzido por `teste3.txt` compila no CPulator e gera saida compativel com os resultados esperados.
