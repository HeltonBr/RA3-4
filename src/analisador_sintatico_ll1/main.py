# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from analisador_sintatico_ll1.ast_nodes import AstNode
from analisador_sintatico_ll1.ast_nodes import BinaryOpNode
from analisador_sintatico_ll1.ast_nodes import BoolNode
from analisador_sintatico_ll1.ast_nodes import IfNode
from analisador_sintatico_ll1.ast_nodes import LogicalNotNode
from analisador_sintatico_ll1.ast_nodes import LogicalOpNode
from analisador_sintatico_ll1.ast_nodes import MemoryReadNode
from analisador_sintatico_ll1.ast_nodes import MemoryWriteNode
from analisador_sintatico_ll1.ast_nodes import NumberNode
from analisador_sintatico_ll1.ast_nodes import ProgramNode
from analisador_sintatico_ll1.ast_nodes import RelationalOpNode
from analisador_sintatico_ll1.ast_nodes import ResultRefNode
from analisador_sintatico_ll1.ast_nodes import SequenceNode
from analisador_sintatico_ll1.ast_nodes import WhileNode
from analisador_sintatico_ll1.attributed_ast import render_attributed_markdown
from analisador_sintatico_ll1.core import construirTabelaSimbolos
from analisador_sintatico_ll1.core import gerarAssembly
from analisador_sintatico_ll1.core import gerarArvoreAtribuida
from analisador_sintatico_ll1.core import prepararEntradaSemanticaComDiagnosticos
from analisador_sintatico_ll1.core import salvar_tokens_em_arquivo
from analisador_sintatico_ll1.diagnostics import AnalysisDiagnostic
from analisador_sintatico_ll1.diagnostics import render_analysis_diagnostics
from analisador_sintatico_ll1.diagnostics import render_console_diagnostics
from analisador_sintatico_ll1.errors import AnalisadorSintaticoError
from analisador_sintatico_ll1.grammar import salvar_documentacao_gramatica
from analisador_sintatico_ll1.type_system import SemanticAnalysisResult


@dataclass
class PipelineExecution:
    generated_dir: Path
    semantic_result: SemanticAnalysisResult
    diagnostics: list[AnalysisDiagnostic]
    report: "ExecutionReport"
    tree_text: str


@dataclass
class ExecutionReport:
    source_path: Path
    statement_count: int
    symbol_count: int
    max_depth: int
    binary_ops: set[str]
    relational_ops: set[str]
    logical_ops: set[str]
    has_integer_literal: bool
    has_real_literal: bool
    has_bool_literal: bool
    has_memory_read: bool
    has_memory_write: bool
    has_res: bool
    has_if: bool
    has_ifelse: bool
    has_while: bool
    has_seq: bool
    comments: dict[str, int]
    diagnostic_counts: dict[str, int]
    assembly_generated: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analisador semantico da Fase 3 para a linguagem RPN LL(1)."
    )
    parser.add_argument("arquivo", type=Path, help="Arquivo-fonte do programa ou arquivo de tokens serializados.")
    parser.add_argument(
        "--mostrar-arvore",
        action="store_true",
        help="Mostra a arvore sintatica desenhada no console. Em programas validos ela ja aparece por padrao.",
    )
    parser.add_argument(
        "--relatorio-completo",
        action="store_true",
        help="Mostra o relatorio de validacao e a arvore sintatica desenhada no console.",
    )
    return parser


def executar_pipeline(arquivo: Path) -> PipelineExecution:
    repo_root = Path(__file__).resolve().parents[2]
    generated_dir = repo_root / "generated"
    docs_dir = repo_root / "docs"

    entrada = prepararEntradaSemanticaComDiagnosticos(str(arquivo))
    resultado_semantico = construirTabelaSimbolos(entrada)
    arvore_atribuida = gerarArvoreAtribuida(entrada, resultado_semantico, resultado_semantico)
    diagnostics = [*entrada.diagnostics, *_semantic_diagnostics_to_analysis(resultado_semantico)]
    report = _build_execution_report(
        arquivo,
        entrada.program,
        resultado_semantico,
        diagnostics,
        assembly_generated=not diagnostics,
    )

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
    (generated_dir / "relatorio_execucao_ultima_execucao.txt").write_text(
        render_execution_report(report),
        encoding="utf-8",
    )
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
        report=report,
        tree_text=entrada.syntax_tree["tree_text"],
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


