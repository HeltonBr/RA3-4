# Arvore Sintatica da Ultima Execucao

```text
Program
  Statement[1] line=3
    MemoryWrite name=N
      Number value=12
  Statement[2] line=4
    MemoryWrite name=D
      Number value=4
  Statement[3] line=5
    MemoryWrite name=TAXA
      Number value=3.25
  Statement[4] line=6
    MemoryWrite name=ATIVO
      Bool value=TRUE
  Statement[5] line=9
    BinaryOp operator=+
      MemoryRead name=N
      MemoryRead name=D
  Statement[6] line=10
    BinaryOp operator=-
      BinaryOp operator=+
        MemoryRead name=N
        MemoryRead name=D
      Number value=2
  Statement[7] line=11
    BinaryOp operator=+
      BinaryOp operator=*
        MemoryRead name=N
        Number value=2
      BinaryOp operator=*
        MemoryRead name=D
        Number value=3
  Statement[8] line=12
    BinaryOp operator=/
      Number value=27
      Number value=5
  Statement[9] line=13
    BinaryOp operator=|
      Number value=27.0
      Number value=5
  Statement[10] line=14
    BinaryOp operator=%
      Number value=27
      Number value=5
  Statement[11] line=15
    BinaryOp operator=^
      MemoryRead name=D
      Number value=2
  Statement[12] line=16
    BinaryOp operator=+
      ResultRef offset=2
      ResultRef offset=1
  Statement[13] line=17
    LogicalOp operator=AND
      RelationalOp operator=>=
        MemoryRead name=N
        MemoryRead name=D
      MemoryRead name=ATIVO
  Statement[14] line=18
    LogicalOp operator=OR
      RelationalOp operator=<
        MemoryRead name=N
        MemoryRead name=D
      LogicalNot
        MemoryRead name=ATIVO
  Statement[15] line=19
    RelationalOp operator=>
      MemoryRead name=N
      MemoryRead name=D
  Statement[16] line=20
    RelationalOp operator=<=
      MemoryRead name=N
      MemoryRead name=D
  Statement[17] line=21
    RelationalOp operator===
      MemoryRead name=N
      MemoryRead name=D
  Statement[18] line=22
    RelationalOp operator=!=
      MemoryRead name=N
      MemoryRead name=D
  Statement[19] line=23
    If
      Condition
        LogicalOp operator=AND
          RelationalOp operator=>
            MemoryRead name=N
            MemoryRead name=D
          MemoryRead name=ATIVO
      Then
        MemoryWrite name=N
          BinaryOp operator=-
            MemoryRead name=N
            MemoryRead name=D
  Statement[20] line=24
    IfElse
      Condition
        RelationalOp operator=>=
          MemoryRead name=N
          MemoryRead name=D
      Then
        MemoryWrite name=N
          BinaryOp operator=-
            MemoryRead name=N
            MemoryRead name=D
      Else
        MemoryWrite name=D
          BinaryOp operator=+
            MemoryRead name=D
            Number value=1
  Statement[21] line=25
    Sequence
      MemoryWrite name=N
        BinaryOp operator=-
          MemoryRead name=N
          Number value=1
      MemoryWrite name=D
        BinaryOp operator=+
          MemoryRead name=D
          Number value=1
  Statement[22] line=26
    While
      Condition
        RelationalOp operator=>
          MemoryRead name=N
          Number value=0
      Body
        MemoryWrite name=N
          BinaryOp operator=-
            MemoryRead name=N
            Number value=1
```
