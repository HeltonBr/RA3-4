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
VALIDOS_OFICIAIS = ("teste1.txt", "teste2.txt", "teste3.txt")
INVALIDO_OFICIAL = "teste4_semantico_invalido.txt"
VALIDO_SURPRESA = ROOT / "professor_surpresa_valido.txt"
INVALIDO_SURPRESA = ROOT / "professor_surpresa_invalido.txt"


class ValidacaoHumanaCompletaTests(unittest.TestCase):
    def test_linha_humana_oficial_executa_validos_e_invalido(self) -> None:
        for nome_arquivo in VALIDOS_OFICIAIS:
            with self.subTest(programa=nome_arquivo):
                resultado = self._executar_cli(nome_arquivo)
                self.assertEqual(resultado.returncode, 0, resultado.stderr)
                self.assertIn("Analise completa concluida: 0 erro(s).", resultado.stdout)
                self.assertIn("Arvore sintatica desenhada:", resultado.stdout)
                self.assertIn("Assembly ARMv7 gerado em: generated/ultimo_assembly.s", resultado.stdout)
                self.assertNotIn("_start:", resultado.stdout)

        invalido = self._executar_cli(INVALIDO_OFICIAL)
        self.assertEqual(invalido.returncode, 1)
        self.assertIn("Analise completa concluida com", invalido.stdout)
        self.assertIn("Erro SEMANTICO", invalido.stdout)
        self.assertIn("Assembly nao gerado porque ha erros lexicos, sintaticos ou semanticos.", invalido.stdout)
        self.assertNotIn("Traceback", invalido.stdout + invalido.stderr)

    def test_entradas_surpresa_simulam_prova_do_professor(self) -> None:
        valido = self._executar_cli(str(VALIDO_SURPRESA))
        self.assertEqual(valido.returncode, 0, valido.stderr)
        self.assertIn("Lexico: OK", valido.stdout)
        self.assertIn("Sintatico LL(1): OK", valido.stdout)
        self.assertIn("Semantico: OK", valido.stdout)
        self.assertIn("Assembly ARMv7 gerado em: generated/ultimo_assembly.s", valido.stdout)
        self.assertIn("Arvore sintatica desenhada:", valido.stdout)

        invalido = self._executar_cli(str(INVALIDO_SURPRESA))
        self.assertEqual(invalido.returncode, 1)
        self.assertGreaterEqual(invalido.stdout.count("Erro SEMANTICO"), 8)
        self.assertIn("variavel 'NAODECLARADA' usada antes da definicao", invalido.stdout)
        self.assertIn("Assembly nao gerado porque ha erros lexicos, sintaticos ou semanticos.", invalido.stdout)
        self.assertNotIn("Traceback", invalido.stdout + invalido.stderr)

    def test_roteiro_e_script_de_validacao_humana_estao_presentes(self) -> None:
        roteiro = (ROOT / "docs" / "validacao_humana_completa_fase3.md").read_text(encoding="utf-8")
        script = (ROOT / "validar_linha_humana.ps1").read_text(encoding="utf-8")

        for trecho in [
            "python -m unittest discover -s tests -p \"test_*.py\" -v",
            "python AnalisadorSemantico.py teste1.txt",
            "python AnalisadorSemantico.py teste4_semantico_invalido.txt",
            "professor_surpresa_valido.txt",
            "professor_surpresa_invalido.txt",
        ]:
            self.assertIn(trecho, roteiro)
            self.assertIn(trecho, script)

    def _executar_cli(self, arquivo: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", arquivo],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
