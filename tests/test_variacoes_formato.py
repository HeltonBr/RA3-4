# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from analisador_sintatico_ll1 import construirGramatica
from analisador_sintatico_ll1 import gerarArvore
from analisador_sintatico_ll1 import gerarAssembly
from analisador_sintatico_ll1 import lerTokens
from analisador_sintatico_ll1 import parsear
from analisador_sintatico_ll1 import prepararEntradaSemanticaComDiagnosticos
from analisador_sintatico_ll1.errors import LexicalTokenError
from analisador_sintatico_ll1.errors import SyntaxAnalysisError


ROOT = Path(__file__).resolve().parents[1]


class VariacoesFormatoTests(unittest.TestCase):
    def test_programas_com_espacos_tabs_e_seq_longo_funcionam(self) -> None:
        for caminho in sorted((ROOT / "tests" / "variacoes").glob("*.txt")):
            with self.subTest(programa=caminho.name):
                tokens = lerTokens(caminho)
                resultado = parsear(tokens, construirGramatica())
                arvore = gerarArvore(resultado)
                assembly = gerarAssembly(arvore)

                self.assertGreaterEqual(arvore["program"]["statement_count"], 9)
                self.assertIn("Program", arvore["tree_text"])
                self.assertIn("while_start_", assembly)
                self.assertIn("puts_jtag", assembly)

    def test_cli_processa_variacao_com_espacos_e_tabs(self) -> None:
        caminho = ROOT / "tests" / "variacoes" / "espacos_tabs_linhas.txt"
        resultado = subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", str(caminho)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Analise concluida para:", resultado.stdout)

    def test_comentario_multilinha_e_descartado_sem_perder_posicoes(self) -> None:
        caminho = ROOT / "tests" / "variacoes" / "comentario_multilinha.txt"
        tokens = lerTokens(caminho)
        lexemas = [token.lexeme for linha in tokens for token in linha]

        self.assertEqual(tokens[1][0].line, 5)
        self.assertEqual(tokens[1][2].lexeme, "M")
        self.assertNotIn("comentario", lexemas)
        self.assertNotIn("declaracoes", lexemas)

    def test_palavras_reservadas_nao_sao_identificadores_de_memoria(self) -> None:
        caminho = ROOT / "tests" / "invalidos" / "sintaxe_palavra_reservada_memoria.txt"
        entrada = prepararEntradaSemanticaComDiagnosticos(str(caminho))
        mensagens = "\n".join(diagnostic.format() for diagnostic in entrada.diagnostics)

        self.assertGreaterEqual(len(entrada.diagnostics), 2)
        self.assertIn("Erro SINTATICO", mensagens)
        self.assertIn("linha 2", mensagens)
        self.assertIn("linha 3", mensagens)
        self.assertIn("'START'", mensagens)
        self.assertIn("'AND'", mensagens)

    def test_numero_malformado_e_erro_lexico(self) -> None:
        caminho = ROOT / "tests" / "invalidos" / "lexico_numero_malformado.txt"

        with self.assertRaisesRegex(LexicalTokenError, "Numero malformado"):
            lerTokens(caminho)

    def test_declaracoes_de_topo_na_mesma_linha_sao_rejeitadas(self) -> None:
        caminho = ROOT / "tests" / "invalidos" / "sintaxe_multiplas_declaracoes_mesma_linha.txt"
        tokens = lerTokens(caminho)

        with self.assertRaisesRegex(SyntaxAnalysisError, "fim de linha"):
            parsear(tokens, construirGramatica())

    def test_expressao_vazia_e_rejeitada_com_erro_sintatico(self) -> None:
        caminho = ROOT / "tests" / "invalidos" / "sintaxe_expressao_vazia.txt"
        tokens = lerTokens(caminho)

        with self.assertRaisesRegex(SyntaxAnalysisError, "Declaracao vazia"):
            parsear(tokens, construirGramatica())


if __name__ == "__main__":
    unittest.main()
