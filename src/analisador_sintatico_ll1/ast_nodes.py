# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass
class NumberNode:
    value: float
    lexeme: str
    line: int
    column: int
    is_integer_literal: bool


@dataclass
class BoolNode:
    value: bool
    lexeme: str
    line: int
    column: int


@dataclass
class MemoryReadNode:
    name: str
    line: int
    column: int


@dataclass
class ResultRefNode:
    offset: int
    line: int
    column: int


@dataclass
class MemoryWriteNode:
    name: str
    value: "AstNode"
    line: int
    column: int


@dataclass
class BinaryOpNode:
    operator: str
    left: "AstNode"
    right: "AstNode"
    line: int
    column: int


@dataclass
class RelationalOpNode:
    operator: str
    left: "AstNode"
    right: "AstNode"
    line: int
    column: int


@dataclass
class LogicalOpNode:
    operator: str
    left: "AstNode"
    right: "AstNode"
    line: int
    column: int


@dataclass
class LogicalNotNode:
    operand: "AstNode"
    line: int
    column: int


@dataclass
class SequenceNode:
    first: "AstNode"
    second: "AstNode"
    line: int
    column: int


@dataclass
class IfNode:
    condition: "AstNode"
    then_branch: "AstNode"
    else_branch: "AstNode | None"
    line: int
    column: int


@dataclass
class WhileNode:
    condition: "AstNode"
    body: "AstNode"
    line: int
    column: int


AstNode = Union[
    NumberNode,
    BoolNode,
    MemoryReadNode,
    ResultRefNode,
    MemoryWriteNode,
    BinaryOpNode,
    RelationalOpNode,
    LogicalOpNode,
    LogicalNotNode,
    SequenceNode,
    IfNode,
    WhileNode,
]


@dataclass
class StatementEntry:
    ordinal: int
    source_line: int
    node: AstNode


@dataclass
class ProgramNode:
    statements: list[StatementEntry]


def is_expression_node(node: AstNode) -> bool:
    return isinstance(
        node,
        (
            NumberNode,
            BoolNode,
            MemoryReadNode,
            ResultRefNode,
            MemoryWriteNode,
            BinaryOpNode,
            RelationalOpNode,
            LogicalOpNode,
            LogicalNotNode,
        ),
    )


def is_statement_node(node: AstNode) -> bool:
    return not isinstance(node, (NumberNode, BoolNode))


def node_to_dict(node: AstNode) -> dict[str, object]:
    if isinstance(node, NumberNode):
        return {
            "type": "Number",
            "value": node.value,
            "lexeme": node.lexeme,
            "line": node.line,
            "column": node.column,
            "is_integer_literal": node.is_integer_literal,
        }
    if isinstance(node, BoolNode):
        return {
            "type": "Bool",
            "value": node.value,
            "lexeme": node.lexeme,
            "line": node.line,
            "column": node.column,
        }
    if isinstance(node, MemoryReadNode):
        return {
            "type": "MemoryRead",
            "name": node.name,
            "line": node.line,
            "column": node.column,
        }
    if isinstance(node, ResultRefNode):
        return {
            "type": "ResultRef",
            "offset": node.offset,
            "line": node.line,
            "column": node.column,
        }
    if isinstance(node, MemoryWriteNode):
        return {
            "type": "MemoryWrite",
            "name": node.name,
            "line": node.line,
            "column": node.column,
            "value": node_to_dict(node.value),
        }
    if isinstance(node, BinaryOpNode):
        return {
            "type": "BinaryOp",
            "operator": node.operator,
            "line": node.line,
            "column": node.column,
            "left": node_to_dict(node.left),
            "right": node_to_dict(node.right),
        }
    if isinstance(node, RelationalOpNode):
        return {
            "type": "RelationalOp",
            "operator": node.operator,
            "line": node.line,
            "column": node.column,
            "left": node_to_dict(node.left),
            "right": node_to_dict(node.right),
        }
    if isinstance(node, LogicalOpNode):
        return {
            "type": "LogicalOp",
            "operator": node.operator,
            "line": node.line,
            "column": node.column,
            "left": node_to_dict(node.left),
            "right": node_to_dict(node.right),
        }
    if isinstance(node, LogicalNotNode):
        return {
            "type": "LogicalNot",
            "operator": "NOT",
            "line": node.line,
            "column": node.column,
            "operand": node_to_dict(node.operand),
        }
    if isinstance(node, SequenceNode):
        return {
            "type": "Sequence",
            "line": node.line,
            "column": node.column,
            "first": node_to_dict(node.first),
            "second": node_to_dict(node.second),
        }
    if isinstance(node, IfNode):
        payload = {
            "type": "IfElse" if node.else_branch is not None else "If",
            "line": node.line,
            "column": node.column,
            "condition": node_to_dict(node.condition),
            "then": node_to_dict(node.then_branch),
        }
        if node.else_branch is not None:
            payload["else"] = node_to_dict(node.else_branch)
        return payload
    if isinstance(node, WhileNode):
        return {
            "type": "While",
            "line": node.line,
            "column": node.column,
            "condition": node_to_dict(node.condition),
            "body": node_to_dict(node.body),
        }
    raise TypeError(f"No AST desconhecido: {type(node)!r}")


