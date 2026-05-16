# Auditoria Assembly e CPulator - Fase 3

## Escopo

Esta auditoria corresponde ao PR 08 planejado para a Fase 3. O objetivo e garantir que a geracao de Assembly so ocorra para programas validos, que programas invalidos deixem evidencia clara de bloqueio, e que o arquivo `generated/ultimo_assembly.s` tenha a estrutura esperada para o CPulator ARMv7 DE1-SoC.

## Pontos auditados

| Ponto | Tratamento adotado | Evidencia |
| --- | --- | --- |
| Assembly apenas para validos | `AnalisadorSemantico.py` gera `generated/ultimo_assembly.s` somente quando nao existem erros lexicos, sintaticos ou semanticos. | `tests/test_auditoria_assembly_cpulator.py` |
| Bloqueio em invalidos | Quando ha erro, `ultimo_assembly.s` recebe apenas marcador textual e nao contem `_start` nem diretivas de programa ARM. | `test_programa_invalido_bloqueia_assembly_e_grava_marcador` |
| Cabecalho ARMv7 | O Assembly valido contem `.syntax unified`, `.arch armv7-a`, `.fpu vfpv3`, `.global _start`, secao `.text` e `_start`. | `test_programas_validos_geram_assembly_armv7_cpulator` |
| Saida no CPulator | A rotina JTAG UART usa endereco `0xFF201000` e labels `jtag_putc`, `puts_jtag`, `print_qword_hex_d0` e `print_newline`. | `codegen_arm.py`, `test_programas_validos_geram_assembly_armv7_cpulator` |
| Rotinas aritmeticas | `/` e `//` usam `intdiv_double`, `%` usa `mod_double`, `^` usa `pow_double_int`, e expoente `0` cai em `pow_double_int_zero`. | `test_operadores_especificos_usam_rotinas_runtime_esperadas` |
| Console limpo | O CLI confirma o caminho do Assembly, mas nao despeja o codigo no console. | `test_programas_validos_geram_assembly_armv7_cpulator` |

## Roteiro manual CPulator

1. Executar `python AnalisadorSemantico.py teste3.txt`.
2. Abrir `generated/ultimo_assembly.s`.
3. Carregar o conteudo no CPulator em ARMv7 DE1-SoC.
4. Conferir que o programa contem `_start`, loop final `program_end` e rotinas JTAG UART.
5. Executar e observar saidas em hexadecimal prefixadas por `L<n>: 0x`, uma por declaracao processada.

## Validacao manual no CPulator

Validacao realizada em 15/05/2026 com o Assembly gerado por `teste3.txt`.

Resultado de compilacao no CPulator:

```text
CPUlator has started with system ARMv7 DE1-SoC containing a ARMv7 processor.
Compiling...
Code and data loaded from ELF executable into memory. Total size is 3984 bytes.
Assemble: arm-eabi-as -mfloat-abi=softfp -march=armv7-a -mcpu=cortex-a9 -mfpu=neon-fp16 --gdwarf2
Link: arm-eabi-ld --script build_arm.ld -e _start -u _start
Compile succeeded.
```

Resultado observado no JTAG UART: foram emitidas linhas `L3` a `L26`, cada uma no formato `L<n>: 0x...`, confirmando que o programa entrou em `_start`, avaliou as 22 declaracoes do arquivo valido, imprimiu os resultados por linha e permaneceu no loop final `program_end`.

## Decisao de entrega

O Assembly e artefato de saida, nao log de console. A saida padrao deve mostrar relatorio, arvore sintatica desenhada e confirmacao do caminho gerado. Para programa invalido, a entrega preserva os demais artefatos de diagnostico, mas bloqueia o Assembly executavel.
