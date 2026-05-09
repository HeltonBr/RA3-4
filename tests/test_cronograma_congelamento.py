# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CronogramaCongelamentoTests(unittest.TestCase):
    def test_cronograma_registra_prs_diarios_ate_sete_dias_antes(self) -> None:
        cronograma = (ROOT / "docs" / "cronograma_commits_prs_fase3.md").read_text(encoding="utf-8")

        self.assertIn("25/05/2026 as 23:59", cronograma)
        self.assertIn("09/05/2026 a 18/05/2026", cronograma)
        self.assertIn("19/05/2026 a 25/05/2026", cronograma)
        for dia in range(9, 19):
            self.assertIn(f"{dia:02d}/05/2026", cronograma)
        self.assertIn("PR 10 - Pre-auditoria final", cronograma)

    def test_bateria_pesada_cobre_sete_dias_finais(self) -> None:
        bateria = (ROOT / "docs" / "bateria_pesada_testes_fase3.md").read_text(encoding="utf-8")

        for dia in range(19, 26):
            self.assertIn(f"{dia:02d}/05/2026", bateria)
        for requisito in [
            "Erro lexico sem traceback",
            "Erro sintatico sem traceback",
            "Erro semantico sem traceback",
            "Tabela de simbolos registra definicao",
            "Arvore atribuida registra tipos",
            "Assembly nao e gerado para programa invalido",
            "GitHubmirror esta identico",
        ]:
            self.assertIn(requisito, bateria)

    def test_script_de_espelho_tem_prazo_e_protecao_basica(self) -> None:
        script = (ROOT / "sincronizar_para_githubmirror.ps1").read_text(encoding="utf-8")

        self.assertIn("GitHubmirror", script)
        self.assertIn("2026-05-25T23:59:00", script)
        self.assertIn("/MIR", script)
        self.assertIn("Destino invalido", script)
        self.assertIn("copia recursiva", script)


if __name__ == "__main__":
    unittest.main()
