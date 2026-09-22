@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  if errorlevel 1 goto :failed
)
".venv\Scripts\python.exe" -c "import fastapi, uvicorn" >nul 2>&1
if errorlevel 1 (
  ".venv\Scripts\python.exe" -m pip install -r requirements-local.txt
  if errorlevel 1 goto :failed
)
set "APP_PORT=8080"
if not "%~1"=="" set "APP_PORT=%~1"
echo Open http://127.0.0.1:%APP_PORT% in your browser.
echo Keep this window open. Press Ctrl+C to stop the server.
".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port %APP_PORT%
if errorlevel 1 goto :failed
exit /b 0
:failed
echo Startup failed. See the error above. If the port is in use, try start-local.cmd 8081
pause
exit /b 1
