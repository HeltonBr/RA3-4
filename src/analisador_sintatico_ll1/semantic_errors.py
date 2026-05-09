# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticDiagnostic:
    code: str
    line: int
    column: int
    message: str

    def format(self) -> str:
        return f"Erro SEMANTICO na linha {self.line}, coluna {self.column}: {self.message}"


def render_diagnostics(errors: list[SemanticDiagnostic]) -> str:
    if not errors:
        return "Analise semantica concluida: 0 erro(s).\n"

    linhas = [f"Analise semantica concluida com {len(errors)} erro(s):"]
    linhas.extend(error.format() for error in errors)
    linhas.append("Assembly nao gerado porque ha erros semanticos.")
    return "\n".join(linhas) + "\n"
