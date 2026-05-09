# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from analisador_sintatico_ll1.attributed_ast import render_attributed_markdown
from analisador_sintatico_ll1.core import construirTabelaSimbolos
from analisador_sintatico_ll1.core import gerarAssembly
from analisador_sintatico_ll1.core import gerarArvoreAtribuida
from analisador_sintatico_ll1.core import prepararEntradaSemanticaComDiagnosticos
from analisador_sintatico_ll1.core import salvar_tokens_em_arquivo
from analisador_sintatico_ll1.diagnostics import AnalysisDiagnostic
from analisador_sintatico_ll1.diagnostics import render_analysis_diagnostics
from analisador_sintatico_ll1.errors import AnalisadorSintaticoError
from analisador_sintatico_ll1.grammar import salvar_documentacao_gramatica
from analisador_sintatico_ll1.type_system import SemanticAnalysisResult


@dataclass
class PipelineExecution:
    generated_dir: Path
    semantic_result: SemanticAnalysisResult
    diagnostics: list[AnalysisDiagnostic]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analisador semantico da Fase 3 para a linguagem RPN LL(1)."
    )
    parser.add_argument("arquivo", type=Path, help="Arquivo-fonte do programa ou arquivo de tokens serializados.")
    return parser


def executar_pipeline(arquivo: Path) -> PipelineExecution:
    repo_root = Path(__file__).resolve().parents[2]
    generated_dir = repo_root / "generated"
    docs_dir = repo_root / "docs"

    entrada = prepararEntradaSemanticaComDiagnosticos(str(arquivo))
    resultado_semantico = construirTabelaSimbolos(entrada)
    arvore_atribuida = gerarArvoreAtribuida(entrada, resultado_semantico, resultado_semantico)
    diagnostics = [*entrada.diagnostics, *_semantic_diagnostics_to_analysis(resultado_semantico)]

    generated_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    salvar_tokens_em_arquivo(entrada.tokens, generated_dir / "tokens_ultima_execucao.txt")
    (generated_dir / "arvore_ultima_execucao.json").write_text(
        json.dumps(entrada.syntax_tree["program"], ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    (generated_dir / "tabela_simbolos_ultima_execucao.json").write_text(
        json.dumps(resultado_semantico.symbol_table.to_dict(), ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    (generated_dir / "arvore_atribuida_ultima_execucao.json").write_text(
        json.dumps(arvore_atribuida.to_dict(), ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    relatorio_erros = render_analysis_diagnostics(diagnostics)
    (generated_dir / "relatorio_erros_ultima_execucao.txt").write_text(relatorio_erros, encoding="utf-8")
    (docs_dir / "arvore_ultima_execucao.md").write_text(
        "# Arvore Sintatica da Ultima Execucao\n\n```text\n"
        + entrada.syntax_tree["tree_text"].rstrip()
        + "\n```\n",
        encoding="utf-8",
    )
    (docs_dir / "tabela_simbolos.md").write_text(resultado_semantico.symbol_table.render_markdown(), encoding="utf-8")
    (docs_dir / "arvore_atribuida_ultima_execucao.md").write_text(
        render_attributed_markdown(arvore_atribuida),
        encoding="utf-8",
    )
    (docs_dir / "relatorio_erros_semanticos.md").write_text(
        "# Relatorio de Erros Semanticos\n\n```text\n" + relatorio_erros.rstrip() + "\n```\n",
        encoding="utf-8",
    )
    salvar_documentacao_gramatica(entrada.grammar, docs_dir)

    if diagnostics:
        (generated_dir / "ultimo_assembly.s").write_text(
            "@ Assembly nao gerado: a ultima execucao possui erros lexicos, sintaticos ou semanticos.\n",
            encoding="utf-8",
        )
    else:
        assembly = gerarAssembly(arvore_atribuida)
        (generated_dir / "ultimo_assembly.s").write_text(assembly, encoding="utf-8")

    return PipelineExecution(
        generated_dir=generated_dir,
        semantic_result=resultado_semantico,
        diagnostics=diagnostics,
    )


def _semantic_diagnostics_to_analysis(resultado: SemanticAnalysisResult) -> list[AnalysisDiagnostic]:
    return [
        AnalysisDiagnostic(
            kind="SEMANTICO",
            code=error.code,
            line=error.line,
            column=error.column,
            message=error.message,
        )
        for error in resultado.errors
    ]


def main() -> int:
    args = build_parser().parse_args()
    try:
        execution = executar_pipeline(args.arquivo)
        print(f"Analise concluida para: {args.arquivo}")
        print(f"Artefatos atualizados em: {execution.generated_dir}")
        if execution.diagnostics:
            print(render_analysis_diagnostics(execution.diagnostics).rstrip(), file=sys.stderr)
            return 1
        print("Analise completa concluida: 0 erro(s).")
        print("Assembly ARMv7 gerado em: generated/ultimo_assembly.s")
        return 0
    except AnalisadorSintaticoError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - ultima barreira defensiva
        print(f"Erro inesperado: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
