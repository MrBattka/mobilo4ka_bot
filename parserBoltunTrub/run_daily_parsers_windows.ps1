$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

function Write-Log($Message) {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$stamp] $Message"
}

function Wait-Network {
    for ($attempt = 1; $attempt -le 60; $attempt++) {
        try {
            [System.Net.Dns]::GetHostAddresses("trubkoved.ru") | Out-Null
            Write-Log "Network is ready"
            return
        } catch {
            Write-Log "Network is not ready yet, waiting 30s ($attempt/60)"
            Start-Sleep -Seconds 30
        }
    }
    throw "Network did not become ready in time"
}

function Invoke-WithRetry($Label, [scriptblock]$Command) {
    for ($attempt = 1; $attempt -le 6; $attempt++) {
        Write-Log "$Label: attempt $attempt/6"
        & $Command
        if ($LASTEXITCODE -eq 0) {
            Write-Log "$Label: ok"
            return
        }
        if ($attempt -lt 6) {
            Write-Log "$Label: failed, retrying in 300s"
            Start-Sleep -Seconds 300
        }
    }
    throw "$Label failed after all retries"
}

function Invoke-PythonScript($ScriptName) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 $ScriptName
    } else {
        python $ScriptName
    }
}

Write-Log "Daily parser started"
Wait-Network

$env:TRUBKOVED_SKIP_DESKTOP = "1"
Invoke-WithRetry "Trubkoved" { Invoke-PythonScript "scrape_trubkoved.py" }
Remove-Item Env:\TRUBKOVED_SKIP_DESKTOP -ErrorAction SilentlyContinue

Invoke-WithRetry "Store77" { node scrape_store77.mjs }
Invoke-WithRetry "Boltyn" { node scrape_boltyn.mjs }
Invoke-WithRetry "Combine" { Invoke-PythonScript "combine_product_outputs.py" }

Write-Log "Daily parser finished"
