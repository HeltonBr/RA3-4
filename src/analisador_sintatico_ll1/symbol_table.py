# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

from dataclasses import dataclass, field


Location = tuple[int, int]


@dataclass
class SymbolInfo:
    name: str
    type_name: str
    category: str = "variable"
    defined_at: Location | None = None
    used_at: list[Location] = field(default_factory=list)
    initialized: bool = False
    declared: bool = True
    redefined_at: list[Location] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "type": self.type_name,
            "category": self.category,
            "defined_at": _location_to_dict(self.defined_at),
            "used_at": [_location_to_dict(location) for location in self.used_at],
            "initialized": self.initialized,
            "declared": self.declared,
            "redefined_at": [_location_to_dict(location) for location in self.redefined_at],
        }


@dataclass
class SymbolTable:
    symbols: dict[str, SymbolInfo] = field(default_factory=dict)

    def get(self, name: str) -> SymbolInfo | None:
        return self.symbols.get(name)

    def define(self, name: str, type_name: str, line: int, column: int) -> SymbolInfo:
        symbol = self.symbols.get(name)
        if symbol is None:
            symbol = SymbolInfo(
                name=name,
                type_name=type_name,
                defined_at=(line, column),
                initialized=True,
                declared=True,
            )
            self.symbols[name] = symbol
            return symbol

        if not symbol.declared:
            symbol.type_name = type_name
            symbol.defined_at = (line, column)
            symbol.initialized = True
            symbol.declared = True
            return symbol

        symbol.redefined_at.append((line, column))
        if symbol.type_name == type_name:
            symbol.initialized = True
        return symbol

    def use(self, name: str, line: int, column: int) -> SymbolInfo:
        symbol = self.symbols.get(name)
        if symbol is None:
            symbol = SymbolInfo(
                name=name,
                type_name="erro",
                defined_at=None,
                initialized=False,
                declared=False,
            )
            self.symbols[name] = symbol
        symbol.used_at.append((line, column))
        return symbol

    def to_dict(self) -> dict[str, object]:
        return {
            "symbols": [
                self.symbols[name].to_dict()
                for name in sorted(self.symbols)
            ]
        }

    def render_markdown(self) -> str:
        linhas = [
            "# Tabela de Simbolos",
            "",
            "| Nome | Tipo | Categoria | Definida em | Usos | Inicializada | Declarada |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for name in sorted(self.symbols):
            symbol = self.symbols[name]
            defined_at = _location_to_text(symbol.defined_at)
            used_at = ", ".join(_location_to_text(location) for location in symbol.used_at) or "-"
            initialized = "sim" if symbol.initialized else "nao"
            declared = "sim" if symbol.declared else "nao"
            linhas.append(
                f"| {symbol.name} | {symbol.type_name} | {symbol.category} | "
                f"{defined_at} | {used_at} | {initialized} | {declared} |"
            )
        linhas.append("")
        return "\n".join(linhas)


def _location_to_dict(location: Location | None) -> dict[str, int] | None:
    if location is None:
        return None
    return {"line": location[0], "column": location[1]}


def _location_to_text(location: Location | None) -> str:
    if location is None:
        return "-"
    return f"{location[0]}:{location[1]}"