def program_to_dict(program: ProgramNode) -> dict[str, object]:
    return {
        "type": "Program",
        "statement_count": len(program.statements),
        "statements": [
            {
                "ordinal": item.ordinal,
                "source_line": item.source_line,
                "tree": node_to_dict(item.node),
            }
            for item in program.statements
        ],
    }


def render_program_tree(program: ProgramNode) -> str:
    linhas = ["Program"]
    for statement in program.statements:
        linhas.append(f"  Statement[{statement.ordinal}] line={statement.source_line}")
        _render_node_tree(statement.node, linhas, 4)
    return "\n".join(linhas) + "\n"


def _render_node_tree(node: AstNode, linhas: list[str], indent: int) -> None:
    prefixo = " " * indent
    if isinstance(node, NumberNode):
        linhas.append(f"{prefixo}Number value={node.lexeme}")
        return
    if isinstance(node, BoolNode):
        linhas.append(f"{prefixo}Bool value={node.lexeme}")
        return
    if isinstance(node, MemoryReadNode):
        linhas.append(f"{prefixo}MemoryRead name={node.name}")
        return
    if isinstance(node, ResultRefNode):
        linhas.append(f"{prefixo}ResultRef offset={node.offset}")
        return
    if isinstance(node, MemoryWriteNode):
        linhas.append(f"{prefixo}MemoryWrite name={node.name}")
        _render_node_tree(node.value, linhas, indent + 2)
        return
    if isinstance(node, BinaryOpNode):
        linhas.append(f"{prefixo}BinaryOp operator={node.operator}")
        _render_node_tree(node.left, linhas, indent + 2)
        _render_node_tree(node.right, linhas, indent + 2)
        return
    if isinstance(node, RelationalOpNode):
        linhas.append(f"{prefixo}RelationalOp operator={node.operator}")
        _render_node_tree(node.left, linhas, indent + 2)
        _render_node_tree(node.right, linhas, indent + 2)
        return
    if isinstance(node, LogicalOpNode):
        linhas.append(f"{prefixo}LogicalOp operator={node.operator}")
        _render_node_tree(node.left, linhas, indent + 2)
        _render_node_tree(node.right, linhas, indent + 2)
        return
    if isinstance(node, LogicalNotNode):
        linhas.append(f"{prefixo}LogicalNot")
        _render_node_tree(node.operand, linhas, indent + 2)
        return
    if isinstance(node, SequenceNode):
        linhas.append(f"{prefixo}Sequence")
        _render_node_tree(node.first, linhas, indent + 2)
        _render_node_tree(node.second, linhas, indent + 2)
        return
    if isinstance(node, IfNode):
        linhas.append(f"{prefixo}{'IfElse' if node.else_branch is not None else 'If'}")
        linhas.append(f"{prefixo}  Condition")
        _render_node_tree(node.condition, linhas, indent + 4)
        linhas.append(f"{prefixo}  Then")
        _render_node_tree(node.then_branch, linhas, indent + 4)
        if node.else_branch is not None:
            linhas.append(f"{prefixo}  Else")
            _render_node_tree(node.else_branch, linhas, indent + 4)
        return
    if isinstance(node, WhileNode):
        linhas.append(f"{prefixo}While")
        linhas.append(f"{prefixo}  Condition")
        _render_node_tree(node.condition, linhas, indent + 4)
        linhas.append(f"{prefixo}  Body")
        _render_node_tree(node.body, linhas, indent + 4)
        return


def node_to_rpn_string(node: AstNode) -> str:
    if isinstance(node, NumberNode):
        return node.lexeme
    if isinstance(node, BoolNode):
        return node.lexeme
    if isinstance(node, MemoryReadNode):
        return f"({node.name})"
    if isinstance(node, ResultRefNode):
        return f"({node.offset} RES)"
    if isinstance(node, MemoryWriteNode):
        return f"({node_to_rpn_string(node.value)} {node.name})"
    if isinstance(node, BinaryOpNode):
        return f"({node_to_rpn_string(node.left)} {node_to_rpn_string(node.right)} {node.operator})"
    if isinstance(node, RelationalOpNode):
        return f"({node_to_rpn_string(node.left)} {node_to_rpn_string(node.right)} {node.operator})"
    if isinstance(node, LogicalOpNode):
        return f"({node_to_rpn_string(node.left)} {node_to_rpn_string(node.right)} {node.operator})"
    if isinstance(node, LogicalNotNode):
        return f"({node_to_rpn_string(node.operand)} NOT)"
    if isinstance(node, SequenceNode):
        return f"({node_to_rpn_string(node.first)} {node_to_rpn_string(node.second)} SEQ)"
    if isinstance(node, IfNode):
        if node.else_branch is None:
            return f"({node_to_rpn_string(node.condition)} {node_to_rpn_string(node.then_branch)} IF)"
        return (
            f"({node_to_rpn_string(node.condition)} "
            f"{node_to_rpn_string(node.then_branch)} "
            f"{node_to_rpn_string(node.else_branch)} IFELSE)"
        )
    if isinstance(node, WhileNode):
        return f"({node_to_rpn_string(node.condition)} {node_to_rpn_string(node.body)} WHILE)"
    raise TypeError(f"No AST desconhecido: {type(node)!r}")
