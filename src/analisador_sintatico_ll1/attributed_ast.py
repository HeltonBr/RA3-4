# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass

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
from analisador_sintatico_ll1.ast_nodes import node_to_rpn_string
from analisador_sintatico_ll1.type_system import SemanticAnalysisResult
from analisador_sintatico_ll1.type_system import TYPE_ERROR


@dataclass
class AttributedAST:
    program: ProgramNode
    payload: dict[str, object]
    semantic_result: SemanticAnalysisResult

    def to_dict(self) -> dict[str, object]:
        return self.payload

    @property
    def has_errors(self) -> bool:
        return self.semantic_result.has_errors


def build_attributed_ast(result: SemanticAnalysisResult) -> AttributedAST:
    payload: dict[str, object] = {
        "type": "Program",
        "statement_count": len(result.program.statements),
        "semantic_status": "error" if result.has_errors else "ok",
        "statements": [
            {
                "ordinal": statement.ordinal,
                "source_line": statement.source_line,
                "inferred_type": result.statement_types.get(statement.ordinal, TYPE_ERROR),
                "rpn": node_to_rpn_string(statement.node),
                "tree": _node_to_attributed_dict(statement.node, result),
            }
            for statement in result.program.statements
        ],
    }
    return AttributedAST(program=result.program, payload=payload, semantic_result=result)


def render_attributed_markdown(attributed_ast: AttributedAST) -> str:
    linhas = [
        "# Arvore Sintatica Atribuida da Ultima Execucao",
        "",
        f"Status semantico: `{attributed_ast.payload['semantic_status']}`",
        "",
        "```text",
    ]
    for statement in attributed_ast.payload["statements"]:
        assert isinstance(statement, dict)
        linhas.append(
            f"Statement[{statement['ordinal']}] line={statement['source_line']} "
            f"type={statement['inferred_type']}"
        )
        _render_node(statement["tree"], linhas, 2)
    linhas.extend(["```", ""])
    return "\n".join(linhas)


def _node_to_attributed_dict(node: AstNode, result: SemanticAnalysisResult) -> dict[str, object]:
    base = _base(node, result)
    if isinstance(node, NumberNode):
        base.update({"kind": "Number", "lexeme": node.lexeme, "value": node.value})
        return base
    if isinstance(node, BoolNode):
        base.update({"kind": "Bool", "lexeme": node.lexeme, "value": node.value})
        return base
    if isinstance(node, MemoryReadNode):
        base.update({"kind": "MemoryRead", "name": node.name, "symbol_ref": _symbol_ref(node.name, result)})
        return base
    if isinstance(node, ResultRefNode):
        base.update({"kind": "ResultRef", "offset": node.offset})
        return base
    if isinstance(node, MemoryWriteNode):
        base.update(
            {
                "kind": "MemoryWrite",
                "name": node.name,
                "symbol_ref": _symbol_ref(node.name, result),
                "value": _node_to_attributed_dict(node.value, result),
            }
        )
        return base
    if isinstance(node, BinaryOpNode):
        base.update(
            {
                "kind": "BinaryOp",
                "operator": node.operator,
                "left": _node_to_attributed_dict(node.left, result),
                "right": _node_to_attributed_dict(node.right, result),
            }
        )
        return base
    if isinstance(node, RelationalOpNode):
        base.update(
            {
                "kind": "RelationalOp",
                "operator": node.operator,
                "left": _node_to_attributed_dict(node.left, result),
                "right": _node_to_attributed_dict(node.right, result),
            }
        )
        return base
    if isinstance(node, LogicalOpNode):
        base.update(
            {
                "kind": "LogicalOp",
                "operator": node.operator,
                "left": _node_to_attributed_dict(node.left, result),
                "right": _node_to_attributed_dict(node.right, result),
            }
        )
        return base
    if isinstance(node, LogicalNotNode):
        base.update(
            {
                "kind": "LogicalNot",
                "operator": "NOT",
                "operand": _node_to_attributed_dict(node.operand, result),
            }
        )
        return base
    if isinstance(node, SequenceNode):
        base.update(
            {
                "kind": "Sequence",
                "first": _node_to_attributed_dict(node.first, result),
                "second": _node_to_attributed_dict(node.second, result),
            }
        )
        return base
    if isinstance(node, IfNode):
        base.update(
            {
                "kind": "IfElse" if node.else_branch is not None else "If",
                "condition": _node_to_attributed_dict(node.condition, result),
                "then": _node_to_attributed_dict(node.then_branch, result),
            }
        )
        if node.else_branch is not None:
            base["else"] = _node_to_attributed_dict(node.else_branch, result)
        return base
    if isinstance(node, WhileNode):
        base.update(
            {
                "kind": "While",
                "condition": _node_to_attributed_dict(node.condition, result),
                "body": _node_to_attributed_dict(node.body, result),
            }
        )
        return base
    raise TypeError(f"No de AST desconhecido: {type(node)!r}")


def _base(node: AstNode, result: SemanticAnalysisResult) -> dict[str, object]:
    type_name = result.node_types.get(id(node), TYPE_ERROR)
    return {
        "line": getattr(node, "line"),
        "column": getattr(node, "column"),
        "inferred_type": type_name,
        "semantic_status": "error" if type_name == TYPE_ERROR else "ok",
    }


def _symbol_ref(name: str, result: SemanticAnalysisResult) -> dict[str, object] | None:
    symbol = result.symbol_table.get(name)
    if symbol is None:
        return None
    return {
        "name": symbol.name,
        "type": symbol.type_name,
        "declared": symbol.declared,
        "initialized": symbol.initialized,
    }


def _render_node(node_payload: object, linhas: list[str], indent: int) -> None:
    assert isinstance(node_payload, dict)
    prefix = " " * indent
    kind = node_payload.get("kind")
    inferred_type = node_payload.get("inferred_type")
    line = node_payload.get("line")
    linhas.append(f"{prefix}{kind} line={line} type={inferred_type}")
    for child_key in ("value", "left", "right", "operand", "condition", "then", "else", "first", "second", "body"):
        child = node_payload.get(child_key)
        if isinstance(child, dict):
            _render_node(child, linhas, indent + 2)
