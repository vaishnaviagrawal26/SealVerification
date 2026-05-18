# ==========================================
# SEAL VERIFICATION API - STARTUP SCRIPT (PowerShell)
# ==========================================

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "SEAL VERIFICATION API - STARTUP" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create output directory if it doesn't exist
if (-not (Test-Path "output")) {
    New-Item -ItemType Directory -Path "output" | Out-Null
}
if (-not (Test-Path "input")) {
    New-Item -ItemType Directory -Path "input" | Out-Null
}

# Start API
Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Starting API on http://localhost:8000" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Swagger UI: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "ReDoc UI: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""

python api.py
