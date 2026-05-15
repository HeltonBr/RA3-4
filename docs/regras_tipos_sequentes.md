# Regras de Tipos em Calculo de Sequentes

Julgamento usado:

```text
Gamma |- expr : tipo
```

`Gamma` representa a tabela de simbolos do arquivo.

## Literais e memoria

```text
[T-INT]
----------------
Gamma |- n : int
quando n e literal inteiro

[T-REAL]
-----------------
Gamma |- r : real
quando r possui ponto decimal

[T-BOOL]
--------------------
Gamma |- TRUE : bool
Gamma |- FALSE : bool

[T-VAR]
Gamma(x) = T
----------------
Gamma |- (x) : T

[T-STORE]
Gamma |- V : T
Gamma(x) indefinido ou Gamma(x) = T
------------------------------------
Gamma |- (V x) : T
```

Variavel usada antes de definicao, ou reatribuida com tipo diferente, gera erro semantico.

## Aritmetica

```text
[T-ADD-SUB-MUL-INT]
Gamma |- A : int    Gamma |- B : int
------------------------------------
Gamma |- (A B op) : int
op em {+, -, *}

[T-ADD-SUB-MUL-REAL]
Gamma |- A : numeric    Gamma |- B : numeric    real em {tipo(A), tipo(B)}
---------------------------------------------------------------------------
Gamma |- (A B op) : real
op em {+, -, *}

[T-REAL-DIV]
Gamma |- A : numeric    Gamma |- B : numeric
--------------------------------------------
Gamma |- (A B |) : real

[T-INT-DIV]
Gamma |- A : int    Gamma |- B : int
------------------------------------
Gamma |- (A B /) : int
Gamma |- (A B //) : int

[T-MOD]
Gamma |- A : int    Gamma |- B : int
------------------------------------
Gamma |- (A B %) : int

[T-POW]
Gamma |- A : numeric    Gamma |- B : int
-----------------------------------------
Gamma |- (A B ^) : tipo(A)
```

`numeric` significa `int` ou `real`.

Na divisao inteira, `//` e aceito como alias de `/` e normalizado internamente para a mesma operacao na AST.

Na potenciacao, o analisador exige expoente `int`. Por orientacao do professor, o literal inteiro `0` e aceito como inteiro positivo nesta linguagem. Quando o expoente vem de memoria ou expressao, a verificacao estatica garante o tipo `int`.

## Relacionais e logicos

```text
[T-REL-ORDER]
Gamma |- A : numeric    Gamma |- B : numeric
--------------------------------------------
Gamma |- (A B rel) : bool
rel em {>, <, >=, <=}

[T-REL-EQ-NUM]
Gamma |- A : numeric    Gamma |- B : numeric
--------------------------------------------
Gamma |- (A B rel) : bool
rel em {==, !=}

[T-REL-EQ-BOOL]
Gamma |- A : bool    Gamma |- B : bool
--------------------------------------
Gamma |- (A B rel) : bool
rel em {==, !=}

[T-AND-OR]
Gamma |- A : bool    Gamma |- B : bool
--------------------------------------
Gamma |- (A B op) : bool
op em {AND, OR}

[T-NOT]
Gamma |- A : bool
------------------------
Gamma |- (A NOT) : bool
```

## Controle e RES

```text
[T-IF]
Gamma |- C : bool    Gamma |- S : T
-----------------------------------
Gamma |- (C S IF) : void

[T-IFELSE]
Gamma |- C : bool    Gamma |- S1 : T1    Gamma |- S2 : T2    compativel(T1, T2)
-------------------------------------------------------------------------------
Gamma |- (C S1 S2 IFELSE) : promover(T1, T2)

[T-WHILE]
Gamma |- C : bool    Gamma |- S : T
-----------------------------------
Gamma |- (C S WHILE) : void

[T-SEQ]
Gamma |- S1 : T1    Gamma |- S2 : T2
------------------------------------
Gamma |- (S1 S2 SEQ) : T2

[T-RES]
resultado(i - N) = T    N > 0    T != void
------------------------------------------
Gamma |- (N RES) : T
```

Programas com qualquer erro semantico nao seguem para geracao de Assembly.
