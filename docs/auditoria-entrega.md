# Auditoria Automatizada da Entrega - Fase 3

A suite em `tests/` verifica os itens com maior risco de penalizacao:

- funcoes exigidas expostas publicamente;
- tres arquivos validos com operadores, comentarios, controle, memoria e tipos;
- erros lexicos, sintaticos e semanticos sem traceback;
- varredura completa de arquivo invalido com multiplos erros no mesmo input;
- tabela de simbolos, arvore atribuida e relatorio de erros gerados;
- Assembly gerado apenas para programa semanticamente valido;
- README e documentos formais presentes.

Comando:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Ultima validacao local: 28 testes aprovados.
