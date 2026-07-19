param([switch]$Live)
$ErrorActionPreference = "Stop"
$Alias = if ($env:RCC_SSH_ALIAS) { $env:RCC_SSH_ALIAS } else { "rcc-login" }
$Key = if ($env:RCC_SSH_KEY) { $env:RCC_SSH_KEY } else { Join-Path $HOME ".ssh\id_ed25519_rcc" }
$Failed = $false
function Pass($m){ Write-Host "PASS  $m" }
function Warn($m){ Write-Host "WARN  $m" }
function Fail($m){ Write-Host "FAIL  $m"; $script:Failed = $true }

if (Get-Command ssh -ErrorAction SilentlyContinue) { Pass "OpenSSH client installed" } else { Fail "OpenSSH client is not installed" }
if ((Test-Path $Key) -and (Test-Path "$Key.pub")) {
  Pass "RCC private and public key files found"
  $fp = & ssh-keygen -lf "$Key.pub" 2>$null
  if ($LASTEXITCODE -eq 0) { Pass "Public key is parseable: $fp" } else { Fail "Public key is not parseable" }
} else { Fail "Expected RCC key pair not found at $Key" }

$Config = if ($env:RCC_SSH_CONFIG) { $env:RCC_SSH_CONFIG } else { Join-Path $HOME ".ssh\config" }
if (Test-Path $Config) {
  $hostLine = Select-String -Path $Config -Pattern ("^\s*Host\s+.*(?:^|\s)" + [regex]::Escape($Alias) + "(?:\s|$)") -CaseSensitive:$false
  if ($hostLine) { Pass "Explicit SSH Host block found for '$Alias'" } else { Fail "No explicit SSH Host block found for '$Alias' in $Config" }
} else { Fail "SSH configuration file not found at $Config" }
if (Get-Command ssh -ErrorAction SilentlyContinue) {
  & ssh -G $Alias *> $null
  if ($LASTEXITCODE -eq 0) { Pass "SSH configuration resolves alias '$Alias'" } else { Fail "SSH configuration does not resolve alias '$Alias'" }
}
if (Get-Command code -ErrorAction SilentlyContinue) {
  Pass "Visual Studio Code installed"
  $ext = & code --list-extensions 2>$null
  if ($ext -match '^ms-vscode-remote\.remote-ssh$') { Pass "VS Code Remote - SSH extension installed" } else { Warn "VS Code Remote - SSH extension not detected" }
} else { Warn "Visual Studio Code command 'code' not detected" }

if ($Live) {
  if ($Failed) { Fail "Live test skipped because local prerequisites failed" }
  else {
    Write-Host "INFO  Making one strict, non-interactive SSH attempt to $Alias"
    $result = & ssh -o BatchMode=yes -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no -o NumberOfPasswordPrompts=0 -o ConnectionAttempts=1 -o ConnectTimeout=10 -o StrictHostKeyChecking=yes $Alias 'printf "RCC_SSH_GATE_OK\n"' 2>$null
    if ($LASTEXITCODE -eq 0 -and $result -contains "RCC_SSH_GATE_OK") { Pass "Bounded SSH credential and connectivity test succeeded" } else { Fail "SSH test failed; do not create a retry loop" }
  }
} else { Write-Host "INFO  No network connection was attempted. Add -Live after verifying the published host fingerprint." }
if ($Failed) { exit 1 } else { exit 0 }
