# Roteiro de Defesa - Fase 3

## Demonstracao principal

```powershell
python AnalisadorSemantico.py tests/teste3.txt
```

Mostrar:

- `generated/tabela_simbolos_ultima_execucao.json`
- `generated/arvore_atribuida_ultima_execucao.json`
- `generated/ultimo_assembly.s`
- `docs/regras_tipos_sequentes.md`

## Demonstracao de erro

```powershell
python AnalisadorSemantico.py tests/invalidos/semantico_variavel_nao_definida.txt
python AnalisadorSemantico.py tests/invalidos/semantico_condicao_nao_bool.txt
python AnalisadorSemantico.py tests/invalidos/lexico_comentario_nao_fechado.txt
```

Pontos de fala:

- Toda mensagem indica tipo do erro, linha, coluna e causa.
- Erros semanticos sao acumulados quando possivel.
- Assembly so e emitido quando a arvore atribuida esta semanticamente valida.

## Frase guia

"A Fase 3 nao apenas reconhece a forma do programa. Ela valida significado: tabela de simbolos, tipos, condicoes booleanas, uso de memoria e `RES`. So depois disso a arvore atribuida pode alimentar o gerador ARMv7."
