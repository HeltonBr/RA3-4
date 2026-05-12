# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import inspect
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from analisador_sintatico_ll1 import construirGramatica
from analisador_sintatico_ll1.main import _inventariar_comentarios


ROOT = Path(__file__).resolve().parents[1]


class AuditoriaGramaticaParserTests(unittest.TestCase):
    def test_first_follow_e_tabela_ll1_cobrem_pontos_criticos(self) -> None:
        bundle = construirGramatica()

        self.assertEqual(bundle.start_symbol, "program")
        self.assertIn("EOF", bundle.follow["program"])
        self.assertEqual(bundle.parsing_table["program"]["LPAREN"], ["start_line", "program_body"])
        self.assertEqual(bundle.parsing_table["program_body_after_lparen"]["KW_END"], ["KW_END", "RPAREN", "EOL", "EOF"])

        for terminal in ["NUMBER", "BOOL_LITERAL", "LPAREN"]:
            with self.subTest(nonterminal="stmt_inner", terminal=terminal):
                self.assertEqual(bundle.parsing_table["stmt_inner"][terminal], ["item", "stmt_after_first"])

        self.assertEqual(bundle.parsing_table["stmt_inner"]["IDENTIFIER"], ["IDENTIFIER"])
        self.assertEqual(bundle.parsing_table["stmt_after_first"]["KW_RES"], ["KW_RES"])
        self.assertEqual(bundle.parsing_table["stmt_after_first"]["IDENTIFIER"], ["IDENTIFIER"])
        self.assertEqual(bundle.parsing_table["stmt_after_first"]["OP_NOT"], ["OP_NOT"])

        for terminal in ["OP_PLUS", "OP_MINUS", "OP_MULT", "OP_REAL_DIV", "OP_INT_DIV", "OP_MOD", "OP_POW"]:
            with self.subTest(nonterminal="stmt_after_second", terminal=terminal):
                self.assertEqual(bundle.parsing_table["stmt_after_second"][terminal], ["binary_op"])

        for terminal in ["OP_GT", "OP_LT", "OP_GTE", "OP_LTE", "OP_EQ", "OP_NEQ"]:
            with self.subTest(nonterminal="stmt_after_second", terminal=terminal):
                self.assertEqual(bundle.parsing_table["stmt_after_second"][terminal], ["relational_op"])

        self.assertEqual(bundle.parsing_table["stmt_after_second"]["OP_AND"], ["logical_op"])
        self.assertEqual(bundle.parsing_table["stmt_after_second"]["OP_OR"], ["logical_op"])
        self.assertEqual(bundle.parsing_table["stmt_after_second"]["KW_IF"], ["KW_IF"])
        self.assertEqual(bundle.parsing_table["stmt_after_second"]["KW_WHILE"], ["KW_WHILE"])
        self.assertEqual(bundle.parsing_table["stmt_after_second"]["KW_SEQ"], ["KW_SEQ"])
        for terminal in ["NUMBER", "BOOL_LITERAL", "LPAREN"]:
            with self.subTest(nonterminal="stmt_after_second", terminal=terminal, estrutura="IFELSE"):
                self.assertEqual(bundle.parsing_table["stmt_after_second"][terminal], ["item", "KW_IFELSE"])

    def test_cli_acumula_erros_sintaticos_estruturais_sem_interromper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            arquivo = Path(tmp_dir) / "sintaxe_multiplos_erros.txt"
            arquivo.write_text(
                "\n".join(
                    [
                        "(START)",
                        "()",
                        "(START)",
                        "(1 2)",
                        "(END)",
                        "(1 2 +)",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            resultado = subprocess.run(
                [sys.executable, "AnalisadorSemantico.py", str(arquivo)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

        saida = resultado.stdout + resultado.stderr
        self.assertEqual(resultado.returncode, 1)
        self.assertGreaterEqual(saida.count("Erro SINTATICO"), 4)
        self.assertIn("Declaracao vazia encontrada", saida)
        self.assertIn("'(START)' so pode aparecer na primeira linha processavel", saida)
        self.assertIn("apos dois itens era esperado", saida)
        self.assertIn("conteudo encontrado apos a linha final '(END)'", saida)
        self.assertNotIn("Traceback", saida)

    def test_inventario_de_comentarios_nao_depende_de_regex(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            arquivo = Path(tmp_dir) / "comentarios.txt"
            arquivo.write_text(
                "\n".join(
                    [
                        "*{ linha inteira }*",
                        "(START)",
                        "(1 *{ entre tokens }* A)",
                        "(2 B) *{ fim de linha }*",
                        "*{ bloco",
                        "multilinha }*",
                        "(END)",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            comentarios = _inventariar_comentarios(arquivo)

        self.assertEqual(comentarios["linha_inteira"], 1)
        self.assertEqual(comentarios["entre_tokens"], 1)
        self.assertEqual(comentarios["fim_de_linha"], 1)
        self.assertEqual(comentarios["multilinha"], 1)

        fonte = inspect.getsource(_inventariar_comentarios)
        self.assertNotIn("re.", fonte)
        self.assertNotIn("finditer", fonte)


if __name__ == "__main__":
    unittest.main()
