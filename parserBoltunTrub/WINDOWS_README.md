# Парсер на Windows

## Что поставить на компьютер

1. Python 3: https://www.python.org/downloads/windows/
   При установке обязательно включить галочку `Add python.exe to PATH`.

2. Node.js LTS: https://nodejs.org/

3. В папке парсера открыть PowerShell и выполнить:

```powershell
npm install
npx playwright install chromium
```

## Как запустить вручную

Открыть файл:

```text
run_daily_parsers_windows.bat
```

Или из PowerShell:

```powershell
cd "C:\путь\к\папке\парсера"
.\run_daily_parsers_windows.bat
```

Итоговый файл появится:

```text
outputs\products_latest.xlsx
```

Также скрипт попробует скопировать файл на рабочий стол:

```text
Desktop\Парсер Трубковед Стор77.xlsx
```

## Как поставить ежедневный запуск

Открыть PowerShell в папке парсера и выполнить:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_windows_schedule.ps1
```

Будет создана задача Windows:

```text
Парсер Трубковед Стор77
```

Она запускается каждый день в `06:10`, а также при входе пользователя в Windows.

## Как запустить задачу сразу для проверки

```powershell
Start-ScheduledTask -TaskName "Парсер Трубковед Стор77"
```

Лог запуска:

```text
outputs\windows_schedule.log
```