def _build_execution_report(
    source_path: Path,
    program: ProgramNode,
    semantic_result: SemanticAnalysisResult,
    diagnostics: list[AnalysisDiagnostic],
    assembly_generated: bool,
) -> ExecutionReport:
    inventory = _inventariar_programa(program)
    diagnostic_counts = {"LEXICO": 0, "SINTATICO": 0, "SEMANTICO": 0}
    for diagnostic in diagnostics:
        diagnostic_counts[diagnostic.kind] = diagnostic_counts.get(diagnostic.kind, 0) + 1

    return ExecutionReport(
        source_path=source_path,
        statement_count=len(program.statements),
        symbol_count=len(semantic_result.symbol_table.symbols),
        max_depth=inventory["max_depth"],
        binary_ops=inventory["binary_ops"],
        relational_ops=inventory["relational_ops"],
        logical_ops=inventory["logical_ops"],
        has_integer_literal=inventory["has_integer_literal"],
        has_real_literal=inventory["has_real_literal"],
        has_bool_literal=inventory["has_bool_literal"],
        has_memory_read=inventory["has_memory_read"],
        has_memory_write=inventory["has_memory_write"],
        has_res=inventory["has_res"],
        has_if=inventory["has_if"],
        has_ifelse=inventory["has_ifelse"],
        has_while=inventory["has_while"],
        has_seq=inventory["has_seq"],
        comments=_inventariar_comentarios(source_path),
        diagnostic_counts=diagnostic_counts,
        assembly_generated=assembly_generated,
    )


def _inventariar_programa(program: ProgramNode) -> dict[str, object]:
    inventory = {
        "binary_ops": set(),
        "relational_ops": set(),
        "logical_ops": set(),
        "has_integer_literal": False,
        "has_real_literal": False,
        "has_bool_literal": False,
        "has_memory_read": False,
        "has_memory_write": False,
        "has_res": False,
        "has_if": False,
        "has_ifelse": False,
        "has_while": False,
        "has_seq": False,
        "max_depth": 0,
    }
    for statement in program.statements:
        _visit_node(statement.node, inventory, depth=1)
    return inventory


def _visit_node(node: AstNode, inventory: dict[str, object], depth: int) -> None:
    inventory["max_depth"] = max(inventory["max_depth"], depth)

    if isinstance(node, NumberNode):
        if node.is_integer_literal:
            inventory["has_integer_literal"] = True
        else:
            inventory["has_real_literal"] = True
        return

    if isinstance(node, BoolNode):
        inventory["has_bool_literal"] = True
        return

    if isinstance(node, MemoryReadNode):
        inventory["has_memory_read"] = True
        return

    if isinstance(node, ResultRefNode):
        inventory["has_res"] = True
        return

    if isinstance(node, MemoryWriteNode):
        inventory["has_memory_write"] = True
        _visit_node(node.value, inventory, depth + 1)
        return

    if isinstance(node, BinaryOpNode):
        inventory["binary_ops"].add(node.operator)
        _visit_node(node.left, inventory, depth + 1)
        _visit_node(node.right, inventory, depth + 1)
        return

    if isinstance(node, RelationalOpNode):
        inventory["relational_ops"].add(node.operator)
        _visit_node(node.left, inventory, depth + 1)
        _visit_node(node.right, inventory, depth + 1)
        return

    if isinstance(node, LogicalOpNode):
        inventory["logical_ops"].add(node.operator)
        _visit_node(node.left, inventory, depth + 1)
        _visit_node(node.right, inventory, depth + 1)
        return

    if isinstance(node, LogicalNotNode):
        inventory["logical_ops"].add("NOT")
        _visit_node(node.operand, inventory, depth + 1)
        return

    if isinstance(node, SequenceNode):
        inventory["has_seq"] = True
        _visit_node(node.first, inventory, depth + 1)
        _visit_node(node.second, inventory, depth + 1)
        return

    if isinstance(node, IfNode):
        inventory["has_if"] = True
        if node.else_branch is not None:
            inventory["has_ifelse"] = True
        _visit_node(node.condition, inventory, depth + 1)
        _visit_node(node.then_branch, inventory, depth + 1)
        if node.else_branch is not None:
            _visit_node(node.else_branch, inventory, depth + 1)
        return

    if isinstance(node, WhileNode):
        inventory["has_while"] = True
        _visit_node(node.condition, inventory, depth + 1)
        _visit_node(node.body, inventory, depth + 1)
        return


