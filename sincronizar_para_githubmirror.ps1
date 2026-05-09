# Integrantes do grupo (ordem alfabetica):
# Helton Tessari Brandao - HeltonBr
#
# Nome do grupo no Canvas: RA3-4

param(
    [string]$Destino = ""
)

$ErrorActionPreference = "Stop"

$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
$origem = (Resolve-Path -LiteralPath $raiz).Path

if ([string]::IsNullOrWhiteSpace($Destino)) {
    $pai = Split-Path -Parent $origem
    $Destino = Join-Path $pai "GitHubmirror"
}

$destinoAbsoluto = [System.IO.Path]::GetFullPath($Destino)
$origemNormalizada = [System.IO.Path]::GetFullPath($origem).TrimEnd('\')
$destinoNormalizado = $destinoAbsoluto.TrimEnd('\')

if ($destinoNormalizado -eq $origemNormalizada) {
    throw "Destino invalido: o espelho nao pode ser a propria pasta principal."
}

if ($destinoNormalizado.StartsWith($origemNormalizada + '\')) {
    throw "Destino invalido: GitHubmirror nao pode ficar dentro da pasta principal, para evitar copia recursiva."
}

$agora = Get-Date
$congelamento = [datetime]"2026-05-25T23:59:00"
if ($agora -gt $congelamento) {
    throw "Sincronizacao bloqueada: apos 25/05/2026 23:59 a pasta principal e o GitHub devem permanecer congelados."
}

New-Item -ItemType Directory -Force -Path $destinoAbsoluto | Out-Null

Write-Host "Origem:  $origemNormalizada"
Write-Host "Destino: $destinoNormalizado"
Write-Host "Prazo de congelamento: 25/05/2026 23:59"

robocopy $origemNormalizada $destinoNormalizado /MIR /FFT /R:2 /W:2 /XJ
$codigo = $LASTEXITCODE

if ($codigo -gt 7) {
    throw "Falha ao sincronizar GitHubmirror. Codigo do robocopy: $codigo"
}

Write-Host "GitHubmirror sincronizado com sucesso. Codigo do robocopy: $codigo"
Write-Host "Repita a sincronizacao apos cada merge aprovado ate 25/05/2026 23:59."
