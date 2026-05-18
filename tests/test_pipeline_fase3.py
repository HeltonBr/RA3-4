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
from analisador_sintatico_ll1 import construirTabelaSimbolos
from analisador_sintatico_ll1 import gerarArvore
from analisador_sintatico_ll1 import gerarArvoreAtribuida
from analisador_sintatico_ll1 import gerarAssembly
from analisador_sintatico_ll1 import lerTokens
from analisador_sintatico_ll1 import parsear
from analisador_sintatico_ll1 import prepararEntradaSemantica
from analisador_sintatico_ll1 import verificarTipos
from analisador_sintatico_ll1.errors import AssemblyGenerationError
from analisador_sintatico_ll1.errors import LexicalTokenError
from analisador_sintatico_ll1.errors import SyntaxAnalysisError


ROOT = Path(__file__).resolve().parents[1]


class PipelineFase3Tests(unittest.TestCase):
    def test_construir_gramatica_sem_conflitos_com_bool_e_logicos(self) -> None:
        bundle = construirGramatica()

        self.assertEqual(bundle.start_symbol, "program")
        self.assertIn("logical_op", bundle.productions)
        self.assertEqual(bundle.parsing_table["item"]["BOOL_LITERAL"], ["BOOL_LITERAL"])
        self.assertEqual(bundle.parsing_table["stmt_after_first"]["OP_NOT"], ["OP_NOT"])
        self.assertEqual(bundle.parsing_table["stmt_after_second"]["OP_AND"], ["logical_op"])

    def test_programas_validos_passam_semantica_e_geram_assembly(self) -> None:
        for nome_arquivo in ["teste1.txt", "teste2.txt", "teste3.txt"]:
            with self.subTest(programa=nome_arquivo):
                entrada = prepararEntradaSemantica(str(ROOT / nome_arquivo))
                tabela = construirTabelaSimbolos(entrada)
                tipos = verificarTipos(entrada, tabela)
                arvore_atribuida = gerarArvoreAtribuida(entrada, tabela, tipos)
                assembly = gerarAssembly(arvore_atribuida)

                self.assertFalse(tipos.has_errors, [erro.format() for erro in tipos.errors])
                self.assertGreaterEqual(arvore_atribuida.payload["statement_count"], 10)
                self.assertGreaterEqual(len(tabela.symbol_table.symbols), 3)
                self.assertIn("_start:", assembly)
                self.assertIn("while_start_", assembly)

    def test_comentarios_sao_descartados_sem_perder_linhas(self) -> None:
        tokens = lerTokens(ROOT / "teste1.txt")
        lexemas = [token.lexeme for linha in tokens for token in linha]

        self.assertNotIn("*{", lexemas)
        self.assertIn("START", lexemas)
        self.assertIn("END", lexemas)

    def test_parser_detecta_erro_lexico(self) -> None:
        caminho = ROOT / "lexico_minusculo.txt"

        with self.assertRaises(LexicalTokenError):
            lerTokens(caminho)

    def test_parser_detecta_erro_sintatico(self) -> None:
        caminho = ROOT / "sintaxe_sem_end.txt"
        tokens = lerTokens(caminho)
        bundle = construirGramatica()

        with self.assertRaises(SyntaxAnalysisError):
            parsear(tokens, bundle)

    def test_semantico_detecta_variavel_antes_da_definicao(self) -> None:
        entrada = prepararEntradaSemantica(str(ROOT / "semantico_variavel_nao_definida.txt"))
        resultado = construirTabelaSimbolos(entrada)

        self.assertTrue(resultado.has_errors)
        self.assertIn("usada antes da definicao", resultado.errors[0].message)

    def test_semantico_bloqueia_assembly_com_erro(self) -> None:
        entrada = prepararEntradaSemantica(str(ROOT / "semantico_tipo_incompativel.txt"))
        resultado = construirTabelaSimbolos(entrada)
        arvore_atribuida = gerarArvoreAtribuida(entrada, resultado, resultado)

        with self.assertRaises(AssemblyGenerationError):
            gerarAssembly(arvore_atribuida)

    def test_cli_retorna_erro_semantico_sem_traceback(self) -> None:
        caminho = ROOT / "semantico_condicao_nao_bool.txt"
        resultado = subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", str(caminho)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 1)
        saida = resultado.stdout + resultado.stderr
        self.assertIn("Erro SEMANTICO", saida)
        self.assertIn("condicao de WHILE deve ser bool", saida)
        self.assertNotIn("Traceback", saida)

    def test_cli_varre_arquivo_inteiro_e_lista_multiplos_erros(self) -> None:
        caminho = ROOT / "auditoria_multiplos_erros.txt"
        resultado = subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", str(caminho)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 1)
        saida = resultado.stdout + resultado.stderr
        self.assertIn("Analise completa concluida com", saida)
        self.assertIn("Erro LEXICO", saida)
        self.assertIn("Erro SINTATICO", saida)
        self.assertIn("Erro SEMANTICO", saida)
        self.assertIn("NAODECLARADA", saida)
        self.assertIn("numero malformado", saida)
        self.assertIn("variavel 'X' ja foi definida", saida)
        self.assertIn("condicao de WHILE deve ser bool", saida)
        self.assertNotIn("Traceback", saida)

    def test_cli_retorna_mensagem_clara_para_end_ausente(self) -> None:
        caminho = ROOT / "sintaxe_sem_end.txt"
        resultado = subprocess.run(
            [sys.executable, "AnalisadorSemantico.py", str(caminho)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(resultado.returncode, 1)
        saida = resultado.stdout + resultado.stderr
        self.assertIn("Programa incompleto: faltou a linha final (END).", saida)
        self.assertNotIn("Traceback", saida)


if __name__ == "__main__":
    unittest.main()
