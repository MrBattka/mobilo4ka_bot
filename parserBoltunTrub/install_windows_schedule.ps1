$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $ProjectDir "run_daily_parsers_windows.ps1"
$LogDir = Join-Path $ProjectDir "outputs"
$TaskName = "Парсер Трубковед Стор77"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$argument = "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" *> `"$LogDir\windows_schedule.log`""
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $argument -WorkingDirectory $ProjectDir
$dailyTrigger = New-ScheduledTaskTrigger -Daily -At 6:10
$logonTrigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 3)

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($dailyTrigger, $logonTrigger) -Settings $settings -Description "Ежедневный сбор товаров Trubkoved, Store77, Boltyn" -Force | Out-Null

Write-Host "Installed scheduled task: $TaskName"
Write-Host "Schedule: every day at 06:10 and at Windows logon"
Write-Host "Run now:"
Write-Host "  Start-ScheduledTask -TaskName `"$TaskName`""
Write-Host "Log:"
Write-Host "  $LogDir\windows_schedule.log"
