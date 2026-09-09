@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_daily_parsers_windows.ps1"
exit /b %ERRORLEVEL%
