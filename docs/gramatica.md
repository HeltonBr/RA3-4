# Gramatica Canonica LL(1)

A linguagem da Fase 3 preserva a analise preditiva LL(1), o estilo pos-fixado e acrescenta os pontos semanticos necessarios para tipos, comentarios e geracao segura de Assembly.

## Observacoes de projeto

- Leitura de memoria e sempre canonica na forma `(MEM)`.
- Gravacao em memoria continua na forma `(<item> MEM)`.
- Literais logicos sao `TRUE` e `FALSE`.
- Operadores logicos sao `AND`, `OR` e `NOT`.
- Isso evita o uso de identificadores soltos como operandos e elimina conflitos na tabela LL(1).
- `START` e `END` aparecem apenas no topo do programa.

## BNF operacional

```text
program ::= start_line program_body
start_line ::= LPAREN KW_START RPAREN EOL
program_body ::= LPAREN program_body_after_lparen
program_body_after_lparen ::= KW_END RPAREN EOL EOF | stmt_inner RPAREN EOL program_body
stmt ::= LPAREN stmt_inner RPAREN
stmt_inner ::= IDENTIFIER | item stmt_after_first
item ::= NUMBER | BOOL_LITERAL | stmt
stmt_after_first ::= KW_RES | IDENTIFIER | OP_NOT | item stmt_after_second
stmt_after_second ::= binary_op | relational_op | logical_op | KW_IF | KW_WHILE | KW_SEQ | item KW_IFELSE
binary_op ::= OP_PLUS | OP_MINUS | OP_MULT | OP_REAL_DIV | OP_INT_DIV | OP_MOD | OP_POW
relational_op ::= OP_GT | OP_LT | OP_GTE | OP_LTE | OP_EQ | OP_NEQ
logical_op ::= OP_AND | OP_OR
```

## EBNF equivalente

```text
program        = start_line , program_body ;
start_line     = LPAREN , KW_START , RPAREN , EOL ;
program_body   = LPAREN , ( KW_END , RPAREN , EOL , EOF
                          | stmt_inner , RPAREN , EOL , program_body ) ;
stmt           = LPAREN , stmt_inner , RPAREN ;
stmt_inner     = IDENTIFIER | item , stmt_after_first ;
item           = NUMBER | BOOL_LITERAL | stmt ;
stmt_after_first = KW_RES | IDENTIFIER | OP_NOT | item , stmt_after_second ;
stmt_after_second = binary_op | relational_op | logical_op | KW_IF | KW_WHILE | KW_SEQ | item , KW_IFELSE ;
logical_op     = OP_AND | OP_OR ;
```

