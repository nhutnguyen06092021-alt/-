@echo off
setlocal
cd /d "%~dp0"

set "ONEFILE_PYTHON=%~dp0backend\.onefile-venv\Scripts\python.exe"
set "ONEFILE_PYTHON_ARGS="
"%ONEFILE_PYTHON%" -c "import click,uvicorn; assert hasattr(click, 'Choice')" >nul 2>nul
if not errorlevel 1 goto run

set "ONEFILE_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
"%ONEFILE_PYTHON%" -c "import sys" >nul 2>nul
if not errorlevel 1 goto run

where py >nul 2>nul
if not errorlevel 1 (
  set "ONEFILE_PYTHON=py"
  set "ONEFILE_PYTHON_ARGS=-3"
  goto run
)

where python >nul 2>nul
if not errorlevel 1 (
  set "ONEFILE_PYTHON=python"
  goto run
)

echo.
echo [ONEFILE] Khong tim thay Python 3.11-3.14.
echo Cai Python tu https://www.python.org/downloads/windows/
echo Trong bo cai, chon "Add python.exe to PATH", sau do chay lai file nay.
echo.
pause
exit /b 1

:run
if /i "%~1"=="--check" (
  "%ONEFILE_PYTHON%" %ONEFILE_PYTHON_ARGS% -c "import sys; print('ONEFILE Python OK:', sys.executable)"
  exit /b %errorlevel%
)

echo [ONEFILE] Dang khoi dong...
"%ONEFILE_PYTHON%" %ONEFILE_PYTHON_ARGS% run_onefile.py
if errorlevel 1 (
  echo.
  echo [ONEFILE] Khoi dong that bai. Xem thong bao phia tren.
  pause
)
