# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFESA = ROOT / "defesa"


class KitDefesaTests(unittest.TestCase):
    def _rodar(self, nome: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", str(DEFESA / nome)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_demo_valido_base_processa(self) -> None:
        resultado = self._rodar("demo_valido_base.txt")

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Analise concluida para:", resultado.stdout)

    def test_demo_valido_alterado_processa(self) -> None:
        resultado = self._rodar("demo_valido_alterado.txt")

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Analise concluida para:", resultado.stdout)

    def test_demo_erro_lexico_retorna_erro_claro(self) -> None:
        resultado = self._rodar("demo_erro_lexico.txt")

        self.assertEqual(resultado.returncode, 1)
        saida = resultado.stdout + resultado.stderr
        self.assertIn("Erro LEXICO", saida)
        self.assertNotIn("Traceback", saida)

    def test_demo_erro_sintatico_retorna_erro_claro(self) -> None:
        resultado = self._rodar("demo_erro_sintatico.txt")

        self.assertEqual(resultado.returncode, 1)
        saida = resultado.stdout + resultado.stderr
        self.assertIn("Erro SINTATICO", saida)
        self.assertNotIn("Traceback", saida)


if __name__ == "__main__":
    unittest.main()
