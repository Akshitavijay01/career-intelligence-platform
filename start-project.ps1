Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Career Intelligence Platform Launcher " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Backend Server
Write-Host "[1/2] Launching FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
$backendDir = Join-Path $rootDir "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendDir'; .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

# Start Frontend Server
Write-Host "[2/2] Launching Vite Frontend on http://localhost:5173..." -ForegroundColor Green
$frontendDir = Join-Path $rootDir "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; npm run dev"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Yellow
Write-Host "Application is starting up!" -ForegroundColor Yellow
Write-Host "Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "Demo User: demo@careerai.com / demo123" -ForegroundColor Gray
Write-Host "=========================================" -ForegroundColor Yellow
