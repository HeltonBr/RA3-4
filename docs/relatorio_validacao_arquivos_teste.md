# Relatorio de Validacao dos Arquivos de Teste

## Objetivo

Este roteiro demonstra como validar os tres arquivos obrigatorios na mesma pasta do codigo-fonte e como conferir os artefatos produzidos.

## Comandos principais

```powershell
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste3.txt
```

Cada execucao deve apresentar:

- fases lexico, sintatico LL(1) e semantico;
- quantidade de declaracoes reconhecidas;
- quantidade de simbolos na tabela;
- profundidade maxima da AST;
- operadores, literais, memoria, `RES`, controle e comentarios detectados;
- confirmacao de Assembly gerado ou bloqueado.

## Arvore no console

```powershell
python AnalisadorSemantico.py teste3.txt --mostrar-arvore
```

A arvore tambem fica persistida em:

- `docs/arvore_ultima_execucao.md`;
- `generated/arvore_ultima_execucao.json`;
- `generated/arvore_atribuida_ultima_execucao.json`.

## Assembly

O Assembly nao e impresso no console. Para programas validos, o CLI confirma:

```text
Assembly ARMv7 gerado em: generated/ultimo_assembly.s
```

Para programas invalidos, o arquivo `generated/ultimo_assembly.s` recebe apenas uma mensagem de bloqueio, preservando a regra de nao gerar codigo a partir de entrada invalida.

## Testes automatizados

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

A suite valida que:

- `teste1.txt`, `teste2.txt` e `teste3.txt` existem na raiz;
- as copias da raiz e de `tests/` permanecem sincronizadas;
- a saida padrao nao despeja Assembly no console;
- a arvore pode ser impressa sob demanda;
- os erros continuam acumulados sem interromper no primeiro problema.
