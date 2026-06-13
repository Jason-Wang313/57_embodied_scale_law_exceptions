$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PaperDir = Join-Path $Root "paper"
$DownloadsPdf = "C:\Users\wangz\Downloads\57.pdf"
$LocalPdf = Join-Path $PaperDir "main.pdf"
$BuildStatus = Join-Path $Root "data\build_status.json"

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Host
    bibtex main | Out-Host
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Host
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Host
}
finally {
    Pop-Location
}

Copy-Item -LiteralPath $LocalPdf -Destination $DownloadsPdf -Force
Remove-Item -LiteralPath $LocalPdf -Force

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $BuildStatus) | Out-Null
$Status = [ordered]@{
    paper = 57
    decision = "workshop-only"
    canonical_pdf = $DownloadsPdf
    local_pdf_removed = -not (Test-Path -LiteralPath $LocalPdf)
    built_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")
}
$Status | ConvertTo-Json | Set-Content -Path $BuildStatus -Encoding UTF8

Get-Item -LiteralPath $DownloadsPdf | Select-Object FullName,Length,LastWriteTime
Write-Host "Local paper/main.pdf exists:" (Test-Path -LiteralPath $LocalPdf)
