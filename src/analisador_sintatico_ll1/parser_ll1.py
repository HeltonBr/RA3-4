# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass

from analisador_sintatico_ll1.diagnostics import AnalysisDiagnostic
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
from analisador_sintatico_ll1.ast_nodes import StatementEntry
from analisador_sintatico_ll1.ast_nodes import WhileNode
from analisador_sintatico_ll1.ast_nodes import is_expression_node
from analisador_sintatico_ll1.ast_nodes import is_statement_node
from analisador_sintatico_ll1.grammar import GrammarBundle
from analisador_sintatico_ll1.tokens import Token
from analisador_sintatico_ll1.tokens import TokenType
from analisador_sintatico_ll1.tokens import flatten_token_lines
from analisador_sintatico_ll1.errors import SyntaxAnalysisError


@dataclass
class ParseResult:
    derivation: list[str]
    syntax_tree_seed: ProgramNode
    analysis_trace: list[str]


@dataclass
class SyntaxScanResult:
    parse_result: ParseResult
    diagnostics: list["AnalysisDiagnostic"]


class TokenStream:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def peek(self, offset: int = 0) -> Token:
        pos = min(self.index + offset, len(self.tokens) - 1)
        return self.tokens[pos]

    def advance(self) -> Token:
        token = self.peek()
        if self.index < len(self.tokens) - 1:
            self.index += 1
        return token

    def check(self, token_type: TokenType) -> bool:
        return self.peek().token_type == token_type

    def expect(self, token_type: TokenType, message: str) -> Token:
        token = self.peek()
        if token.token_type != token_type:
            raise SyntaxAnalysisError(
                f"{message} Encontrado {format_token_for_error(token)} na linha {token.line}, coluna {token.column}."
            )
        return self.advance()


