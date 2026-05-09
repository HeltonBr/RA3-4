# Sintaxe das Estruturas de Controle

## Convencoes

- Toda estrutura fica entre parenteses.
- A linguagem continua pos-fixada: os operandos aparecem antes do operador final.
- Leitura de memoria e sempre parentetizada, por exemplo `(X)`.

## Formas canonicas

```text
(<expr> <stmt> IF)
(<expr> <stmt> <stmt> IFELSE)
(<expr> <stmt> WHILE)
(<stmt> <stmt> SEQ)
(<expr> <expr> AND)
(<expr> <expr> OR)
(<expr> NOT)
```

## Exemplos

```text
(((X) 0 >) (((X) 1 -) X) WHILE)
(((X) (Y) >) (((X) (Y) +) Z) IF)
(((X) (Y) <) (((X) (Y) +) W) (((X) (Y) -) W) IFELSE)
((((X) 1 -) X) (((W) (X) +) W) SEQ)
(((X) 0 >) TRUE AND)
(((X) 0 ==) NOT)
```
