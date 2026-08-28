$ErrorActionPreference = "Stop"

if (-not $env:NAVER_CLIENT_ID -or -not $env:NAVER_CLIENT_SECRET) {
    Write-Error "Set NAVER_CLIENT_ID and NAVER_CLIENT_SECRET before running."
}
if (-not $env:MFDS_API_KEY) {
    Write-Error "Set MFDS_API_KEY before running."
}

$env:PYTHONPATH = Join-Path $PSScriptRoot "src"
python -m moongcheap_ai.pipeline --root $PSScriptRoot
