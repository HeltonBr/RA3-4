# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import subprocess
import sys
import unittest
import re
from pathlib import Path

from analisador_sintatico_ll1 import construirGramatica
from analisador_sintatico_ll1 import lerTokens
from analisador_sintatico_ll1 import parsear
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
from analisador_sintatico_ll1.core import construirTabelaSimbolos
from analisador_sintatico_ll1.core import gerarArvoreAtribuida
from analisador_sintatico_ll1.core import gerarAssembly
from analisador_sintatico_ll1.core import prepararEntradaSemantica


ROOT = Path(__file__).resolve().parents[1]
NOMES_PROGRAMAS_VALIDOS = ("teste1.txt", "teste2.txt", "teste3.txt")
PROGRAMAS_VALIDOS = [ROOT / nome for nome in NOMES_PROGRAMAS_VALIDOS]
PROGRAMA_SEMANTICO_INVALIDO_RAIZ = ROOT / "teste4_semantico_invalido.txt"
ARQUIVOS_OBRIGATORIOS = [
    ROOT / "README.md",
    ROOT / "AnalisadorSemantico.py",
    ROOT / "teste1.txt",
    ROOT / "teste2.txt",
    ROOT / "teste3.txt",
    PROGRAMA_SEMANTICO_INVALIDO_RAIZ,
    ROOT / "docs" / "decisoes_inconformidades_fase3.md",
    ROOT / "docs" / "auditoria_dossie_inconformidades_fase3.md",
    ROOT / "docs" / "auditoria_gramatica_parser_fase3.md",
    ROOT / "docs" / "auditoria_semantica_tipos_fase3.md",
    ROOT / "docs" / "estrategia_diagnosticos_acumulados.md",
    ROOT / "docs" / "gramatica_atribuida.md",
    ROOT / "docs" / "matriz_cobertura_requisitos.md",
    ROOT / "docs" / "regras_tipos_sequentes.md",
    ROOT / "docs" / "tabela_simbolos.md",
    ROOT / "docs" / "arvore_atribuida_ultima_execucao.md",
    ROOT / "docs" / "relatorio_erros_semanticos.md",
    ROOT / "generated" / "tokens_ultima_execucao.txt",
    ROOT / "generated" / "arvore_ultima_execucao.json",
    ROOT / "generated" / "tabela_simbolos_ultima_execucao.json",
    ROOT / "generated" / "arvore_atribuida_ultima_execucao.json",
    ROOT / "generated" / "relatorio_erros_ultima_execucao.txt",
    ROOT / "generated" / "relatorio_execucao_ultima_execucao.txt",
    ROOT / "generated" / "ultimo_assembly.s",
]


