# Estrategia de Diagnosticos Acumulados

Esta entrega evita a penalizacao de interromper a analise no primeiro problema encontrado. O CLI usa a funcao `prepararEntradaSemanticaComDiagnosticos`, que varre o arquivo completo e acumula erros por etapa.

## Como a varredura funciona

1. **Lexico:** percorre todas as linhas do arquivo-fonte, registra caracteres invalidos, numeros malformados, identificadores invalidos e comentarios nao fechados, mas continua examinando as proximas linhas quando ha recuperacao possivel.
2. **Sintatico:** tenta recuperar por declaracao de topo. Uma linha mal formada nao impede que as demais linhas sejam avaliadas.
3. **Semantico:** percorre a AST parcial/valida que foi possivel construir e acumula uso antes da definicao, incompatibilidade de tipos, `RES` invalido, condicao nao bool e reatribuicao incompativel.
4. **Assembly:** fica bloqueado quando ha qualquer erro lexico, sintatico ou semantico.

## Formato de saida

```text
Analise completa concluida com N erro(s):
Erro LEXICO
  linha: L
  coluna: C
  detalhe: ...
Erro SINTATICO
  linha: L
  coluna: C
  detalhe: ...
Erro SEMANTICO
  linha: L
  coluna: C
  detalhe: ...
Assembly nao gerado porque ha erros lexicos, sintaticos ou semanticos.
```

## Caso de auditoria

O arquivo `tests/invalidos/auditoria_multiplos_erros.txt` mistura erro lexico, sintatico e semantico no mesmo input. O teste automatizado correspondente exige que a saida liste todos eles, sem traceback e sem parar no primeiro erro.
