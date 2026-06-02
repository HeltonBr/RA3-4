# Auditoria do Dossie de Inconformidades - Fase 3

Este documento registra as decisoes finais adotadas para a entrega da Fase 3, ja considerando a especificacao revisada e os seis arquivos oficiais mantidos na raiz do projeto.

## Decisoes consolidadas

| Item | Decisao |
| --- | --- |
| Entrada do analisador | Sempre arquivo-fonte bruto passado por argumento de linha de comando. |
| Local dos arquivos de entrada | Somente a raiz do projeto, no mesmo diretorio de `AnalisadorSemantico.py`. |
| Arquivos oficiais validos | `teste1.txt`, `teste2.txt`, `teste3.txt`. |
| Arquivos oficiais invalidos | `teste4_semantico_invalido.txt`, `teste5_lexico_invalido.txt`, `teste6_sintatico_invalido.txt`. |
| Funcoes publicas de teste | `funcoes_teste_fase3.py`, tambem na raiz, exercita os arquivos oficiais sem criar subpastas de teste. |
| Comentarios | `*{ ... }*`, descartados pelo lexico, com preservacao de linha e coluna para diagnosticos. |
| Memoria | `(NOME)` para leitura e `(V NOME)` para escrita ou definicao. |
| Tipos | `int`, `real` e `bool`, com reatribuicao permitida apenas para o mesmo tipo. |
| Resultado anterior | `(N RES)` exige `N > 0` e referencia declaracao anterior valida. |
| Controle | Sintaxe pos-fixada para `IF`, `IFELSE`, `WHILE` e `SEQ`; condicoes devem ser `bool`. |
| Potenciacao | Expoente deve ser `int`; literal `0` e aceito como caso neutro/valido conforme orientacao do professor. |
| Assembly | Gerado somente quando nao ha erro lexico, sintatico ou semantico. |
| Testes invalidos | `teste4` cobre erros semanticos, incluindo condicoes invalidas em `IF` e `WHILE`; `teste5` cobre erros lexicos; `teste6` cobre erros sintaticos. |

## Sequencia de validacao

```powershell
python funcoes_teste_fase3.py
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py teste5_lexico_invalido.txt
python AnalisadorSemantico.py teste6_sintatico_invalido.txt
python AnalisadorSemantico.py teste3.txt
```

O `teste3.txt` deve ser executado por ultimo para deixar a arvore, a arvore atribuida, a tabela de simbolos, o relatorio de execucao e o Assembly alinhados com um programa semanticamente valido.
