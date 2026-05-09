# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from analisador_sintatico_ll1.diagnostics import AnalysisDiagnostic
from analisador_sintatico_ll1.errors import LexicalTokenError
from analisador_sintatico_ll1.errors import TokenReadError


class TokenType(Enum):
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    NUMBER = "NUMBER"
    BOOL_LITERAL = "BOOL_LITERAL"
    IDENTIFIER = "IDENTIFIER"
    KW_START = "KW_START"
    KW_END = "KW_END"
    KW_RES = "KW_RES"
    KW_SEQ = "KW_SEQ"
    KW_IF = "KW_IF"
    KW_IFELSE = "KW_IFELSE"
    KW_WHILE = "KW_WHILE"
    OP_PLUS = "OP_PLUS"
    OP_MINUS = "OP_MINUS"
    OP_MULT = "OP_MULT"
    OP_REAL_DIV = "OP_REAL_DIV"
    OP_INT_DIV = "OP_INT_DIV"
    OP_MOD = "OP_MOD"
    OP_POW = "OP_POW"
    OP_GT = "OP_GT"
    OP_LT = "OP_LT"
    OP_GTE = "OP_GTE"
    OP_LTE = "OP_LTE"
    OP_EQ = "OP_EQ"
    OP_NEQ = "OP_NEQ"
    OP_AND = "OP_AND"
    OP_OR = "OP_OR"
    OP_NOT = "OP_NOT"
    EOL = "EOL"
    EOF = "EOF"


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int
    numeric_value: float | None = None
    is_integer_literal: bool = False

    def to_serializable(self) -> str:
        parts = [
            f"type={self.token_type.name}",
            f"lexeme={self.lexeme}",
            f"line={self.line}",
            f"column={self.column}",
        ]
        if self.numeric_value is not None:
            parts.append(f"value={self.numeric_value}")
        parts.append(f"is_integer_literal={self.is_integer_literal}")
        return ";".join(parts)


@dataclass
class TokenReadResult:
    tokens_por_linha: list[list[Token]]
    diagnostics: list[AnalysisDiagnostic]


KEYWORDS = {
    "START": TokenType.KW_START,
    "END": TokenType.KW_END,
    "RES": TokenType.KW_RES,
    "SEQ": TokenType.KW_SEQ,
    "IF": TokenType.KW_IF,
    "IFELSE": TokenType.KW_IFELSE,
    "WHILE": TokenType.KW_WHILE,
    "TRUE": TokenType.BOOL_LITERAL,
    "FALSE": TokenType.BOOL_LITERAL,
    "AND": TokenType.OP_AND,
    "OR": TokenType.OP_OR,
    "NOT": TokenType.OP_NOT,
}

SYMBOLIC_OPERATORS = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "+": TokenType.OP_PLUS,
    "-": TokenType.OP_MINUS,
    "*": TokenType.OP_MULT,
    "|": TokenType.OP_REAL_DIV,
    "/": TokenType.OP_INT_DIV,
    "%": TokenType.OP_MOD,
    "^": TokenType.OP_POW,
    ">": TokenType.OP_GT,
    "<": TokenType.OP_LT,
}

MULTI_CHAR_OPERATORS = {
    ">=": TokenType.OP_GTE,
    "<=": TokenType.OP_LTE,
    "==": TokenType.OP_EQ,
    "!=": TokenType.OP_NEQ,
}

LEXEME_TOKEN_OVERRIDES = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "+": TokenType.OP_PLUS,
    "-": TokenType.OP_MINUS,
    "*": TokenType.OP_MULT,
    "|": TokenType.OP_REAL_DIV,
    "/": TokenType.OP_INT_DIV,
    "//": TokenType.OP_INT_DIV,
    "%": TokenType.OP_MOD,
    "^": TokenType.OP_POW,
    ">": TokenType.OP_GT,
    "<": TokenType.OP_LT,
    ">=": TokenType.OP_GTE,
    "<=": TokenType.OP_LTE,
    "==": TokenType.OP_EQ,
    "!=": TokenType.OP_NEQ,
    "AND": TokenType.OP_AND,
    "OR": TokenType.OP_OR,
    "NOT": TokenType.OP_NOT,
    "TRUE": TokenType.BOOL_LITERAL,
    "FALSE": TokenType.BOOL_LITERAL,
    "START": TokenType.KW_START,
    "END": TokenType.KW_END,
    "RES": TokenType.KW_RES,
    "SEQ": TokenType.KW_SEQ,
    "IF": TokenType.KW_IF,
    "IFELSE": TokenType.KW_IFELSE,
    "WHILE": TokenType.KW_WHILE,
}