class RecursiveDescentLL1Parser:
    def __init__(self, tokens: list[Token], grammar: GrammarBundle) -> None:
        self.stream = TokenStream(tokens)
        self.grammar = grammar
        self.derivation: list[str] = []
        self.analysis_trace: list[str] = []
        self.analysis_stack: list[str] = []
        self.statement_ordinal = 1

    def parse_program(self) -> ProgramNode:
        self._push("program")
        self._choose("program")
        self._parse_start_line()
        statements = self._parse_program_body()
        self._pop()
        return ProgramNode(statements=statements)

    def _parse_start_line(self) -> None:
        self._push("start_line")
        self._choose("start_line")
        self.stream.expect(TokenType.LPAREN, "Era esperado '(' para iniciar a linha START.")
        self.stream.expect(TokenType.KW_START, "Era esperado START.")
        self.stream.expect(TokenType.RPAREN, "Era esperado ')' apos START.")
        self.stream.expect(TokenType.EOL, "Era esperado fim de linha apos (START).")
        self._pop()

    def _parse_program_body(self) -> list[StatementEntry]:
        self._push("program_body")
        self._choose("program_body")
        opening = self.stream.expect(TokenType.LPAREN, "Era esperado '(' para iniciar uma linha do programa.")
        statements = self._parse_program_body_after_lparen(opening)
        self._pop()
        return statements

    def _parse_program_body_after_lparen(self, opening: Token) -> list[StatementEntry]:
        self._push("program_body_after_lparen")
        lookahead = self.stream.peek()
        if lookahead.token_type == TokenType.KW_END:
            self._choose("program_body_after_lparen")
            self.stream.advance()
            self.stream.expect(TokenType.RPAREN, "Era esperado ')' apos END.")
            self.stream.expect(TokenType.EOL, "Era esperado fim de linha apos (END).")
            self.stream.expect(TokenType.EOF, "Era esperado fim de arquivo apos (END).")
            self._pop()
            return []

        self._choose("program_body_after_lparen")
        node = self._parse_stmt_inner()
        self.stream.expect(TokenType.RPAREN, "Era esperado ')' para fechar a declaracao.")
        self.stream.expect(TokenType.EOL, "Era esperado fim de linha apos a declaracao.")
        entry = StatementEntry(
            ordinal=self.statement_ordinal,
            source_line=opening.line,
            node=node,
        )
        self.statement_ordinal += 1
        tail = self._parse_program_body()
        self._pop()
        return [entry, *tail]

    def _parse_stmt(self) -> AstNode:
        self._push("stmt")
        self._choose("stmt")
        opening = self.stream.expect(TokenType.LPAREN, "Era esperado '(' para iniciar a estrutura.")
        node = self._parse_stmt_inner()
        self.stream.expect(TokenType.RPAREN, "Era esperado ')' para fechar a estrutura.")
        self._pop()
        return self._with_fallback_position(node, opening)

    def _parse_stmt_inner(self) -> AstNode:
        self._push("stmt_inner")
        producao = self._choose("stmt_inner")
        if producao == ["IDENTIFIER"]:
            token = self.stream.expect(
                TokenType.IDENTIFIER,
                "Era esperado um identificador de memoria na forma canonica (MEM).",
            )
            node = MemoryReadNode(name=token.lexeme, line=token.line, column=token.column)
            self._pop()
            return node

        first = self._parse_item()
        node = self._parse_stmt_after_first(first)
        self._pop()
        return node

    def _parse_item(self) -> AstNode:
        self._push("item")
        producao = self._choose("item")
        if producao == ["NUMBER"]:
            token = self.stream.expect(TokenType.NUMBER, "Era esperado um numero.")
            assert token.numeric_value is not None
            node = NumberNode(
                value=token.numeric_value,
                lexeme=token.lexeme,
                line=token.line,
                column=token.column,
                is_integer_literal=token.is_integer_literal,
            )
            self._pop()
            return node

        if producao == ["BOOL_LITERAL"]:
            token = self.stream.expect(TokenType.BOOL_LITERAL, "Era esperado um literal logico.")
            node = BoolNode(
                value=token.lexeme == "TRUE",
                lexeme=token.lexeme,
                line=token.line,
                column=token.column,
            )
            self._pop()
            return node

        node = self._parse_stmt()
        self._pop()
        return node

    def _parse_stmt_after_first(self, first: AstNode) -> AstNode:
        self._push("stmt_after_first")
        producao = self._choose("stmt_after_first")
        if producao == ["KW_RES"]:
            kw_token = self.stream.expect(TokenType.KW_RES, "Era esperado RES.")
            if not isinstance(first, NumberNode) or not first.is_integer_literal or first.value < 0:
                raise SyntaxAnalysisError(
                    f"RES exige um literal inteiro nao negativo na linha {kw_token.line}, coluna {kw_token.column}."
                )
            node = ResultRefNode(offset=int(first.value), line=kw_token.line, column=kw_token.column)
            self._pop()
            return node

        if producao == ["IDENTIFIER"]:
            id_token = self.stream.expect(
                TokenType.IDENTIFIER,
                "Era esperado o nome da memoria de destino para o armazenamento.",
            )
            self._ensure_expression(first, id_token, "armazenamento em memoria")
            node = MemoryWriteNode(name=id_token.lexeme, value=first, line=id_token.line, column=id_token.column)
            self._pop()
            return node

        if producao == ["OP_NOT"]:
            operator = self.stream.expect(TokenType.OP_NOT, "Era esperado NOT.")
            self._ensure_expression(first, operator, "operacao logica unaria")
            node = LogicalNotNode(operand=first, line=operator.line, column=operator.column)
            self._pop()
            return node

        second = self._parse_item()
        node = self._parse_stmt_after_second(first, second)
        self._pop()
        return node

    def _parse_stmt_after_second(self, first: AstNode, second: AstNode) -> AstNode:
        self._push("stmt_after_second")
        producao = self._choose("stmt_after_second")

        if producao == ["binary_op"]:
            operator = self._parse_binary_op()
            self._ensure_expression(first, operator, "operacao aritmetica")
            self._ensure_expression(second, operator, "operacao aritmetica")
            node = BinaryOpNode(
                operator=operator.lexeme,
                left=first,
                right=second,
                line=operator.line,
                column=operator.column,
            )
            self._pop()
            return node

        if producao == ["relational_op"]:
            operator = self._parse_relational_op()
            self._ensure_expression(first, operator, "operacao relacional")
            self._ensure_expression(second, operator, "operacao relacional")
            node = RelationalOpNode(
                operator=operator.lexeme,
                left=first,
                right=second,
                line=operator.line,
                column=operator.column,
            )
            self._pop()
            return node

        if producao == ["logical_op"]:
            operator = self._parse_logical_op()
            self._ensure_expression(first, operator, "operacao logica")
            self._ensure_expression(second, operator, "operacao logica")
            node = LogicalOpNode(
                operator=operator.lexeme,
                left=first,
                right=second,
                line=operator.line,
                column=operator.column,
            )
            self._pop()
            return node

        if producao == ["KW_IF"]:
            operator = self.stream.expect(TokenType.KW_IF, "Era esperado IF.")
            self._ensure_expression(first, operator, "condicao do IF")
            self._ensure_statement(second, operator, "ramo do IF")
            node = IfNode(
                condition=first,
                then_branch=second,
                else_branch=None,
                line=operator.line,
                column=operator.column,
            )
            self._pop()
            return node

        if producao == ["KW_WHILE"]:
            operator = self.stream.expect(TokenType.KW_WHILE, "Era esperado WHILE.")
            self._ensure_expression(first, operator, "condicao do WHILE")
            self._ensure_statement(second, operator, "corpo do WHILE")
            node = WhileNode(condition=first, body=second, line=operator.line, column=operator.column)
            self._pop()
            return node

        if producao == ["KW_SEQ"]:
            operator = self.stream.expect(TokenType.KW_SEQ, "Era esperado SEQ.")
            self._ensure_statement(first, operator, "primeiro elemento do SEQ")
            self._ensure_statement(second, operator, "segundo elemento do SEQ")
            node = SequenceNode(first=first, second=second, line=operator.line, column=operator.column)
            self._pop()
            return node

        third = self._parse_item()
        operator = self.stream.expect(TokenType.KW_IFELSE, "Era esperado IFELSE.")
        self._ensure_expression(first, operator, "condicao do IFELSE")
        self._ensure_statement(second, operator, "ramo THEN do IFELSE")
        self._ensure_statement(third, operator, "ramo ELSE do IFELSE")
        node = IfNode(
            condition=first,
            then_branch=second,
            else_branch=third,
            line=operator.line,
            column=operator.column,
        )
        self._pop()
        return node

    def _parse_binary_op(self) -> Token:
        self._push("binary_op")
        self._choose("binary_op")
        token = self.stream.advance()
        if token.token_type not in {
            TokenType.OP_PLUS,
            TokenType.OP_MINUS,
            TokenType.OP_MULT,
            TokenType.OP_REAL_DIV,
            TokenType.OP_INT_DIV,
            TokenType.OP_MOD,
            TokenType.OP_POW,
        }:
            raise SyntaxAnalysisError(
                f"Operador aritmetico invalido '{token.lexeme}' na linha {token.line}, coluna {token.column}."
            )
        self._pop()
        return token

    def _parse_relational_op(self) -> Token:
        self._push("relational_op")
        self._choose("relational_op")
        token = self.stream.advance()
        if token.token_type not in {
            TokenType.OP_GT,
            TokenType.OP_LT,
            TokenType.OP_GTE,
            TokenType.OP_LTE,
            TokenType.OP_EQ,
            TokenType.OP_NEQ,
        }:
            raise SyntaxAnalysisError(
                f"Operador relacional invalido '{token.lexeme}' na linha {token.line}, coluna {token.column}."
            )
        self._pop()
        return token

    def _parse_logical_op(self) -> Token:
        self._push("logical_op")
        self._choose("logical_op")
        token = self.stream.advance()
        if token.token_type not in {TokenType.OP_AND, TokenType.OP_OR}:
            raise SyntaxAnalysisError(
                f"Operador logico invalido '{token.lexeme}' na linha {token.line}, coluna {token.column}."
            )
        self._pop()
        return token

    def _choose(self, nonterminal: str) -> list[str]:
        lookahead = self.stream.peek().token_type.name
        producao = self.grammar.parsing_table.get(nonterminal, {}).get(lookahead)
        if producao is None:
            token = self.stream.peek()
            raise SyntaxAnalysisError(self._build_prediction_error(nonterminal, token))
        self.derivation.append(f"{nonterminal} -> {' '.join(producao)}")
        self.analysis_trace.append(f"pilha={self.analysis_stack!r} lookahead={lookahead} producao={producao}")
        return producao

    def _push(self, symbol: str) -> None:
        self.analysis_stack.append(symbol)

    def _pop(self) -> None:
        self.analysis_stack.pop()

    def _ensure_expression(self, node: AstNode, token: Token, contexto: str) -> None:
        if not is_expression_node(node):
            raise SyntaxAnalysisError(
                f"A estrutura usada em {contexto} nao produz valor na linha {token.line}, coluna {token.column}."
            )

    def _ensure_statement(self, node: AstNode, token: Token, contexto: str) -> None:
        if not is_statement_node(node):
            raise SyntaxAnalysisError(
                f"O item usado em {contexto} precisa ser uma estrutura parentetizada na linha "
                f"{token.line}, coluna {token.column}."
            )

    def _with_fallback_position(self, node: AstNode, opening: Token) -> AstNode:
        if getattr(node, "line", None):
            return node
        setattr(node, "line", opening.line)
        setattr(node, "column", opening.column)
        return node

    def _build_prediction_error(self, nonterminal: str, token: Token) -> str:
        esperados = sorted(self.grammar.parsing_table.get(nonterminal, {}))
        esperado_legivel = ", ".join(esperados)

        if nonterminal == "program_body" and token.token_type == TokenType.EOF:
            return "Programa incompleto: faltou a linha final (END)."
        if nonterminal == "program_body_after_lparen" and token.token_type == TokenType.RPAREN:
            return (
                "Declaracao vazia encontrada. Entre '(' e ')' era esperado END, um numero, "
                f"um identificador ou uma estrutura aninhada na linha {token.line}, coluna {token.column}."
            )
        if token.token_type == TokenType.EOF:
            return (
                f"Fim inesperado de arquivo enquanto analisava {nonterminal}. "
                f"Esperado: {esperado_legivel}."
            )
        if nonterminal == "stmt_after_second":
            return (
                "Estrutura pos-fixada incompleta: apos dois itens era esperado um operador aritmetico, "
                "um operador relacional, um operador logico ou uma keyword de controle (IF, IFELSE, WHILE, SEQ). "
                f"Encontrado {format_token_for_error(token)} na linha {token.line}, coluna {token.column}."
            )
        if nonterminal == "stmt_after_first":
            return (
                "Estrutura pos-fixada incompleta: apos o primeiro item era esperado RES, NOT, um identificador "
                "de memoria de destino ou outro item para continuar a estrutura. "
                f"Encontrado {format_token_for_error(token)} na linha {token.line}, coluna {token.column}."
            )
        return (
            f"Nao ha producao LL(1) para {nonterminal} com lookahead {token.token_type.name} "
            f"na linha {token.line}, coluna {token.column}. Esperado: {esperado_legivel}."
        )


