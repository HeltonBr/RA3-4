# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from analisador_sintatico_ll1.errors import GrammarError

EPSILON = "EPSILON"


@dataclass
class GrammarBundle:
    start_symbol: str
    productions: dict[str, list[list[str]]]
    first: dict[str, set[str]]
    follow: dict[str, set[str]]
    parsing_table: dict[str, dict[str, list[str]]]
    terminals: tuple[str, ...]
    nonterminals: tuple[str, ...]


def construirGramatica() -> GrammarBundle:
    productions = _producoes_canonicas()
    nonterminals = tuple(productions.keys())
    terminals = tuple(sorted(_descobrir_terminais(productions)))
    first = _calcular_first(productions, terminals)
    follow = _calcular_follow(productions, first, "program")
    parsing_table = _construir_tabela_ll1(productions, first, follow)
    return GrammarBundle(
        start_symbol="program",
        productions=productions,
        first=first,
        follow=follow,
        parsing_table=parsing_table,
        terminals=terminals,
        nonterminals=nonterminals,
    )


def salvar_documentacao_gramatica(bundle: GrammarBundle, docs_dir: str | Path) -> None:
    destino = Path(docs_dir)
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "gramatica.md").write_text(render_grammar_markdown(bundle), encoding="utf-8")
    (destino / "gramatica_atribuida.md").write_text(render_grammar_markdown(bundle), encoding="utf-8")
    (destino / "first_follow.md").write_text(render_first_follow_markdown(bundle), encoding="utf-8")
    (destino / "tabela_ll1.md").write_text(render_ll1_table_markdown(bundle), encoding="utf-8")
    (destino / "sintaxe_controle.md").write_text(render_control_syntax_markdown(), encoding="utf-8")


def render_grammar_markdown(bundle: GrammarBundle) -> str:
    linhas = [
        "# Gramatica Canonica LL(1)",
        "",
        "A linguagem da Fase 3 preserva a analise preditiva LL(1), o estilo pos-fixado e acrescenta os pontos semanticos necessarios para tipos, comentarios e geracao segura de Assembly.",
        "",
        "## Observacoes de projeto",
        "",
        "- Leitura de memoria e sempre canonica na forma `(MEM)`.",
        "- Gravacao em memoria continua na forma `(<item> MEM)`.",
        "- Literais logicos sao `TRUE` e `FALSE`.",
        "- Operadores logicos sao `AND`, `OR` e `NOT`.",
        "- Isso evita o uso de identificadores soltos como operandos e elimina conflitos na tabela LL(1).",
        "- `START` e `END` aparecem apenas no topo do programa.",
        "",
        "## BNF operacional",
        "",
        "```text",
    ]
    for nao_terminal, producoes in bundle.productions.items():
        alternativas = [" ".join(_render_symbol(simbolo) for simbolo in producao) for producao in producoes]
        linhas.append(f"{nao_terminal} ::= " + " | ".join(alternativas))
    linhas.extend(
        [
            "```",
            "",
            "## EBNF equivalente",
            "",
            "```text",
            "program        = start_line , program_body ;",
            "start_line     = LPAREN , KW_START , RPAREN , EOL ;",
            "program_body   = LPAREN , ( KW_END , RPAREN , EOL , EOF",
            "                          | stmt_inner , RPAREN , EOL , program_body ) ;",
            "stmt           = LPAREN , stmt_inner , RPAREN ;",
            "stmt_inner     = IDENTIFIER | item , stmt_after_first ;",
            "item           = NUMBER | BOOL_LITERAL | stmt ;",
            "stmt_after_first = KW_RES | IDENTIFIER | OP_NOT | item , stmt_after_second ;",
            "stmt_after_second = binary_op | relational_op | logical_op | KW_IF | KW_WHILE | KW_SEQ | item , KW_IFELSE ;",
            "logical_op     = OP_AND | OP_OR ;",
            "```",
            "",
        ]
    )
    return "\n".join(linhas) + "\n"