class AuditoriaEntregaTests(unittest.TestCase):
    def test_funcoes_exigidas_estao_expostas(self) -> None:
        import analisador_sintatico_ll1 as pacote

        for nome in [
            "prepararEntradaSemantica",
            "construirTabelaSimbolos",
            "verificarTipos",
            "gerarArvoreAtribuida",
            "gerarAssembly",
        ]:
            self.assertTrue(callable(getattr(pacote, nome)))

    def test_arquivos_obrigatorios_existentes_e_nao_vazios(self) -> None:
        for caminho in ARQUIVOS_OBRIGATORIOS:
            with self.subTest(arquivo=str(caminho.relative_to(ROOT))):
                self.assertTrue(caminho.exists(), f"Arquivo obrigatorio ausente: {caminho}")
                self.assertGreater(caminho.stat().st_size, 0, f"Arquivo vazio: {caminho}")

    def test_readme_cobre_itens_administrativos_e_semanticos(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()

        for trecho in [
            "pontificia universidade catolica do parana",
            "2026",
            "linguagens formais e compiladores",
            "frank coelho de alcantara",
            "ra3-4",
            "python analisadorsemantico.py",
            "comentarios",
            "tabela de simbolos",
            "calculo de sequentes",
            "varre o arquivo inteiro",
            "arvore sintatica atribuida",
            "arvore sintatica desenhada",
            "cpulator",
            "relatorio de validacao",
            "teste4_semantico_invalido.txt",
            "auditoria_dossie_inconformidades_fase3.md",
            "auditoria_gramatica_parser_fase3.md",
            "auditoria_semantica_tipos_fase3.md",
            "tests/invalidos",
            "tests/variacoes",
        ]:
            self.assertIn(trecho, readme)

    def test_matriz_cobertura_requisitos_existe_e_cita_pontos_criticos(self) -> None:
        matriz = (ROOT / "docs" / "matriz_cobertura_requisitos.md").read_text(encoding="utf-8")

        for trecho in [
            "Arquivos oficiais na raiz",
            "teste1.txt",
            "teste2.txt",
            "teste3.txt",
            "teste4_semantico_invalido.txt",
            "Operadores aritmeticos",
            "Operadores relacionais",
            "Operadores logicos",
            "Comentarios",
            "Varredura completa",
            "Assembly",
        ]:
            self.assertIn(trecho, matriz)

    def test_arquivos_de_teste_obrigatorios_ficam_na_raiz_e_sincronizados(self) -> None:
        for nome in NOMES_PROGRAMAS_VALIDOS:
            with self.subTest(programa=nome):
                raiz = ROOT / nome
                suite = ROOT / "tests" / nome

                self.assertTrue(raiz.exists())
                self.assertTrue(suite.exists())
                self.assertEqual(raiz.read_text(encoding="utf-8"), suite.read_text(encoding="utf-8"))

    def test_arquivo_semantico_invalido_oficial_fica_na_raiz(self) -> None:
        self.assertTrue(PROGRAMA_SEMANTICO_INVALIDO_RAIZ.exists())
        self.assertGreaterEqual(
            len([linha for linha in PROGRAMA_SEMANTICO_INVALIDO_RAIZ.read_text(encoding="utf-8").splitlines() if linha.strip()]),
            10,
        )

    def test_documentacao_registra_decisoes_para_inconformidades(self) -> None:
        decisoes = (ROOT / "docs" / "decisoes_inconformidades_fase3.md").read_text(encoding="utf-8")
        auditoria = (ROOT / "docs" / "auditoria_dossie_inconformidades_fase3.md").read_text(encoding="utf-8")

        for inc in ["INC-01", "INC-03", "INC-05", "INC-07", "INC-09", "INC-16", "INC-18"]:
            self.assertIn(inc, decisoes)
            self.assertIn(inc, auditoria)
        self.assertIn("Assembly nao e gerado para programas invalidos", decisoes)
        self.assertIn("varrer o arquivo inteiro", decisoes)
        self.assertIn("Perguntas prioritarias para o professor", auditoria)
        self.assertIn("expoente literal `0`", auditoria)

    def test_cada_programa_valido_cobre_requisitos_minimos(self) -> None:
        for caminho in PROGRAMAS_VALIDOS:
            with self.subTest(programa=caminho.name):
                texto = caminho.read_text(encoding="utf-8")
                linhas_uteis = [linha for linha in texto.splitlines() if linha.strip()]
                self.assertGreaterEqual(len(linhas_uteis), 10)
                self.assertIn("*{", texto)

                program = self._parse_program(caminho)
                inventario = self._inventariar_programa(program)
                comentarios = self._inventariar_comentarios(texto)

                self.assertTrue({"+", "-", "*", "|", "/", "%", "^"}.issubset(inventario["binary_ops"]))
                self.assertTrue({">", "<", ">=", "<=", "==", "!="}.issubset(inventario["relational_ops"]))
                self.assertTrue({"AND", "OR", "NOT"}.issubset(inventario["logical_ops"]))
                self.assertTrue(inventario["has_memory_read"])
                self.assertTrue(inventario["has_memory_write"])
                self.assertTrue(inventario["has_res"])
                self.assertTrue(inventario["has_if"])
                self.assertTrue(inventario["has_ifelse"])
                self.assertTrue(inventario["has_while"])
                self.assertTrue(inventario["has_seq"])
                self.assertTrue(inventario["has_integer_literal"])
                self.assertTrue(inventario["has_real_literal"])
                self.assertTrue(inventario["has_bool_literal"])
                self.assertGreater(comentarios["linha_inteira"], 0)
                self.assertGreater(comentarios["fim_de_linha"], 0)
                self.assertGreater(comentarios["entre_tokens"], 0)
                self.assertGreater(comentarios["multilinha"], 0)

    def test_cli_processa_programa_valido_e_atualiza_artefatos(self) -> None:
        resultado = subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", PROGRAMAS_VALIDOS[0].name],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Analise completa concluida: 0 erro(s).", resultado.stdout)
        self.assertIn("Assembly ARMv7 gerado", resultado.stdout)
        self.assertIn("Relatorio de validacao da execucao", resultado.stdout)
        self.assertIn("Lexico: OK", resultado.stdout)
        self.assertIn("Sintatico LL(1): OK", resultado.stdout)
        self.assertIn("Semantico: OK", resultado.stdout)
        self.assertIn("Operadores aritmeticos: + - * | / % ^", resultado.stdout)
        self.assertIn("Arvore sintatica desenhada:", resultado.stdout)
        self.assertIn("|-- Statement[1]", resultado.stdout)
        self.assertIn("`--", resultado.stdout)
        self.assertIn("Assembly nao e impresso no console", resultado.stdout)
        self.assertNotIn("_start:", resultado.stdout)
        self.assertNotIn("puts_jtag", resultado.stdout)

    def test_cli_mostra_arvore_sem_imprimir_assembly(self) -> None:
        resultado = subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", "teste3.txt", "--mostrar-arvore"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Arvore sintatica desenhada:", resultado.stdout)
        self.assertIn("Program", resultado.stdout)
        self.assertIn("|-- Statement[1]", resultado.stdout)
        self.assertIn("`--", resultado.stdout)
        self.assertIn("|       `-- MemoryWrite name=D\n|           `-- BinaryOp operator='+'", resultado.stdout)
        self.assertNotIn("_start:", resultado.stdout)
        self.assertNotIn("puts_jtag", resultado.stdout)

    def test_cli_rejeita_programa_semantico_invalido(self) -> None:
        resultado = subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", PROGRAMA_SEMANTICO_INVALIDO_RAIZ.name],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 1)
        self.assertIn("Erro SEMANTICO", resultado.stdout)
        self.assertIn("operador '%'", resultado.stdout)
        self.assertIn("NAOEXISTE", resultado.stdout)
        linhas_erro = [line for line in resultado.stdout.splitlines() if line.startswith("Erro SEMANTICO")]
        self.assertEqual(len(linhas_erro), 8)
        self.assertIn("  linha: 11", resultado.stdout)
        self.assertIn("  detalhe: variavel 'X' ja foi definida como int e nao pode receber real.", resultado.stdout)
        self.assertNotIn(".Erro SEMANTICO", resultado.stdout)
        self.assertNotIn("Arvore sintatica desenhada:", resultado.stdout)
        self.assertNotIn("Erro SEMANTICO", resultado.stderr)

    def test_import_publico_funciona_sem_py_path_externo(self) -> None:
        resultado = subprocess.run(
            [
                sys.executable,
                "-c",
                "import analisador_semantico; print(','.join(analisador_semantico.__all__))",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("prepararEntradaSemantica", resultado.stdout)
        self.assertIn("gerarAssembly", resultado.stdout)

    def test_pipeline_semantico_end_to_end_em_memoria(self) -> None:
        entrada = prepararEntradaSemantica(str(PROGRAMAS_VALIDOS[1]))
        resultado = construirTabelaSimbolos(entrada)
        arvore_atribuida = gerarArvoreAtribuida(entrada, resultado, resultado)
        assembly = gerarAssembly(arvore_atribuida)

        self.assertFalse(resultado.has_errors, [erro.format() for erro in resultado.errors])
        self.assertIn("symbols", resultado.symbol_table.to_dict())
        self.assertEqual(arvore_atribuida.payload["semantic_status"], "ok")
        self.assertIn("_start:", assembly)

    def _parse_program(self, caminho: Path) -> ProgramNode:
        tokens = lerTokens(caminho)
        bundle = construirGramatica()
        resultado = parsear(tokens, bundle)
        return resultado.syntax_tree_seed

    def _inventariar_programa(self, program: ProgramNode) -> dict[str, object]:
        inventario = {
            "binary_ops": set(),
            "relational_ops": set(),
            "logical_ops": set(),
            "has_memory_read": False,
            "has_memory_write": False,
            "has_res": False,
            "has_if": False,
            "has_ifelse": False,
            "has_while": False,
            "has_seq": False,
            "has_integer_literal": False,
            "has_real_literal": False,
            "has_bool_literal": False,
        }
        for statement in program.statements:
            self._visitar(statement.node, inventario)
        return inventario

    def _visitar(self, node, inventario: dict[str, object]) -> None:
        if isinstance(node, NumberNode):
            if node.is_integer_literal:
                inventario["has_integer_literal"] = True
            else:
                inventario["has_real_literal"] = True
            return
        if isinstance(node, BoolNode):
            inventario["has_bool_literal"] = True
            return
        if isinstance(node, MemoryReadNode):
            inventario["has_memory_read"] = True
            return
        if isinstance(node, ResultRefNode):
            inventario["has_res"] = True
            return
        if isinstance(node, MemoryWriteNode):
            inventario["has_memory_write"] = True
            self._visitar(node.value, inventario)
            return
        if isinstance(node, BinaryOpNode):
            inventario["binary_ops"].add(node.operator)
            self._visitar(node.left, inventario)
            self._visitar(node.right, inventario)
            return
        if isinstance(node, RelationalOpNode):
            inventario["relational_ops"].add(node.operator)
            self._visitar(node.left, inventario)
            self._visitar(node.right, inventario)
            return
        if isinstance(node, LogicalOpNode):
            inventario["logical_ops"].add(node.operator)
            self._visitar(node.left, inventario)
            self._visitar(node.right, inventario)
            return
        if isinstance(node, LogicalNotNode):
            inventario["logical_ops"].add("NOT")
            self._visitar(node.operand, inventario)
            return
        if isinstance(node, SequenceNode):
            inventario["has_seq"] = True
            self._visitar(node.first, inventario)
            self._visitar(node.second, inventario)
            return
        if isinstance(node, IfNode):
            inventario["has_if"] = True
            if node.else_branch is not None:
                inventario["has_ifelse"] = True
            self._visitar(node.condition, inventario)
            self._visitar(node.then_branch, inventario)
            if node.else_branch is not None:
                self._visitar(node.else_branch, inventario)
            return
        if isinstance(node, WhileNode):
            inventario["has_while"] = True
            self._visitar(node.condition, inventario)
            self._visitar(node.body, inventario)

    def _inventariar_comentarios(self, text: str) -> dict[str, int]:
        counts = {"linha_inteira": 0, "fim_de_linha": 0, "entre_tokens": 0, "multilinha": 0}
        for match in re.finditer(r"\*\{.*?\}\*", text, flags=re.DOTALL):
            comment = match.group(0)
            before_line = text[text.rfind("\n", 0, match.start()) + 1 : match.start()]
            after_line_end = text.find("\n", match.end())
            if after_line_end == -1:
                after_line_end = len(text)
            after_line = text[match.end() : after_line_end]

            if "\n" in comment:
                counts["multilinha"] += 1
            elif not before_line.strip() and not after_line.strip():
                counts["linha_inteira"] += 1
            elif before_line.strip() and not after_line.strip():
                counts["fim_de_linha"] += 1
            else:
                counts["entre_tokens"] += 1
        return counts


if __name__ == "__main__":
    unittest.main()