def lerTokens(arquivo: str | Path) -> list[list[Token]]:
    caminho = Path(arquivo)
    texto = _ler_texto(caminho)
    if _parece_tokens_serializados(texto):
        tokens_por_linha = _ler_tokens_serializados(texto, caminho)
    else:
        tokens_por_linha = _tokenizar_programa(texto)

    if not tokens_por_linha:
        raise TokenReadError("A entrada nao contem nenhuma linha processavel.")
    return tokens_por_linha


def lerTokensComDiagnosticos(arquivo: str | Path) -> TokenReadResult:
    caminho = Path(arquivo)
    texto = _ler_texto(caminho)
    if _parece_tokens_serializados(texto):
        try:
            tokens_por_linha = _ler_tokens_serializados(texto, caminho)
        except TokenReadError as exc:
            return TokenReadResult(
                tokens_por_linha=[],
                diagnostics=[
                    AnalysisDiagnostic(
                        kind="LEXICO",
                        code="TOKEN_SERIALIZADO_INVALIDO",
                        line=1,
                        column=1,
                        message=str(exc),
                    )
                ],
            )
        return TokenReadResult(tokens_por_linha=tokens_por_linha, diagnostics=[])

    return _tokenizar_programa_com_diagnosticos(texto)


def salvar_tokens_em_arquivo(tokens_por_linha: list[list[Token]], caminho_saida: str | Path) -> None:
    caminho = Path(caminho_saida)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(serializar_tokens(tokens_por_linha), encoding="utf-8")


def serializar_tokens(tokens_por_linha: list[list[Token]]) -> str:
    linhas_saida: list[str] = []
    for indice, tokens in enumerate(tokens_por_linha, start=1):
        header_line = tokens[0].line if tokens else indice
        linhas_saida.append(f"[LINHA {header_line}]")
        for token in tokens:
            if token.token_type in {TokenType.EOL, TokenType.EOF}:
                continue
            linhas_saida.append(token.to_serializable())
        linhas_saida.append("")
    return "\n".join(linhas_saida).rstrip() + "\n"


def flatten_token_lines(tokens_por_linha: list[list[Token]]) -> list[Token]:
    fluxo: list[Token] = []
    ultima_linha = 1
    for tokens in tokens_por_linha:
        if not tokens:
            continue
        fluxo.extend(tokens)
        ultima_linha = tokens[-1].line
        fluxo.append(Token(TokenType.EOL, "<EOL>", ultima_linha, tokens[-1].column + 1))
    fluxo.append(Token(TokenType.EOF, "<EOF>", ultima_linha + 1, 1))
    return fluxo


def _ler_texto(caminho: Path) -> str:
    if not caminho.exists():
        raise TokenReadError(f"Arquivo nao encontrado: {caminho}")
    if not caminho.is_file():
        raise TokenReadError(f"O caminho informado nao e um arquivo: {caminho}")
    try:
        return caminho.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise TokenReadError(f"Falha ao ler o arquivo como UTF-8: {caminho}") from exc
    except OSError as exc:
        raise TokenReadError(f"Falha ao abrir o arquivo: {caminho}") from exc


def _parece_tokens_serializados(texto: str) -> bool:
    for linha in texto.splitlines():
        limpa = linha.strip()
        if not limpa:
            continue
        return limpa.startswith("[LINHA ") or limpa.startswith("type=")
    return False


def _tokenizar_programa(texto: str) -> list[list[Token]]:
    tokens_por_linha: list[list[Token]] = []
    em_comentario = False
    comentario_inicio_linha = 1
    comentario_inicio_coluna = 1

    for numero_linha, linha in enumerate(texto.splitlines(), start=1):
        if not linha.strip() and not em_comentario:
            continue
        tokens, em_comentario, inicio = _tokenizar_linha(
            linha,
            numero_linha,
            em_comentario,
            comentario_inicio_linha,
            comentario_inicio_coluna,
        )
        comentario_inicio_linha, comentario_inicio_coluna = inicio
        if tokens:
            tokens_por_linha.append(tokens)

    if em_comentario:
        raise LexicalTokenError(
            "Erro LEXICO na linha "
            f"{comentario_inicio_linha}, coluna {comentario_inicio_coluna}: "
            "comentario iniciado com '*{' nao foi fechado com '}*'."
        )

    return tokens_por_linha