def render_first_follow_markdown(bundle: GrammarBundle) -> str:
    linhas = [
        "# Conjuntos FIRST e FOLLOW",
        "",
        "| Nao-terminal | FIRST | FOLLOW |",
        "| --- | --- | --- |",
    ]
    for nao_terminal in bundle.nonterminals:
        first = ", ".join(_render_symbol(simbolo) for simbolo in sorted(bundle.first[nao_terminal]))
        follow = ", ".join(_render_symbol(simbolo) for simbolo in sorted(bundle.follow[nao_terminal]))
        linhas.append(f"| `{nao_terminal}` | `{first}` | `{follow}` |")
    linhas.append("")
    return "\n".join(linhas)


def render_ll1_table_markdown(bundle: GrammarBundle) -> str:
    colunas = [terminal for terminal in bundle.terminals if terminal != EPSILON]
    linhas = [
        "# Tabela LL(1)",
        "",
        "| Nao-terminal | " + " | ".join(f"`{_render_symbol(coluna)}`" for coluna in colunas) + " |",
        "| --- | " + " | ".join("---" for _ in colunas) + " |",
    ]
    for nao_terminal in bundle.nonterminals:
        celulas: list[str] = []
        for terminal in colunas:
            producao = bundle.parsing_table.get(nao_terminal, {}).get(terminal)
            if producao is None:
                celulas.append("")
            else:
                texto = " ".join(_render_symbol(simbolo) for simbolo in producao)
                celulas.append(f"`{texto}`")
        linhas.append(f"| `{nao_terminal}` | " + " | ".join(celulas) + " |")
    linhas.append("")
    return "\n".join(linhas)


def render_control_syntax_markdown() -> str:
    return "\n".join(
        [
            "# Sintaxe das Estruturas de Controle",
            "",
            "## Convencoes",
            "",
            "- Toda estrutura fica entre parenteses.",
            "- A linguagem continua pos-fixada: os operandos aparecem antes do operador final.",
            "- Leitura de memoria e sempre parentetizada, por exemplo `(X)`.",
            "",
            "## Formas canonicas",
            "",
            "```text",
            "(<expr> <stmt> IF)",
            "(<expr> <stmt> <stmt> IFELSE)",
            "(<expr> <stmt> WHILE)",
            "(<stmt> <stmt> SEQ)",
            "(<expr> <expr> AND)",
            "(<expr> <expr> OR)",
            "(<expr> NOT)",
            "```",
            "",
            "## Exemplos",
            "",
            "```text",
            "(((X) 0 >) (((X) 1 -) X) WHILE)",
            "(((X) (Y) >) (((X) (Y) +) Z) IF)",
            "(((X) (Y) <) (((X) (Y) +) W) (((X) (Y) -) W) IFELSE)",
            "((((X) 1 -) X) (((W) (X) +) W) SEQ)",
            "(((X) 0 >) TRUE AND)",
            "(((X) 0 ==) NOT)",
            "```",
            "",
        ]
    )


def _producoes_canonicas() -> dict[str, list[list[str]]]:
    return {
        "program": [["start_line", "program_body"]],
        "start_line": [["LPAREN", "KW_START", "RPAREN", "EOL"]],
        "program_body": [["LPAREN", "program_body_after_lparen"]],
        "program_body_after_lparen": [
            ["KW_END", "RPAREN", "EOL", "EOF"],
            ["stmt_inner", "RPAREN", "EOL", "program_body"],
        ],
        "stmt": [["LPAREN", "stmt_inner", "RPAREN"]],
        "stmt_inner": [["IDENTIFIER"], ["item", "stmt_after_first"]],
        "item": [["NUMBER"], ["BOOL_LITERAL"], ["stmt"]],
        "stmt_after_first": [["KW_RES"], ["IDENTIFIER"], ["OP_NOT"], ["item", "stmt_after_second"]],
        "stmt_after_second": [
            ["binary_op"],
            ["relational_op"],
            ["logical_op"],
            ["KW_IF"],
            ["KW_WHILE"],
            ["KW_SEQ"],
            ["item", "KW_IFELSE"],
        ],
        "binary_op": [
            ["OP_PLUS"],
            ["OP_MINUS"],
            ["OP_MULT"],
            ["OP_REAL_DIV"],
            ["OP_INT_DIV"],
            ["OP_MOD"],
            ["OP_POW"],
        ],
        "relational_op": [
            ["OP_GT"],
            ["OP_LT"],
            ["OP_GTE"],
            ["OP_LTE"],
            ["OP_EQ"],
            ["OP_NEQ"],
        ],
        "logical_op": [
            ["OP_AND"],
            ["OP_OR"],
        ],
    }


