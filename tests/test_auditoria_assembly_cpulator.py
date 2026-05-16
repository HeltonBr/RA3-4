# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSEMBLY_PATH = ROOT / "generated" / "ultimo_assembly.s"
RELATORIO_EXECUCAO_PATH = ROOT / "generated" / "relatorio_execucao_ultima_execucao.txt"
PROGRAMAS_VALIDOS = ("teste1.txt", "teste2.txt", "teste3.txt")


class AuditoriaAssemblyCpulatorTests(unittest.TestCase):
    def test_programas_validos_geram_assembly_armv7_cpulator(self) -> None:
        for nome_arquivo in PROGRAMAS_VALIDOS:
            with self.subTest(programa=nome_arquivo):
                resultado = self._executar_cli(nome_arquivo)

                self.assertEqual(resultado.returncode, 0, resultado.stderr)
                self.assertIn("Analise completa concluida: 0 erro(s).", resultado.stdout)
                self.assertIn("Assembly ARMv7 gerado em: generated/ultimo_assembly.s", resultado.stdout)
                self.assertNotIn(".syntax unified", resultado.stdout)
                self.assertNotIn("_start:", resultado.stdout)

                assembly = ASSEMBLY_PATH.read_text(encoding="utf-8")
                for trecho in [
                    ".syntax unified",
                    ".arch armv7-a",
                    ".fpu vfpv3",
                    ".global _start",
                    ".text",
                    "_start:",
                    "program_end:",
                    ".data",
                    "jtag_putc:",
                    "puts_jtag:",
                    "print_qword_hex_d0:",
                    "0xFF201000",
                ]:
                    self.assertIn(trecho, assembly)
                self.assertRegex(assembly, r"msg_line_\d+:")
                self.assertNotIn("Assembly nao gerado", assembly)

    def test_operadores_especificos_usam_rotinas_runtime_esperadas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            caminho = Path(tmp_dir) / "assembly_operadores_confirmados.txt"
            caminho.write_text(
                "\n".join(
                    [
                        "(START)",
                        "(2 BASE)",
                        "((BASE) 0 ^)",
                        "((BASE) 2 //)",
                        "(9 4 %)",
                        "(9.0 2 |)",
                        "(END)",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            resultado = self._executar_cli(str(caminho))

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        assembly = ASSEMBLY_PATH.read_text(encoding="utf-8")

        for trecho in [
            "bl pow_double_int",
            "pow_double_int:",
            "pow_double_int_zero:",
            "bl intdiv_double",
            "intdiv_double:",
            "bl mod_double",
            "mod_double:",
            "signed_divmod32:",
            "vdiv.f64 d0, d0, d1",
        ]:
            self.assertIn(trecho, assembly)

    def test_programa_invalido_bloqueia_assembly_e_grava_marcador(self) -> None:
        resultado = self._executar_cli("teste4_semantico_invalido.txt")

        self.assertEqual(resultado.returncode, 1)
        self.assertIn("Assembly nao gerado porque ha erros lexicos, sintaticos ou semanticos.", resultado.stdout)
        assembly = ASSEMBLY_PATH.read_text(encoding="utf-8")
        relatorio_execucao = RELATORIO_EXECUCAO_PATH.read_text(encoding="utf-8")

        self.assertIn("Assembly nao gerado", assembly)
        self.assertNotIn(".global _start", assembly)
        self.assertNotIn("_start:", assembly)
        self.assertIn("- Assembly ARMv7: nao gerado por erros na analise", relatorio_execucao)

    def _executar_cli(self, arquivo: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", arquivo],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
