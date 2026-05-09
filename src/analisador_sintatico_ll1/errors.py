# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations


class AnalisadorSintaticoError(Exception):
    """Classe base para os erros tratados pelo projeto."""


class TokenReadError(AnalisadorSintaticoError):
    """Falha ao ler ou interpretar a entrada de tokens."""


class LexicalTokenError(TokenReadError):
    """Falha ao tokenizar um arquivo-fonte da Fase 3."""


class GrammarError(AnalisadorSintaticoError):
    """Falha ao construir ou validar a gramatica LL(1)."""


class SyntaxAnalysisError(AnalisadorSintaticoError):
    """Falha sintatica detectada durante o parsing."""


class AssemblyGenerationError(AnalisadorSintaticoError):
    """Falha ao transformar a AST em Assembly ARMv7."""