def _tokenizar_programa_com_diagnosticos(texto: str) -> TokenReadResult:
    tokens_por_linha: list[list[Token]] = []
    diagnostics: list[AnalysisDiagnostic] = []
    em_comentario = False
    comentario_inicio_linha = 1
    comentario_inicio_coluna = 1

    for numero_linha, linha in enumerate(texto.splitlines(), start=1):
        if not linha.strip() and not em_comentario:
            continue
        tokens, em_comentario, inicio = _tokenizar_linha_com_diagnosticos(
            linha,
            numero_linha,
            diagnostics,
            em_comentario,
            comentario_inicio_linha,
            comentario_inicio_coluna,
        )
        comentario_inicio_linha, comentario_inicio_coluna = inicio
        if tokens:
            tokens_por_linha.append(tokens)

    if em_comentario:
        diagnostics.append(
            AnalysisDiagnostic(
                kind="LEXICO",
                code="COMENTARIO_NAO_FECHADO",
                line=comentario_inicio_linha,
                column=comentario_inicio_coluna,
                message="comentario iniciado com '*{' nao foi fechado com '}*'.",
            )
        )

    if not tokens_por_linha and not diagnostics:
        diagnostics.append(
            AnalysisDiagnostic(
                kind="LEXICO",
                code="ENTRADA_VAZIA",
                line=1,
                column=1,
                message="a entrada nao contem nenhuma linha processavel.",
            )
        )

    return TokenReadResult(tokens_por_linha=tokens_por_linha, diagnostics=diagnostics)


def _tokenizar_linha_com_diagnosticos(
    linha: str,
    numero_linha: int,
    diagnostics: list[AnalysisDiagnostic],
    em_comentario: bool = False,
    comentario_inicio_linha: int = 1,
    comentario_inicio_coluna: int = 1,
) -> tuple[list[Token], bool, tuple[int, int]]:
    tokens: list[Token] = []
    indice = 0
    while indice < len(linha):
        caractere = linha[indice]
        coluna = indice + 1

        if em_comentario:
            fechamento = linha.find("}*", indice)
            if fechamento == -1:
                return tokens, True, (comentario_inicio_linha, comentario_inicio_coluna)
            em_comentario = False
            indice = fechamento + 2
            continue

        if caractere.isspace():
            indice += 1
            continue

        trecho_duplo = linha[indice : indice + 2]
        if trecho_duplo == "*{":
            em_comentario = True
            comentario_inicio_linha = numero_linha
            comentario_inicio_coluna = coluna
            indice += 2
            continue

        if trecho_duplo in MULTI_CHAR_OPERATORS:
            tokens.append(Token(MULTI_CHAR_OPERATORS[trecho_duplo], trecho_duplo, numero_linha, coluna))
            indice += 2
            continue

        if caractere in SYMBOLIC_OPERATORS:
            tokens.append(Token(SYMBOLIC_OPERATORS[caractere], caractere, numero_linha, coluna))
            indice += 1
            continue

        if caractere.isdigit():
            token, proximo_indice, erro = _tokenizar_numero_com_diagnostico(linha, indice, numero_linha)
            if erro is not None:
                diagnostics.append(erro)
            elif token is not None:
                tokens.append(token)
            indice = proximo_indice
            continue

        if caractere.isalpha():
            palavra = _ler_palavra(linha, indice)
            if not palavra.isupper():
                diagnostics.append(
                    AnalysisDiagnostic(
                        kind="LEXICO",
                        code="IDENTIFICADOR_INVALIDO",
                        line=numero_linha,
                        column=coluna,
                        message=f"identificador invalido '{palavra}'. Use apenas letras maiusculas.",
                    )
                )
                indice += len(palavra)
                continue
            token_type = KEYWORDS.get(palavra, TokenType.IDENTIFIER)
            tokens.append(Token(token_type, palavra, numero_linha, coluna))
            indice += len(palavra)
            continue

        diagnostics.append(
            AnalysisDiagnostic(
                kind="LEXICO",
                code="CARACTERE_INVALIDO",
                line=numero_linha,
                column=coluna,
                message=f"caractere invalido '{caractere}'.",
            )
        )
        indice += 1

    return tokens, em_comentario, (comentario_inicio_linha, comentario_inicio_coluna)


