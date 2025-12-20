#requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
function Clear-Port {
  param (
    [Parameter(Mandatory)]
    [int]$Port
  )

  Write-Host "Checking if port $Port is in use..."

  try {
    $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
  } catch {
    Write-Warning "Get-NetTCPConnection failed. Cannot auto-clear port."
    return
  }

  if (-not $connections) {
    Write-Host "Port $Port is free."
    return
  }

  $owningProcessIds = $connections |
    Select-Object -ExpandProperty OwningProcess -Unique

  foreach ($processId in $owningProcessIds) {
    try {
      $proc = Get-Process -Id $processId -ErrorAction Stop
      Write-Warning "Stopping process $($proc.ProcessName) (PID $processId) using port $Port"
      Stop-Process -Id $processId -Force -ErrorAction Stop
    } catch {
      Write-Warning "Failed to stop process with PID $processId"
    }
  }

  Start-Sleep -Milliseconds 500

  # Verify
  $stillUsed = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
  if ($stillUsed) {
    throw "Port $Port is still in use after cleanup."
  }

  Write-Host "Port $Port successfully cleared."
}


# =========================
# CONFIGURATION
# =========================
$Port        = 8000
$BindHost    = '0.0.0.0'
$HealthPath  = '/health'
$OllamaUrl   = 'http://127.0.0.1:11434'
$DevReload  = $false   # set to $true ONLY when running backend in foreground

# =========================
# PATHS
# =========================
$RepoRoot     = Split-Path -Parent $PSScriptRoot
$ServerDir    = Join-Path $RepoRoot 'server'
$ExtensionDir = Join-Path $RepoRoot 'extension'
$VenvPython   = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $VenvPython)) { $VenvPython = 'python' }

$HostUrl = "http://localhost:${Port}"

Write-Host "== LocalPilot Dev Runner ==" -ForegroundColor Cyan
Write-Host "Repo:     $RepoRoot"
Write-Host "Backend:  $HostUrl"
Write-Host "Ollama:   $OllamaUrl"
Write-Host ""

# =========================
# 1) BACKEND DEPENDENCIES
# =========================
$Requirements = Join-Path $ServerDir 'requirements.txt'
if (Test-Path $Requirements) {
  Write-Host "Installing backend requirements..."
  & $VenvPython -m pip install -r $Requirements | Out-Host
}

# =========================
# 2) PORT CHECK
# =========================
Write-Host "Checking port $Port availability..."
try {
  Clear-Port -Port $Port
} catch {
  Write-Error $_
  exit 1
}

# =========================
# 3) START BACKEND
# =========================
Write-Host "Starting backend..."

$BackendArgs = @(
  '-m', 'uvicorn',
  'server.main:app',
  '--host', $BindHost,
  '--port', $Port,
  '--log-level', 'debug'
)

if ($DevReload) {
  $BackendArgs += '--reload'
}

$BackendProcess = Start-Process `
  -FilePath $VenvPython `
  -ArgumentList $BackendArgs `
  -WorkingDirectory $RepoRoot `
  -NoNewWindow `
  -PassThru

# =========================
# 4) HEALTH CHECK
# =========================
Write-Host "Waiting for backend to accept connections..."

$Deadline = (Get-Date).AddSeconds(30)
$Healthy = $false

while ((Get-Date) -lt $Deadline) {
  try {
    $client = New-Object System.Net.Sockets.TcpClient
    $client.Connect("localhost", $Port)
    $client.Close()
    $Healthy = $true
    break
  } catch {
    Start-Sleep -Milliseconds 500
  }

  if ($BackendProcess.HasExited) {
    Write-Error "Backend exited during startup."
    exit 1
  }
}

if (-not $Healthy) {
  Write-Error "Backend did not open port $Port within timeout."
  Stop-Process -Id $BackendProcess.Id -Force -ErrorAction SilentlyContinue
  exit 1
}

Write-Host "Backend is accepting connections." -ForegroundColor Green

# =========================
# 5) BUILD EXTENSION
# =========================
Write-Host "Preparing extension..."
Set-Location $ExtensionDir

if (-not (Test-Path 'node_modules')) {
  npm install
}

npm run build
if ($LASTEXITCODE -ne 0) {
  Write-Error "Extension build failed."
  Stop-Process -Id $BackendProcess.Id -Force
  exit 1
}

# =========================
# 6) LAUNCH VS CODE
# =========================
$codeCmd = Get-Command code -ErrorAction SilentlyContinue
if (-not $codeCmd) {
  Write-Warning "VS Code CLI 'code' not found."
  Write-Host "Run manually:"
  Write-Host "  code --extensionDevelopmentPath `"$ExtensionDir`""
} else {
  Write-Host "Launching VS Code Extension Development Host..."
  Start-Process "code" "--disable-extensions --extensionDevelopmentPath `"$ExtensionDir`""
  # & code --disable-extensions --extensionDevelopmentPath $ExtensionDir
}

Write-Host ""
Write-Host "== Backend running. Press Ctrl+C to stop ==" -ForegroundColor Cyan

# =========================
# 7) SHUTDOWN HANDLING
# =========================
try {
  while ($true) {
    Start-Sleep -Seconds 1
  }
}
finally {
  Write-Host "Stopping backend..."
  try {
    Stop-Process -Id $BackendProcess.Id -Force
  } catch {}
}



