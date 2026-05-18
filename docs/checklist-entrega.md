# Checklist de Entrega - Fase 3

## Estrutura

- [x] `AnalisadorSemantico.py` na raiz.
- [x] Entrada por argumento de linha de comando.
- [x] Sem menu interativo.
- [x] Arquivos oficiais na raiz: `teste1.txt`, `teste2.txt`, `teste3.txt`, `teste4_semantico_invalido.txt`.
- [x] Sem subpastas para arquivos-fonte de entrada da linguagem.

## Analise

- [x] Lexico integrado.
- [x] Parser LL(1) integrado.
- [x] Analise semantica com tabela de simbolos.
- [x] Regras de tipos documentadas.
- [x] Arvore sintatica atribuida gerada.
- [x] Diagnosticos com linha, coluna e detalhe.
- [x] Varredura completa dos erros recuperaveis.

## Artefatos

- [x] `generated/tokens_ultima_execucao.txt`.
- [x] `generated/arvore_ultima_execucao.json`.
- [x] `generated/tabela_simbolos_ultima_execucao.json`.
- [x] `generated/arvore_atribuida_ultima_execucao.json`.
- [x] `generated/relatorio_erros_ultima_execucao.txt`.
- [x] `generated/relatorio_execucao_ultima_execucao.txt`.
- [x] `generated/ultimo_assembly.s`.

## Fechamento

```powershell
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py teste3.txt
```

O `teste3.txt` fica por ultimo como execucao canonica valida.