def _tokenizar_linha(
    linha: str,
    numero_linha: int,
    em_comentario: bool = False,
    comentario_inicio_linha: int = 1,
    comentario_inicio_coluna: int = 1,
) -> tuple[list[Token], bool, tuple[int, int]]:
    tokens: list[Token] = []
    indice = 0
    while indice < len(linha):
        caractere = linha[indice]
        coluna = indice + 1

        if em_comentario:
            fechamento = linha.find("}*", indice)
            if fechamento == -1:
                return tokens, True, (comentario_inicio_linha, comentario_inicio_coluna)
            em_comentario = False
            indice = fechamento + 2
            continue

        if caractere.isspace():
            indice += 1
            continue

        trecho_duplo = linha[indice : indice + 2]
        if trecho_duplo == "*{":
            em_comentario = True
            comentario_inicio_linha = numero_linha
            comentario_inicio_coluna = coluna
            indice += 2
            continue

        if trecho_duplo in MULTI_CHAR_OPERATORS:
            tokens.append(Token(MULTI_CHAR_OPERATORS[trecho_duplo], trecho_duplo, numero_linha, coluna))
            indice += 2
            continue

        if caractere in SYMBOLIC_OPERATORS:
            tokens.append(Token(SYMBOLIC_OPERATORS[caractere], caractere, numero_linha, coluna))
            indice += 1
            continue

        if caractere.isdigit():
            tokens.append(_tokenizar_numero(linha, indice, numero_linha))
            indice += len(tokens[-1].lexeme)
            continue

        if caractere.isalpha():
            palavra = _ler_palavra(linha, indice)
            if not palavra.isupper():
                raise LexicalTokenError(
                    f"Identificador invalido '{palavra}' na linha {numero_linha}, coluna {coluna}. "
                    "Use apenas letras maiusculas."
                )
            token_type = KEYWORDS.get(palavra, TokenType.IDENTIFIER)
            tokens.append(Token(token_type, palavra, numero_linha, coluna))
            indice += len(palavra)
            continue

        raise LexicalTokenError(
            f"Caractere invalido '{caractere}' na linha {numero_linha}, coluna {coluna}."
        )

    return tokens, em_comentario, (comentario_inicio_linha, comentario_inicio_coluna)


def _ler_palavra(linha: str, inicio: int) -> str:
    fim = inicio
    while fim < len(linha) and linha[fim].isalpha():
        fim += 1
    return linha[inicio:fim]


def _tokenizar_numero(linha: str, inicio: int, numero_linha: int) -> Token:
    fim = inicio
    tem_ponto = False
    while fim < len(linha):
        atual = linha[fim]
        if atual.isdigit():
            fim += 1
            continue
        if atual == "." and not tem_ponto:
            tem_ponto = True
            fim += 1
            continue
        break

    lexema = linha[inicio:fim]
    if fim < len(linha) and linha[fim] == ".":
        fim_malformado = fim
        while fim_malformado < len(linha) and (linha[fim_malformado].isdigit() or linha[fim_malformado] == "."):
            fim_malformado += 1
        lexema_malformado = linha[inicio:fim_malformado]
        raise LexicalTokenError(
            f"Numero malformado '{lexema_malformado}' na linha {numero_linha}, coluna {inicio + 1}. "
            "Use no maximo um ponto decimal por numero."
        )

    if lexema.endswith("."):
        raise LexicalTokenError(
            f"Numero invalido '{lexema}' na linha {numero_linha}, coluna {inicio + 1}."
        )

    valor = float(lexema)
    return Token(
        TokenType.NUMBER,
        lexema,
        numero_linha,
        inicio + 1,
        numeric_value=valor,
        is_integer_literal="." not in lexema,
    )


