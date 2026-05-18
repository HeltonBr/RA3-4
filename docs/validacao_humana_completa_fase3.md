# Validacao Humana Completa - Fase 3

## Objetivo

Registrar uma linha de validacao humana para tudo que ja foi desenvolvido ate a etapa PR09. Esta linha combina execucoes manuais, entradas oficiais, entradas surpresa simulando prova de autoria, suite automatizada e conferencias de artefatos.

## Sequencia manual recomendada

Execute a partir da pasta `GitHub`:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python AnalisadorSemantico.py teste1.txt
python AnalisadorSemantico.py teste2.txt
python AnalisadorSemantico.py teste3.txt
python AnalisadorSemantico.py teste4_semantico_invalido.txt
python AnalisadorSemantico.py professor_surpresa_valido.txt
python AnalisadorSemantico.py professor_surpresa_invalido.txt
python AnalisadorSemantico.py teste3.txt
```

A ultima execucao de `teste3.txt` deve ser mantida para deixar `generated/ultimo_assembly.s` canonico e valido.

## Criterios de observacao humana

| Item | Resultado esperado |
| --- | --- |
| Suite automatizada | Todos os testes `OK`. |
| `teste1.txt`, `teste2.txt`, `teste3.txt` | Retorno `0`, lexico/sintatico/semantico `OK`, arvore sintatica desenhada e Assembly gerado. |
| `teste4_semantico_invalido.txt` | Retorno `1`, varios erros semanticos listados, sem traceback e Assembly bloqueado. |
| `professor_surpresa_valido.txt` | Programa diferente dos oficiais, com comentarios, `//`, expoente `0`, controle e memoria; deve gerar Assembly. |
| `professor_surpresa_invalido.txt` | Programa diferente dos oficiais, com erros semanticos acumulados; deve bloquear Assembly. |
| Console | Deve mostrar relatorio e arvore para validos, sem despejar o Assembly. |
| CPulator apos invalido | Um invalido nao deve sobrescrever `generated/ultimo_assembly.s`; o arquivo `.s` deve continuar sendo o ultimo Assembly valido. |
| `generated/` | Deve conter tokens, AST, arvore atribuida, tabela de simbolos, relatorios e `ultimo_assembly.s`. |

## Script auxiliar

O script `validar_linha_humana.ps1` executa a mesma sequencia e falha se algum comando retornar codigo diferente do esperado.

```powershell
powershell -ExecutionPolicy Bypass -File .\validar_linha_humana.ps1
```

## Resultado da etapa

Esta etapa deve terminar com:

- PR08 ja integrado na `main`;
- `GitHubmirror` sincronizado apos o merge do PR08;
- PR09 contendo entradas surpresa, roteiro de validacao humana e testes automatizados;
- `teste3.txt` executado por ultimo para manter artefatos canonicos.

Validacao executada em 16/05/2026:

- `powershell -ExecutionPolicy Bypass -File .\validar_linha_humana.ps1` concluido com sucesso;
- suite completa com 51 testes `OK`;
- `teste1.txt`, `teste2.txt`, `teste3.txt` e entrada surpresa valida geraram Assembly;
- `teste4_semantico_invalido.txt` e entrada surpresa invalida bloquearam Assembly;
- validacao manual detectou e corrigiu que entradas invalidas nao podem substituir `generated/ultimo_assembly.s` por marcador textual, pois isso causa falso positivo no CPulator;
- `teste3.txt` foi regenerado ao final como artefato canonico.
