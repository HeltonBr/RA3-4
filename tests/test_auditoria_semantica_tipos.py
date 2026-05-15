# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from analisador_sintatico_ll1 import construirTabelaSimbolos
from analisador_sintatico_ll1 import prepararEntradaSemantica


class AuditoriaSemanticaTiposTests(unittest.TestCase):
    def test_matriz_valida_de_tipos_retorna_tipos_esperados(self) -> None:
        resultado = self._analisar(
            [
                "(2 A)",
                "(3.5 B)",
                "(TRUE FLAG)",
                "((A) (B) +)",
                "((A) 2 /)",
                "((A) 2 %)",
                "((B) 2 |)",
                "((B) 2 ^)",
                "((A) (B) >)",
                "((FLAG) TRUE AND)",
                "((FLAG) NOT)",
            ]
        )

        self.assertFalse(resultado.has_errors, [erro.format() for erro in resultado.errors])
        self.assertEqual(resultado.statement_types[4], "real")
        self.assertEqual(resultado.statement_types[5], "int")
        self.assertEqual(resultado.statement_types[6], "int")
        self.assertEqual(resultado.statement_types[7], "real")
        self.assertEqual(resultado.statement_types[8], "real")
        self.assertEqual(resultado.statement_types[9], "bool")
        self.assertEqual(resultado.statement_types[10], "bool")
        self.assertEqual(resultado.statement_types[11], "bool")

    def test_matriz_invalida_acumula_erros_semanticos_de_tipos(self) -> None:
        resultado = self._analisar(
            [
                "(2 A)",
                "(TRUE FLAG)",
                "((A) 1.5 %)",
                "((FLAG) 1 +)",
                "((A) TRUE AND)",
                "((A) NOT)",
                "((FLAG) 1 >)",
                "((FLAG) 1 ==)",
                "((A) (((A) 1 -) A) WHILE)",
                "((A) (((A) 1 -) A) IF)",
                "(2 1.5 ^)",
            ]
        )

        codigos = {erro.code for erro in resultado.errors}
        self.assertIn("INT_ONLY_OP", codigos)
        self.assertIn("ARITH_TYPE", codigos)
        self.assertIn("LOGICAL_TYPE", codigos)
        self.assertIn("LOGICAL_NOT_TYPE", codigos)
        self.assertIn("RELATIONAL_ORDER_TYPE", codigos)
        self.assertIn("RELATIONAL_EQUALITY_TYPE", codigos)
        self.assertIn("WHILE_CONDITION", codigos)
        self.assertIn("IF_CONDITION", codigos)
        self.assertIn("POW_TYPE", codigos)
        self.assertGreaterEqual(len(resultado.errors), 9)

    def test_res_reatribuicao_e_comando_sem_valor_sao_rejeitados(self) -> None:
        resultado = self._analisar(
            [
                "(10 A)",
                "((1 RES) 2 +)",
                "(0 RES)",
                "((5 RES) 1 +)",
                "(TRUE B)",
                "(1 B)",
                "(((A) 0 >) (((A) 1 -) A) WHILE)",
                "((1 RES) 1 +)",
            ]
        )

        codigos = [erro.code for erro in resultado.errors]
        self.assertIn("RES_ZERO", codigos)
        self.assertIn("RES_OUT_OF_RANGE", codigos)
        self.assertIn("VAR_TYPE_REDEFINITION", codigos)
        self.assertIn("RES_NO_VALUE", codigos)

    def test_potenciacao_com_expoente_inteiro_em_memoria_continua_aceita(self) -> None:
        resultado = self._analisar(
            [
                "(2 BASE)",
                "(3 EXP)",
                "((BASE) (EXP) ^)",
            ]
        )

        self.assertFalse(resultado.has_errors, [erro.format() for erro in resultado.errors])
        self.assertEqual(resultado.statement_types[3], "int")

    def test_zero_em_potenciacao_e_divisao_dupla_sao_aceitos(self) -> None:
        resultado = self._analisar(
            [
                "(10 BASE)",
                "((BASE) 0 ^)",
                "((BASE) 2 //)",
            ]
        )

        self.assertFalse(resultado.has_errors, [erro.format() for erro in resultado.errors])
        self.assertEqual(resultado.statement_types[2], "int")
        self.assertEqual(resultado.statement_types[3], "int")

    def _analisar(self, linhas: list[str]):
        fonte = "\n".join(["(START)", *linhas, "(END)"]) + "\n"
        with tempfile.TemporaryDirectory() as tmp_dir:
            caminho = Path(tmp_dir) / "programa.txt"
            caminho.write_text(fonte, encoding="utf-8")
            entrada = prepararEntradaSemantica(str(caminho))
            return construirTabelaSimbolos(entrada)


if __name__ == "__main__":
    unittest.main()
