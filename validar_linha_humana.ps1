# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

$ErrorActionPreference = "Stop"

$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $raiz

# Comandos oficiais cobertos por este roteiro, todos com arquivos-fonte na raiz:
# python AnalisadorSemantico.py teste1.txt
# python AnalisadorSemantico.py teste2.txt
# python AnalisadorSemantico.py teste4_semantico_invalido.txt
# python AnalisadorSemantico.py teste3.txt

$comandos = @(
    @{ Nome = "teste1 valido"; Esperado = 0; Args = @("AnalisadorSemantico.py", "teste1.txt") },
    @{ Nome = "teste2 valido"; Esperado = 0; Args = @("AnalisadorSemantico.py", "teste2.txt") },
    @{ Nome = "teste4 semantico invalido"; Esperado = 1; Args = @("AnalisadorSemantico.py", "teste4_semantico_invalido.txt") },
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
Write-Host "Validacao oficial concluida com sucesso."
