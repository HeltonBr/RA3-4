# Relatorio de Validacao dos Arquivos Oficiais

Todos os arquivos-fonte de validacao da entrega ficam na raiz do projeto, no mesmo diretorio de `AnalisadorSemantico.py`.

## Arquivos

- `teste1.txt`: valido.
- `teste2.txt`: valido.
- `teste3.txt`: valido e usado como execucao canonica final.
- `teste4_semantico_invalido.txt`: invalido semanticamente, com erros intencionais.

## Comandos oficiais

```powershell
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py teste3.txt
```

## Criterios de aceite

- Arquivos validos concluem com lexico, sintatico LL(1) e semantico `OK`.
- O arquivo invalido lista erros com linha, coluna e detalhe.
- Programas invalidos nao geram Assembly.
- `teste3.txt` deve ser executado por ultimo para atualizar `generated/ultimo_assembly.s` e os demais artefatos canonicos.