def parsear(tokens: list[list[Token]], tabela_ll1: GrammarBundle) -> ParseResult:
    fluxo = flatten_token_lines(tokens)
    parser = RecursiveDescentLL1Parser(fluxo, tabela_ll1)
    program = parser.parse_program()
    return ParseResult(
        derivation=parser.derivation,
        syntax_tree_seed=program,
        analysis_trace=parser.analysis_trace,
    )


def parsearComDiagnosticos(tokens: list[list[Token]], tabela_ll1: GrammarBundle) -> SyntaxScanResult:
    diagnostics: list[AnalysisDiagnostic] = []
    if not tokens:
        diagnostics.append(
            AnalysisDiagnostic(
                kind="SINTATICO",
                code="PROGRAMA_VAZIO",
                line=1,
                column=1,
                message="programa vazio; esperado '(START)' e '(END)'.",
            )
        )
        return SyntaxScanResult(
            parse_result=ParseResult(derivation=[], syntax_tree_seed=ProgramNode(statements=[]), analysis_trace=[]),
            diagnostics=diagnostics,
        )

    _validar_linha_start(tokens, diagnostics)
    end_index = _encontrar_linha_end(tokens, diagnostics)
    statements = _parsear_linhas_declaracao(tokens, tabela_ll1, end_index, diagnostics)

    if end_index is not None:
        for extra_line in tokens[end_index + 1 :]:
            if not extra_line:
                continue
            first = extra_line[0]
            diagnostics.append(
                AnalysisDiagnostic(
                    kind="SINTATICO",
                    code="CONTEUDO_APOS_END",
                    line=first.line,
                    column=first.column,
                    message="conteudo encontrado apos a linha final '(END)'.",
                )
            )

    program = ProgramNode(statements=statements)
    parse_result = ParseResult(derivation=[], syntax_tree_seed=program, analysis_trace=[])
    return SyntaxScanResult(parse_result=parse_result, diagnostics=diagnostics)


