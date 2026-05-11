# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisDiagnostic:
    kind: str
    code: str
    line: int
    column: int
    message: str

    def format(self) -> str:
        return f"Erro {self.kind} na linha {self.line}, coluna {self.column}: {self.message}"


def render_analysis_diagnostics(diagnostics: list[AnalysisDiagnostic]) -> str:
    if not diagnostics:
        return "Analise completa concluida: 0 erro(s).\n"

    sorted_diagnostics = sorted(diagnostics, key=lambda item: (item.line, item.column, item.kind, item.code))
    linhas = [f"Analise completa concluida com {len(sorted_diagnostics)} erro(s):"]
    linhas.extend(diagnostic.format() for diagnostic in sorted_diagnostics)
    linhas.append("Assembly nao gerado porque ha erros lexicos, sintaticos ou semanticos.")
    return "\n".join(linhas) + "\n"


def render_console_diagnostics(diagnostics: list[AnalysisDiagnostic]) -> str:
    if not diagnostics:
        return "Analise completa concluida: 0 erro(s).\n"

    sorted_diagnostics = sorted(diagnostics, key=lambda item: (item.line, item.column, item.kind, item.code))
    linhas = [f"Analise completa concluida com {len(sorted_diagnostics)} erro(s):"]
    for diagnostic in sorted_diagnostics:
        linhas.append(f"Erro {diagnostic.kind}")
        linhas.append(f"  linha: {diagnostic.line}")
        linhas.append(f"  coluna: {diagnostic.column}")
        linhas.append(f"  detalhe: {diagnostic.message}")
    linhas.append("Assembly nao gerado porque ha erros lexicos, sintaticos ou semanticos.")
    return "\n".join(linhas) + "\n"