def _inventariar_comentarios(source_path: Path) -> dict[str, int]:
    try:
        text = source_path.read_text(encoding="utf-8")
    except OSError:
        return {"linha_inteira": 0, "fim_de_linha": 0, "entre_tokens": 0, "multilinha": 0}

    counts = {"linha_inteira": 0, "fim_de_linha": 0, "entre_tokens": 0, "multilinha": 0}
    for match in re.finditer(r"\*\{.*?\}\*", text, flags=re.DOTALL):
        comment = match.group(0)
        before_line = text[text.rfind("\n", 0, match.start()) + 1 : match.start()]
        after_line_end = text.find("\n", match.end())
        if after_line_end == -1:
            after_line_end = len(text)
        after_line = text[match.end() : after_line_end]

        if "\n" in comment:
            counts["multilinha"] += 1
        elif not before_line.strip() and not after_line.strip():
            counts["linha_inteira"] += 1
        elif before_line.strip() and not after_line.strip():
            counts["fim_de_linha"] += 1
        else:
            counts["entre_tokens"] += 1
    return counts


def render_execution_report(report: ExecutionReport) -> str:
    lines = [
        "Relatorio de validacao da execucao",
        f"- Arquivo analisado: {report.source_path}",
        "- Fases executadas:",
        f"  - Lexico: {_phase_status(report.diagnostic_counts.get('LEXICO', 0))}",
        f"  - Sintatico LL(1): {_phase_status(report.diagnostic_counts.get('SINTATICO', 0))}",
        f"  - Semantico: {_phase_status(report.diagnostic_counts.get('SEMANTICO', 0))}",
        f"- Declaracoes reconhecidas: {report.statement_count}",
        f"- Simbolos na tabela: {report.symbol_count}",
        f"- Profundidade maxima da AST: {report.max_depth}",
        "- Caracteristicas detectadas:",
        f"  - Operadores aritmeticos: {_format_set(report.binary_ops, ['+', '-', '*', '|', '/', '%', '^'])}",
        f"  - Operadores relacionais: {_format_set(report.relational_ops, ['>', '<', '>=', '<=', '==', '!='])}",
        f"  - Operadores logicos: {_format_set(report.logical_ops, ['AND', 'OR', 'NOT'])}",
        f"  - Literais: {_format_flags([('int', report.has_integer_literal), ('real', report.has_real_literal), ('bool', report.has_bool_literal)])}",
        f"  - Memoria e RES: {_format_flags([('(MEM)', report.has_memory_read), ('(V MEM)', report.has_memory_write), ('(N RES)', report.has_res)])}",
        f"  - Controle: {_format_flags([('IF', report.has_if), ('IFELSE', report.has_ifelse), ('WHILE', report.has_while), ('SEQ', report.has_seq)])}",
        f"  - Comentarios: {_format_comments(report.comments)}",
        f"- Assembly ARMv7: {'gerado em generated/ultimo_assembly.s' if report.assembly_generated else 'nao gerado por erros na analise'}",
        "- Observacao: o Assembly nao e impresso no console; consulte o arquivo gerado quando aplicavel.",
    ]
    return "\n".join(lines) + "\n"


def _phase_status(error_count: int) -> str:
    return "OK" if error_count == 0 else f"COM {error_count} ERRO(S)"


def _format_set(found: set[str], order: list[str]) -> str:
    present = [item for item in order if item in found]
    missing = [item for item in order if item not in found]
    if not present:
        return "nenhum detectado"
    text = " ".join(present)
    if missing:
        text += " | ausentes: " + " ".join(missing)
    return text


def _format_flags(items: list[tuple[str, bool]]) -> str:
    return ", ".join(f"{label}={'sim' if enabled else 'nao'}" for label, enabled in items)


def _format_comments(comments: dict[str, int]) -> str:
    return (
        f"linha inteira={comments.get('linha_inteira', 0)}, "
        f"fim de linha={comments.get('fim_de_linha', 0)}, "
        f"entre tokens={comments.get('entre_tokens', 0)}, "
        f"multilinha={comments.get('multilinha', 0)}"
    )


def main() -> int:
    args = build_parser().parse_args()
    try:
        execution = executar_pipeline(args.arquivo)
        print(f"Analise concluida para: {args.arquivo}")
        print(f"Artefatos atualizados em: {execution.generated_dir}")
        print(render_execution_report(execution.report).rstrip())
        if execution.report.assembly_generated or args.mostrar_arvore or args.relatorio_completo:
            print("Arvore sintatica desenhada:")
            print(execution.tree_text.rstrip())
        if execution.diagnostics:
            # Mantem relatorio e diagnosticos no mesmo fluxo para preservar ordem no PowerShell.
            for line in render_console_diagnostics(execution.diagnostics).splitlines():
                print(line, flush=True)
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