def _tokenizar_numero_com_diagnostico(
    linha: str,
    inicio: int,
    numero_linha: int,
) -> tuple[Token | None, int, AnalysisDiagnostic | None]:
    fim = inicio
    tem_ponto = False
    while fim < len(linha):
        atual = linha[fim]
        if atual.isdigit():
            fim += 1
            continue
        if atual == "." and not tem_ponto:
            tem_ponto = True
            fim += 1
            continue
        break

    lexema = linha[inicio:fim]
    if fim < len(linha) and linha[fim] == ".":
        fim_malformado = fim
        while fim_malformado < len(linha) and (
            linha[fim_malformado].isdigit() or linha[fim_malformado] == "."
        ):
            fim_malformado += 1
        lexema_malformado = linha[inicio:fim_malformado]
        return (
            None,
            fim_malformado,
            AnalysisDiagnostic(
                kind="LEXICO",
                code="NUMERO_MALFORMADO",
                line=numero_linha,
                column=inicio + 1,
                message=f"numero malformado '{lexema_malformado}'. Use no maximo um ponto decimal por numero.",
            ),
        )

    if lexema.endswith("."):
        return (
            None,
            fim,
            AnalysisDiagnostic(
                kind="LEXICO",
                code="NUMERO_INVALIDO",
                line=numero_linha,
                column=inicio + 1,
                message=f"numero invalido '{lexema}'.",
            ),
        )

    valor = float(lexema)
    return (
        Token(
            TokenType.NUMBER,
            lexema,
            numero_linha,
            inicio + 1,
            numeric_value=valor,
            is_integer_literal="." not in lexema,
        ),
        fim,
        None,
    )


def _ler_tokens_serializados(texto: str, caminho: Path) -> list[list[Token]]:
    tokens_por_linha: list[list[Token]] = []
    atual: list[Token] | None = None

    for bruto in texto.splitlines():
        linha = bruto.strip()
        if not linha:
            continue
        if linha.startswith("[LINHA "):
            if atual is not None:
                tokens_por_linha.append(atual)
            atual = []
            continue
        if atual is None:
            raise TokenReadError(
                f"Formato invalido em {caminho}: token encontrado antes do cabecalho [LINHA N]."
            )
        atual.append(_parse_token_serializado(linha))

    if atual is not None:
        tokens_por_linha.append(atual)

    if not tokens_por_linha:
        raise TokenReadError(f"Nenhum token serializado foi encontrado em {caminho}.")
    return tokens_por_linha


def _parse_token_serializado(linha: str) -> Token:
    campos: dict[str, str] = {}
    for parte in linha.split(";"):
        chave, separador, valor = parte.partition("=")
        if not separador:
            raise TokenReadError(f"Linha de token invalida: {linha}")
        campos[chave] = valor

    try:
        lexema = campos["lexeme"]
        line = int(campos["line"])
        column = int(campos["column"])
        is_integer_literal = campos.get("is_integer_literal", "False").lower() == "true"
    except KeyError as exc:
        raise TokenReadError(f"Campo obrigatorio ausente no token serializado: {linha}") from exc
    except ValueError as exc:
        raise TokenReadError(f"Campo numerico invalido no token serializado: {linha}") from exc

    numeric_value_raw = campos.get("value") or campos.get("numeric_value")
    numeric_value = float(numeric_value_raw) if numeric_value_raw is not None else None
    token_type = _resolver_tipo_serializado(campos["type"], lexema)
    return Token(
        token_type=token_type,
        lexeme=lexema,
        line=line,
        column=column,
        numeric_value=numeric_value,
        is_integer_literal=is_integer_literal,
    )


def _resolver_tipo_serializado(type_name: str, lexema: str) -> TokenType:
    if lexema in LEXEME_TOKEN_OVERRIDES:
        return LEXEME_TOKEN_OVERRIDES[lexema]

    try:
        return TokenType[type_name]
    except KeyError:
        alias_map = {
            "OP_DIV": TokenType.OP_REAL_DIV if lexema == "|" else TokenType.OP_INT_DIV,
            "OP_INT_DIV": TokenType.OP_INT_DIV,
        }
        if type_name in alias_map:
            return alias_map[type_name]
        raise TokenReadError(f"Tipo de token desconhecido: {type_name}")