def _descobrir_terminais(productions: dict[str, list[list[str]]]) -> set[str]:
    nonterminals = set(productions)
    terminals: set[str] = set()
    for producoes in productions.values():
        for producao in producoes:
            for simbolo in producao:
                if simbolo != EPSILON and simbolo not in nonterminals:
                    terminals.add(simbolo)
    return terminals


def _calcular_first(
    productions: dict[str, list[list[str]]],
    terminals: tuple[str, ...],
) -> dict[str, set[str]]:
    first: dict[str, set[str]] = {terminal: {terminal} for terminal in terminals}
    for nao_terminal in productions:
        first.setdefault(nao_terminal, set())

    alterado = True
    while alterado:
        alterado = False
        for nao_terminal, producoes in productions.items():
            for producao in producoes:
                first_antes = set(first[nao_terminal])
                first[nao_terminal] |= _first_de_sequencia(producao, first, productions)
                if first_antes != first[nao_terminal]:
                    alterado = True
    return {chave: valor for chave, valor in first.items() if chave in productions}


def _calcular_follow(
    productions: dict[str, list[list[str]]],
    first: dict[str, set[str]],
    start_symbol: str,
) -> dict[str, set[str]]:
    follow: dict[str, set[str]] = {nao_terminal: set() for nao_terminal in productions}
    follow[start_symbol].add("EOF")

    alterado = True
    while alterado:
        alterado = False
        for nao_terminal, producoes in productions.items():
            for producao in producoes:
                for indice, simbolo in enumerate(producao):
                    if simbolo not in productions:
                        continue
                    resto = producao[indice + 1 :]
                    first_resto = _first_de_sequencia(resto, first, productions)
                    follow_antes = set(follow[simbolo])
                    follow[simbolo] |= {terminal for terminal in first_resto if terminal != EPSILON}
                    if not resto or EPSILON in first_resto:
                        follow[simbolo] |= follow[nao_terminal]
                    if follow_antes != follow[simbolo]:
                        alterado = True
    return follow


def _construir_tabela_ll1(
    productions: dict[str, list[list[str]]],
    first: dict[str, set[str]],
    follow: dict[str, set[str]],
) -> dict[str, dict[str, list[str]]]:
    tabela: dict[str, dict[str, list[str]]] = {nao_terminal: {} for nao_terminal in productions}

    for nao_terminal, producoes in productions.items():
        for producao in producoes:
            first_producao = _first_de_sequencia(producao, first, productions)
            destinos = {terminal for terminal in first_producao if terminal != EPSILON}
            if EPSILON in first_producao:
                destinos |= follow[nao_terminal]

            for terminal in destinos:
                existente = tabela[nao_terminal].get(terminal)
                if existente is not None and existente != producao:
                    atual = " ".join(producao)
                    outro = " ".join(existente)
                    raise GrammarError(
                        f"Conflito LL(1) em ({nao_terminal}, {terminal}): '{outro}' x '{atual}'."
                    )
                tabela[nao_terminal][terminal] = producao

    return tabela


def _first_de_sequencia(
    sequencia: list[str],
    first: dict[str, set[str]],
    productions: dict[str, list[list[str]]],
) -> set[str]:
    if not sequencia:
        return {EPSILON}

    resultado: set[str] = set()
    for simbolo in sequencia:
        if simbolo == EPSILON:
            resultado.add(EPSILON)
            break
        if simbolo not in productions:
            resultado.add(simbolo)
            break

        resultado |= {terminal for terminal in first[simbolo] if terminal != EPSILON}
        if EPSILON not in first[simbolo]:
            break
    else:
        resultado.add(EPSILON)
    return resultado


def _render_symbol(simbolo: str) -> str:
    return "e" if simbolo == EPSILON else simbolo
