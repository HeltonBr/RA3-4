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
from analisador_sintatico_ll1.semantic_errors import SemanticDiagnostic
from analisador_sintatico_ll1.symbol_table import SymbolTable

TYPE_INT = "int"
TYPE_REAL = "real"
TYPE_BOOL = "bool"
TYPE_VOID = "void"
TYPE_ERROR = "erro"

NUMERIC_TYPES = {TYPE_INT, TYPE_REAL}


@dataclass
class SemanticAnalysisResult:
    program: ProgramNode
    symbol_table: SymbolTable
    errors: list[SemanticDiagnostic]
    node_types: dict[int, str]
    statement_types: dict[int, str]

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)


class SemanticAnalyzer:
    def __init__(self) -> None:
        self.symbol_table = SymbolTable()
        self.errors: list[SemanticDiagnostic] = []
        self.node_types: dict[int, str] = {}
        self.statement_types: dict[int, str] = {}
        self.current_statement = 0

    def analyze(self, program: ProgramNode) -> SemanticAnalysisResult:
        for statement in program.statements:
            self.current_statement = statement.ordinal
            statement_type = self._infer(statement.node)
            self.statement_types[statement.ordinal] = statement_type
        return SemanticAnalysisResult(
            program=program,
            symbol_table=self.symbol_table,
            errors=self.errors,
            node_types=self.node_types,
            statement_types=self.statement_types,
        )

    def _infer(self, node: AstNode) -> str:
        if isinstance(node, NumberNode):
            return self._mark(node, TYPE_INT if node.is_integer_literal else TYPE_REAL)

        if isinstance(node, BoolNode):
            return self._mark(node, TYPE_BOOL)

        if isinstance(node, MemoryReadNode):
            symbol = self.symbol_table.use(node.name, node.line, node.column)
            if not symbol.declared:
                self._error(
                    "VAR_UNDEFINED",
                    node.line,
                    node.column,
                    f"variavel '{node.name}' usada antes da definicao.",
                )
                return self._mark(node, TYPE_ERROR)
            return self._mark(node, symbol.type_name)

        if isinstance(node, ResultRefNode):
            return self._infer_result_ref(node)

        if isinstance(node, MemoryWriteNode):
            value_type = self._infer(node.value)
            if value_type in {TYPE_ERROR, TYPE_VOID}:
                self._error(
                    "STORE_INVALID_VALUE",
                    node.line,
                    node.column,
                    f"variavel '{node.name}' nao pode receber valor do tipo {value_type}.",
                )
                return self._mark(node, TYPE_ERROR)

            symbol = self.symbol_table.get(node.name)
            if symbol is not None and symbol.declared and symbol.type_name != value_type:
                self._error(
                    "VAR_TYPE_REDEFINITION",
                    node.line,
                    node.column,
                    f"variavel '{node.name}' ja foi definida como {symbol.type_name} e nao pode receber {value_type}.",
                )
                self.symbol_table.define(node.name, value_type, node.line, node.column)
                return self._mark(node, TYPE_ERROR)

            self.symbol_table.define(node.name, value_type, node.line, node.column)
            return self._mark(node, value_type)

        if isinstance(node, BinaryOpNode):
            return self._infer_binary_op(node)

        if isinstance(node, RelationalOpNode):
            return self._infer_relational_op(node)

        if isinstance(node, LogicalOpNode):
            left_type = self._infer(node.left)
            right_type = self._infer(node.right)
            if left_type == TYPE_BOOL and right_type == TYPE_BOOL:
                return self._mark(node, TYPE_BOOL)
            if TYPE_ERROR not in {left_type, right_type}:
                self._error(
                    "LOGICAL_TYPE",
                    node.line,
                    node.column,
                    f"operador '{node.operator}' exige bool e bool, recebido {left_type} e {right_type}.",
                )
            return self._mark(node, TYPE_ERROR)

        if isinstance(node, LogicalNotNode):
            operand_type = self._infer(node.operand)
            if operand_type == TYPE_BOOL:
                return self._mark(node, TYPE_BOOL)
            if operand_type != TYPE_ERROR:
                self._error(
                    "LOGICAL_NOT_TYPE",
                    node.line,
                    node.column,
                    f"operador 'NOT' exige bool, recebido {operand_type}.",
                )
            return self._mark(node, TYPE_ERROR)

        if isinstance(node, SequenceNode):
            self._infer(node.first)
            return self._mark(node, self._infer(node.second))

        if isinstance(node, IfNode):
            return self._infer_if(node)

        if isinstance(node, WhileNode):
            condition_type = self._infer(node.condition)
            if condition_type != TYPE_BOOL and condition_type != TYPE_ERROR:
                self._error(
                    "WHILE_CONDITION",
                    node.line,
                    node.column,
                    f"condicao de WHILE deve ser bool, recebido {condition_type}.",
                )
            self._infer(node.body)
            return self._mark(node, TYPE_VOID)

        raise TypeError(f"No de AST desconhecido: {type(node)!r}")

    def _infer_result_ref(self, node: ResultRefNode) -> str:
        if node.offset <= 0:
            self._error(
                "RES_ZERO",
                node.line,
                node.column,
                "RES exige N positivo; N=0 nao referencia uma linha anterior.",
            )
            return self._mark(node, TYPE_ERROR)

        target_statement = self.current_statement - node.offset
        target_type = self.statement_types.get(target_statement)
        if target_type is None:
            self._error(
                "RES_OUT_OF_RANGE",
                node.line,
                node.column,
                f"RES invalido: nao existe resultado {node.offset} linha(s) antes desta declaracao.",
            )
            return self._mark(node, TYPE_ERROR)

        if target_type in {TYPE_VOID, TYPE_ERROR}:
            self._error(
                "RES_NO_VALUE",
                node.line,
                node.column,
                f"RES referencia declaracao anterior sem valor utilizavel ({target_type}).",
            )
            return self._mark(node, TYPE_ERROR)

        return self._mark(node, target_type)

    def _infer_binary_op(self, node: BinaryOpNode) -> str:
        left_type = self._infer(node.left)
        right_type = self._infer(node.right)
        if TYPE_ERROR in {left_type, right_type}:
            return self._mark(node, TYPE_ERROR)

        if node.operator in {"+", "-", "*"}:
            if self._both_numeric(left_type, right_type):
                return self._mark(node, self._promote_numeric(left_type, right_type))
            self._error(
                "ARITH_TYPE",
                node.line,
                node.column,
                f"operador '{node.operator}' exige operandos numericos, recebido {left_type} e {right_type}.",
            )
            return self._mark(node, TYPE_ERROR)

        if node.operator == "|":
            if self._both_numeric(left_type, right_type):
                return self._mark(node, TYPE_REAL)
            self._error(
                "REAL_DIV_TYPE",
                node.line,
                node.column,
                f"divisao real '|' exige operandos numericos, recebido {left_type} e {right_type}.",
            )
            return self._mark(node, TYPE_ERROR)

        if node.operator in {"/", "%"}:
            if left_type == TYPE_INT and right_type == TYPE_INT:
                return self._mark(node, TYPE_INT)
            self._error(
                "INT_ONLY_OP",
                node.line,
                node.column,
                f"operador '{node.operator}' exige int e int, recebido {left_type} e {right_type}.",
            )
            return self._mark(node, TYPE_ERROR)

        if node.operator == "^":
            if left_type in NUMERIC_TYPES and right_type == TYPE_INT:
                return self._mark(node, TYPE_REAL if left_type == TYPE_REAL else TYPE_INT)
            self._error(
                "POW_TYPE",
                node.line,
                node.column,
                f"potenciacao '^' exige base numerica e expoente int, recebido {left_type} e {right_type}.",
            )
            return self._mark(node, TYPE_ERROR)

        self._error(
            "UNKNOWN_BINARY_OP",
            node.line,
            node.column,
            f"operador aritmetico desconhecido '{node.operator}'.",
        )
        return self._mark(node, TYPE_ERROR)

    def _infer_relational_op(self, node: RelationalOpNode) -> str:
        left_type = self._infer(node.left)
        right_type = self._infer(node.right)
        if TYPE_ERROR in {left_type, right_type}:
            return self._mark(node, TYPE_ERROR)

        if node.operator in {">", "<", ">=", "<="}:
            if self._both_numeric(left_type, right_type):
                return self._mark(node, TYPE_BOOL)
            self._error(
                "RELATIONAL_ORDER_TYPE",
                node.line,
                node.column,
                f"operador '{node.operator}' exige operandos numericos, recebido {left_type} e {right_type}.",
            )
            return self._mark(node, TYPE_ERROR)

        if node.operator in {"==", "!="}:
            if self._both_numeric(left_type, right_type) or left_type == right_type == TYPE_BOOL:
                return self._mark(node, TYPE_BOOL)
            self._error(
                "RELATIONAL_EQUALITY_TYPE",
                node.line,
                node.column,
                f"operador '{node.operator}' exige tipos compativeis, recebido {left_type} e {right_type}.",
            )
            return self._mark(node, TYPE_ERROR)

        self._error(
            "UNKNOWN_RELATIONAL_OP",
            node.line,
            node.column,
            f"operador relacional desconhecido '{node.operator}'.",
        )
        return self._mark(node, TYPE_ERROR)

    def _infer_if(self, node: IfNode) -> str:
        condition_type = self._infer(node.condition)
        if condition_type != TYPE_BOOL and condition_type != TYPE_ERROR:
            keyword = "IFELSE" if node.else_branch is not None else "IF"
            self._error(
                "IF_CONDITION",
                node.line,
                node.column,
                f"condicao de {keyword} deve ser bool, recebido {condition_type}.",
            )

        then_type = self._infer(node.then_branch)
        if node.else_branch is None:
            return self._mark(node, TYPE_VOID)

        else_type = self._infer(node.else_branch)
        if TYPE_ERROR in {then_type, else_type}:
            return self._mark(node, TYPE_ERROR)
        if then_type == else_type:
            return self._mark(node, then_type)
        if self._both_numeric(then_type, else_type):
            return self._mark(node, self._promote_numeric(then_type, else_type))

        self._error(
            "IFELSE_BRANCH_TYPE",
            node.line,
            node.column,
            f"ramos de IFELSE devem ter tipos compativeis, recebido {then_type} e {else_type}.",
        )
        return self._mark(node, TYPE_ERROR)

    def _mark(self, node: AstNode, type_name: str) -> str:
        self.node_types[id(node)] = type_name
        return type_name

    def _error(self, code: str, line: int, column: int, message: str) -> None:
        self.errors.append(SemanticDiagnostic(code=code, line=line, column=column, message=message))

    @staticmethod
    def _both_numeric(left_type: str, right_type: str) -> bool:
        return left_type in NUMERIC_TYPES and right_type in NUMERIC_TYPES

    @staticmethod
    def _promote_numeric(left_type: str, right_type: str) -> str:
        return TYPE_REAL if TYPE_REAL in {left_type, right_type} else TYPE_INT


def analyze_program(program: ProgramNode) -> SemanticAnalysisResult:
    return SemanticAnalyzer().analyze(program)
