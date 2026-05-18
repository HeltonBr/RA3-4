# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

"""Funcoes de teste publicas para a Fase 3.

Este arquivo fica na raiz para preservar a regra da entrega: todos os
arquivos oficiais de entrada da linguagem tambem ficam na raiz.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parent
ANALISADOR = RAIZ / "AnalisadorSemantico.py"


def executar_analisador(nome_arquivo: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ANALISADOR), nome_arquivo],
        cwd=RAIZ,
        text=True,
        capture_output=True,
        check=False,
    )


def exigir(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise AssertionError(mensagem)


def testar_programas_validos_da_raiz() -> None:
    for arquivo in ("teste1.txt", "teste2.txt", "teste3.txt"):
        resultado = executar_analisador(arquivo)
        saida = resultado.stdout + resultado.stderr
        exigir(resultado.returncode == 0, f"{arquivo} deveria ser valido.")
        exigir("Semantico: OK" in saida, f"{arquivo} deveria concluir semantica OK.")
        exigir("Assembly ARMv7 gerado" in saida, f"{arquivo} deveria gerar Assembly.")


def testar_programa_semantico_invalido_da_raiz() -> None:
    resultado = executar_analisador("teste4_semantico_invalido.txt")
    saida = resultado.stdout + resultado.stderr
    exigir(resultado.returncode != 0, "teste4 deveria falhar semanticamente.")
    exigir("Erro SEMANTICO" in saida, "teste4 deveria listar erro semantico.")
    exigir(
        "condicao de IF deve ser bool" in saida,
        "teste4 deveria acusar condicao invalida de IF.",
    )
    exigir(
        "condicao de WHILE deve ser bool" in saida,
        "teste4 deveria acusar condicao invalida de WHILE.",
    )
    exigir("Assembly nao gerado" in saida, "teste4 deveria bloquear Assembly.")


def testar_programa_lexico_invalido_da_raiz() -> None:
    resultado = executar_analisador("teste5_lexico_invalido.txt")
    saida = resultado.stdout + resultado.stderr
    exigir(resultado.returncode != 0, "teste5 deveria falhar no lexico.")
    exigir("Erro LEXICO" in saida, "teste5 deveria listar erro lexico.")
    exigir("Assembly nao gerado" in saida, "teste5 deveria bloquear Assembly.")


def testar_programa_sintatico_invalido_da_raiz() -> None:
    resultado = executar_analisador("teste6_sintatico_invalido.txt")
    saida = resultado.stdout + resultado.stderr
    exigir(resultado.returncode != 0, "teste6 deveria falhar no sintatico.")
    exigir("Erro SINTATICO" in saida, "teste6 deveria listar erro sintatico.")
    exigir("Assembly nao gerado" in saida, "teste6 deveria bloquear Assembly.")


def testar_teste3_como_execucao_canonica() -> None:
    resultado = executar_analisador("teste3.txt")
    saida = resultado.stdout + resultado.stderr
    relatorio = RAIZ / "generated" / "relatorio_execucao_ultima_execucao.txt"
    conteudo = relatorio.read_text(encoding="utf-8")
    exigir(resultado.returncode == 0, "teste3 deveria fechar a validacao com sucesso.")
    exigir("Assembly ARMv7 gerado" in saida, "teste3 deveria gerar Assembly.")
    exigir("Arquivo analisado: teste3.txt" in conteudo, "teste3 deve ser a execucao canonica final.")


def executar_funcoes_de_teste() -> None:
    testar_programas_validos_da_raiz()
    testar_programa_semantico_invalido_da_raiz()
    testar_programa_lexico_invalido_da_raiz()
    testar_programa_sintatico_invalido_da_raiz()
    testar_teste3_como_execucao_canonica()


if __name__ == "__main__":
    executar_funcoes_de_teste()
    print("Funcoes de teste da Fase 3 concluidas com sucesso.")
