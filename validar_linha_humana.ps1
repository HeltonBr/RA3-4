# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

$ErrorActionPreference = "Stop"

$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $raiz

# Comandos canonicos cobertos por este roteiro:
# python -m unittest discover -s tests -p "test_*.py" -v
# python AnalisadorSemantico.py teste1.txt
# python AnalisadorSemantico.py teste2.txt
# python AnalisadorSemantico.py teste3.txt
# python AnalisadorSemantico.py teste4_semantico_invalido.txt
# python AnalisadorSemantico.py tests\autoria\professor_surpresa_valido.txt
# python AnalisadorSemantico.py tests\autoria\professor_surpresa_invalido.txt

$comandos = @(
    @{ Nome = "suite completa"; Esperado = 0; Args = @("-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v") },
    @{ Nome = "teste1 valido"; Esperado = 0; Args = @("AnalisadorSemantico.py", "teste1.txt") },
    @{ Nome = "teste2 valido"; Esperado = 0; Args = @("AnalisadorSemantico.py", "teste2.txt") },
    @{ Nome = "teste3 valido"; Esperado = 0; Args = @("AnalisadorSemantico.py", "teste3.txt") },
    @{ Nome = "teste4 semantico invalido"; Esperado = 1; Args = @("AnalisadorSemantico.py", "teste4_semantico_invalido.txt") },
    @{ Nome = "surpresa valido"; Esperado = 0; Args = @("AnalisadorSemantico.py", "tests\autoria\professor_surpresa_valido.txt") },
    @{ Nome = "surpresa invalido"; Esperado = 1; Args = @("AnalisadorSemantico.py", "tests\autoria\professor_surpresa_invalido.txt") },
    @{ Nome = "regeneracao canonica teste3"; Esperado = 0; Args = @("AnalisadorSemantico.py", "teste3.txt") }
)

foreach ($comando in $comandos) {
    Write-Host ""
    Write-Host "==> $($comando.Nome)"
    Write-Host "python $($comando.Args -join ' ')"
    & python @($comando.Args)
    $codigo = $LASTEXITCODE
    if ($codigo -ne $comando.Esperado) {
        throw "Falha em '$($comando.Nome)': esperado codigo $($comando.Esperado), obtido $codigo."
    }
}

Write-Host ""
Write-Host "Validacao humana completa concluida com sucesso."