def _validar_linha_start(tokens: list[list[Token]], diagnostics: list[AnalysisDiagnostic]) -> None:
    first_line = tokens[0]
    if _is_exact_line(first_line, [TokenType.LPAREN, TokenType.KW_START, TokenType.RPAREN]):
        return
    first = first_line[0]
    diagnostics.append(
        AnalysisDiagnostic(
            kind="SINTATICO",
            code="START_AUSENTE",
            line=first.line,
            column=first.column,
            message="programa deve iniciar com a linha '(START)'.",
        )
    )


def _encontrar_linha_end(
    tokens: list[list[Token]],
    diagnostics: list[AnalysisDiagnostic],
) -> int | None:
    end_index: int | None = None
    for index, line_tokens in enumerate(tokens):
        if _is_exact_line(line_tokens, [TokenType.LPAREN, TokenType.KW_END, TokenType.RPAREN]):
            if end_index is None:
                end_index = index
            else:
                first = line_tokens[0]
                diagnostics.append(
                    AnalysisDiagnostic(
                        kind="SINTATICO",
                        code="END_DUPLICADO",
                        line=first.line,
                        column=first.column,
                        message="linha '(END)' duplicada.",
                    )
                )
    if end_index is None:
        last = tokens[-1][-1]
        diagnostics.append(
            AnalysisDiagnostic(
                kind="SINTATICO",
                code="END_AUSENTE",
                line=last.line,
                column=last.column + len(last.lexeme),
                message="Programa incompleto: faltou a linha final (END).",
            )
        )
    return end_index


