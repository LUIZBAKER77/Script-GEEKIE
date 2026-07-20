@echo off
setlocal EnableExtensions
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

echo.
echo === Geekie ===
echo O que voce quer fazer?
echo   1 - Corrigir turma / criar contas
echo   2 - Auditar alunos
echo   3 - Corrigir pendentes da auditoria
echo.
set /p "OPCAO=Opcao: "
if "%OPCAO%"=="" set "OPCAO=1"

if "%OPCAO%"=="1" (
  taskkill /F /T /IM chromedriver.exe >nul 2>&1
  py menu_geekie.py run
  goto fim
)

if "%OPCAO%"=="2" (
  py menu_geekie.py audit
  goto fim
)

if "%OPCAO%"=="3" (
  taskkill /F /T /IM chromedriver.exe >nul 2>&1
  py menu_geekie.py correct
  goto fim
)

echo Opcao invalida.

:fim
pause
