# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from analisador_sintatico_ll1.attributed_ast import AttributedAST
from analisador_sintatico_ll1.attributed_ast import build_attributed_ast
from analisador_sintatico_ll1.codegen_arm import gerarAssembly as gerarAssemblyBase
from analisador_sintatico_ll1.diagnostics import AnalysisDiagnostic
from analisador_sintatico_ll1.ast_nodes import ProgramNode
from analisador_sintatico_ll1.ast_nodes import program_to_dict
from analisador_sintatico_ll1.ast_nodes import render_program_tree
from analisador_sintatico_ll1.errors import AssemblyGenerationError
from analisador_sintatico_ll1.grammar import GrammarBundle
from analisador_sintatico_ll1.grammar import construirGramatica
from analisador_sintatico_ll1.parser_ll1 import ParseResult
from analisador_sintatico_ll1.parser_ll1 import parsear
from analisador_sintatico_ll1.parser_ll1 import parsearComDiagnosticos
from analisador_sintatico_ll1.tokens import Token
from analisador_sintatico_ll1.tokens import TokenReadResult
from analisador_sintatico_ll1.tokens import TokenType
from analisador_sintatico_ll1.tokens import lerTokens
from analisador_sintatico_ll1.tokens import lerTokensComDiagnosticos
from analisador_sintatico_ll1.tokens import salvar_tokens_em_arquivo
from analisador_sintatico_ll1.type_system import SemanticAnalysisResult
from analisador_sintatico_ll1.type_system import analyze_program


@dataclass
class SemanticInput:
    tokens: list[list[Token]]
    grammar: GrammarBundle
    parse_result: ParseResult
    syntax_tree: dict[str, Any]
    program: ProgramNode


@dataclass
class SemanticInputDiagnostics(SemanticInput):
    diagnostics: list[AnalysisDiagnostic]


def gerarArvore(derivacao: ParseResult) -> dict[str, Any]:
    program = derivacao.syntax_tree_seed
    if not isinstance(program, ProgramNode):
        raise TypeError("ParseResult nao contem uma ProgramNode valida.")
    return {
        "program": program_to_dict(program),
        "tree_text": render_program_tree(program),
        "derivation": derivacao.derivation,
        "_ast": program,
    }


def prepararEntradaSemantica(arquivo: str) -> SemanticInput:
    tokens = lerTokens(arquivo)
    grammar = construirGramatica()
    parse_result = parsear(tokens, grammar)
    syntax_tree = gerarArvore(parse_result)
    program = _extract_program(syntax_tree)
    return SemanticInput(
        tokens=tokens,
        grammar=grammar,
        parse_result=parse_result,
        syntax_tree=syntax_tree,
        program=program,
    )


def prepararEntradaSemanticaComDiagnosticos(arquivo: str) -> SemanticInputDiagnostics:
    token_result: TokenReadResult = lerTokensComDiagnosticos(arquivo)
    grammar = construirGramatica()
    syntax_result = parsearComDiagnosticos(token_result.tokens_por_linha, grammar)
    program = syntax_result.parse_result.syntax_tree_seed
    syntax_tree = {
        "program": program_to_dict(program),
        "tree_text": render_program_tree(program),
        "derivation": syntax_result.parse_result.derivation,
        "_ast": program,
    }
    return SemanticInputDiagnostics(
        tokens=token_result.tokens_por_linha,
        grammar=grammar,
        parse_result=syntax_result.parse_result,
        syntax_tree=syntax_tree,
        program=program,
        diagnostics=[*token_result.diagnostics, *syntax_result.diagnostics],
    )


def construirTabelaSimbolos(arvore: ProgramNode | dict[str, Any] | SemanticInput) -> SemanticAnalysisResult:
    return analyze_program(_extract_program(arvore))


def verificarTipos(
    arvore: ProgramNode | dict[str, Any] | SemanticInput,
    tabelaSimbolos: SemanticAnalysisResult | None = None,
) -> SemanticAnalysisResult:
    if isinstance(tabelaSimbolos, SemanticAnalysisResult):
        return tabelaSimbolos
    return analyze_program(_extract_program(arvore))


def gerarArvoreAtribuida(
    arvore: ProgramNode | dict[str, Any] | SemanticInput,
    tabelaSimbolos: SemanticAnalysisResult | None = None,
    tipos: SemanticAnalysisResult | None = None,
) -> AttributedAST:
    semantic_result = tipos or tabelaSimbolos
    if not isinstance(semantic_result, SemanticAnalysisResult):
        semantic_result = analyze_program(_extract_program(arvore))
    return build_attributed_ast(semantic_result)


def gerarAssembly(arvore: dict[str, Any] | AttributedAST) -> str:
    if isinstance(arvore, AttributedAST):
        if arvore.has_errors:
            raise AssemblyGenerationError("Assembly bloqueado: ha erros semanticos na arvore atribuida.")
        return gerarAssemblyBase({"_ast": arvore.program})
    return gerarAssemblyBase(arvore)


def _extract_program(arvore: ProgramNode | dict[str, Any] | SemanticInput) -> ProgramNode:
    if isinstance(arvore, SemanticInput):
        return arvore.program
    if isinstance(arvore, ProgramNode):
        return arvore
    program = arvore.get("_ast")
    if isinstance(program, ProgramNode):
        return program
    raise TypeError("Entrada nao contem uma ProgramNode valida.")


__all__ = [
    "GrammarBundle",
    "ParseResult",
    "SemanticAnalysisResult",
    "SemanticInput",
    "SemanticInputDiagnostics",
    "Token",
    "TokenType",
    "construirGramatica",
    "construirTabelaSimbolos",
    "gerarArvore",
    "gerarArvoreAtribuida",
    "gerarAssembly",
    "lerTokens",
    "parsear",
    "prepararEntradaSemanticaComDiagnosticos",
    "prepararEntradaSemantica",
    "salvar_tokens_em_arquivo",
    "verificarTipos",
]
