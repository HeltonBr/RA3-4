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
  Statement[5] line=7
    BinaryOp operator=+
      MemoryRead name=N
      MemoryRead name=D
  Statement[6] line=8
    BinaryOp operator=-
      BinaryOp operator=+
        MemoryRead name=N
        MemoryRead name=D
      Number value=2
  Statement[7] line=9
    BinaryOp operator=+
      BinaryOp operator=*
        MemoryRead name=N
        Number value=2
      BinaryOp operator=*
        MemoryRead name=D
        Number value=3
  Statement[8] line=10
    BinaryOp operator=/
      Number value=27
      Number value=5
  Statement[9] line=11
    BinaryOp operator=|
      Number value=27.0
      Number value=5
  Statement[10] line=12
    BinaryOp operator=%
      Number value=27
      Number value=5
  Statement[11] line=13
    BinaryOp operator=^
      MemoryRead name=D
      Number value=2
  Statement[12] line=14
    BinaryOp operator=+
      ResultRef offset=2
      ResultRef offset=1
  Statement[13] line=15
    LogicalOp operator=AND
      RelationalOp operator=>=
        MemoryRead name=N
        MemoryRead name=D
      MemoryRead name=ATIVO
  Statement[14] line=16
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
  Statement[15] line=17
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
