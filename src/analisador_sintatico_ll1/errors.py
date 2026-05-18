# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations


class SemanticAnalyzerError(Exception):
    """Classe base para os erros tratados pelo projeto."""


class TokenReadError(SemanticAnalyzerError):
    """Falha ao ler ou interpretar a entrada de tokens."""


class LexicalTokenError(TokenReadError):
    """Falha ao tokenizar um arquivo-fonte da Fase 3."""


class GrammarError(SemanticAnalyzerError):
    """Falha ao construir ou validar a gramatica LL(1)."""


class SyntaxAnalysisError(SemanticAnalyzerError):
    """Falha sintatica detectada durante o parsing."""


class AssemblyGenerationError(SemanticAnalyzerError):
    """Falha ao transformar a AST em Assembly ARMv7."""
