# Roteiro de Envio - Fase 3

Data final de congelamento: **25/05/2026 as 23:59**.

1. Confirmar o nome exato do grupo no Canvas.
2. Criar repositorio publico exclusivo da Fase 3.
3. Seguir o cronograma diario em `docs/cronograma_commits_prs_fase3.md`.
4. Abrir e fechar pull requests diarios ate **18/05/2026**.
5. Reservar **19/05/2026 a 25/05/2026** para a bateria pesada em `docs/bateria_pesada_testes_fase3.md`.
6. Rodar:

```powershell
python AnalisadorSemantico.py tests/teste3.txt
python -m unittest discover -s tests -p "test_*.py" -v
.\sincronizar_para_githubmirror.ps1
```

7. Conferir `generated/`, `docs/`, GitHub e `GitHubmirror`.
8. Fazer merge somente depois de README, testes e artefatos estarem coerentes.
9. Congelar a pasta principal local e o GitHub em **25/05/2026 as 23:59**.
