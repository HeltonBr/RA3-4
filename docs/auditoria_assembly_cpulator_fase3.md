# Auditoria Assembly e CPulator - Fase 3

Esta auditoria registra a regra final para geracao ARMv7, usando somente os arquivos oficiais publicados na raiz da entrega.

## Regras

| Ponto | Tratamento adotado | Evidencia |
| --- | --- |
| Assembly apenas para validos | `AnalisadorSemantico.py` gera `generated/ultimo_assembly.s` somente quando nao existem erros lexicos, sintaticos ou semanticos. | `funcoes_teste_fase3.py`, `teste1.txt`, `teste2.txt`, `teste3.txt` |
| Bloqueio em invalidos | Quando ha erro, a execucao registra o bloqueio no console e nos relatorios, mas nao sobrescreve o Assembly valido final da entrega. | `teste4_semantico_invalido.txt`, `teste5_lexico_invalido.txt`, `teste6_sintatico_invalido.txt` |
| Cabecalho ARMv7 | O Assembly valido contem diretivas e simbolos compativeis com ARMv7 DE1-SoC. | `generated/ultimo_assembly.s` |
| Saida no CPulator | A rotina JTAG UART usa endereco `0xFF201000` e rotinas de impressao hexadecimal. | `generated/ultimo_assembly.s` e validacao manual no CPulator |
| Console limpo | O CLI confirma o caminho do Assembly, mas nao despeja o codigo no console. | `generated/relatorio_execucao_ultima_execucao.txt` |

## Sequencia de validacao antes do CPulator

```powershell
python funcoes_teste_fase3.py
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py teste5_lexico_invalido.txt
python AnalisadorSemantico.py teste6_sintatico_invalido.txt
python AnalisadorSemantico.py teste3.txt
```

O `teste3.txt` deve ser executado por ultimo para manter `generated/ultimo_assembly.s` e `generated/relatorio_execucao_ultima_execucao.txt` alinhados com um programa semanticamente valido.

## Roteiro CPulator

1. Confirmar que a sequencia de validacao terminou em `teste3.txt`.
2. Abrir `generated/ultimo_assembly.s`.
3. Colar o Assembly no CPulator ARMv7 DE1-SoC.
4. Compilar e executar.
5. Conferir a saida JTAG UART.

Validacao manual registrada: o Assembly produzido por `teste3.txt` compila no CPulator e gera saida compativel com os resultados esperados.