def _parsear_linhas_declaracao(
    tokens: list[list[Token]],
    tabela_ll1: GrammarBundle,
    end_index: int | None,
    diagnostics: list[AnalysisDiagnostic],
) -> list[StatementEntry]:
    stop_index = end_index if end_index is not None else len(tokens)
    start_index = 1 if _is_exact_line(tokens[0], [TokenType.LPAREN, TokenType.KW_START, TokenType.RPAREN]) else 0
    statements: list[StatementEntry] = []
    ordinal = 1

    for line_tokens in tokens[start_index:stop_index]:
        if not line_tokens:
            continue
        if _is_exact_line(line_tokens, [TokenType.LPAREN, TokenType.KW_START, TokenType.RPAREN]):
            first = line_tokens[0]
            diagnostics.append(
                AnalysisDiagnostic(
                    kind="SINTATICO",
                    code="START_FORA_DO_INICIO",
                    line=first.line,
                    column=first.column,
                    message="'(START)' so pode aparecer na primeira linha processavel.",
                )
            )
            continue
        if _is_exact_line(line_tokens, [TokenType.LPAREN, TokenType.KW_END, TokenType.RPAREN]):
            continue
        try:
            parsed = _parsear_uma_declaracao(line_tokens, tabela_ll1)
        except SyntaxAnalysisError as exc:
            first = line_tokens[0]
            diagnostics.append(
                AnalysisDiagnostic(
                    kind="SINTATICO",
                    code="DECLARACAO_INVALIDA",
                    line=first.line,
                    column=first.column,
                    message=str(exc),
                )
            )
            continue
        if parsed.statements:
            statement = parsed.statements[0]
            statements.append(
                StatementEntry(
                    ordinal=ordinal,
                    source_line=statement.source_line,
                    node=statement.node,
                )
            )
            ordinal += 1
    return statements


def _parsear_uma_declaracao(line_tokens: list[Token], tabela_ll1: GrammarBundle) -> ProgramNode:
    line_number = line_tokens[0].line
    synthetic_start = [
        Token(TokenType.LPAREN, "(", line_number, 0),
        Token(TokenType.KW_START, "START", line_number, 0),
        Token(TokenType.RPAREN, ")", line_number, 0),
    ]
    synthetic_end = [
        Token(TokenType.LPAREN, "(", line_number, 0),
        Token(TokenType.KW_END, "END", line_number, 0),
        Token(TokenType.RPAREN, ")", line_number, 0),
    ]
    parser = RecursiveDescentLL1Parser(
        flatten_token_lines([synthetic_start, line_tokens, synthetic_end]),
        tabela_ll1,
    )
    return parser.parse_program()


def _is_exact_line(tokens: list[Token], token_types: list[TokenType]) -> bool:
    return [token.token_type for token in tokens] == token_types


def format_token_for_error(token: Token) -> str:
    if token.token_type == TokenType.EOF:
        return "fim de arquivo"
    if token.token_type == TokenType.EOL:
        return "fim de linha"
    return f"'{token.lexeme}'"
