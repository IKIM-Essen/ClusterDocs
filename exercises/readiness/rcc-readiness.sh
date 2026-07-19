#!/usr/bin/env bash
set -euo pipefail

LIVE=0
[[ "${1:-}" == "--live" ]] && LIVE=1
ALIAS="${RCC_SSH_ALIAS:-rcc-login}"
KEY="${RCC_SSH_KEY:-$HOME/.ssh/id_ed25519_rcc}"
FAIL=0

pass(){ printf 'PASS  %s\n' "$1"; }
warn(){ printf 'WARN  %s\n' "$1"; }
fail(){ printf 'FAIL  %s\n' "$1"; FAIL=1; }

if command -v ssh >/dev/null 2>&1; then pass "OpenSSH client installed: $(ssh -V 2>&1 | head -1)"; else fail "OpenSSH client is not installed"; fi

if [[ -f "$KEY" && -f "$KEY.pub" ]]; then
  pass "RCC private and public key files found"
  if command -v stat >/dev/null 2>&1; then
    mode=$(stat -c '%a' "$KEY" 2>/dev/null || stat -f '%Lp' "$KEY" 2>/dev/null || true)
    [[ "$mode" == "600" || "$mode" == "400" ]] && pass "Private-key permissions are restrictive" || warn "Review private-key permissions; expected 600 or 400"
  fi
  if fp=$(ssh-keygen -lf "$KEY.pub" 2>/dev/null); then pass "Public key is parseable: ${fp%% *} ${fp#* }"; else fail "Public key is not parseable"; fi
else
  fail "Expected RCC key pair not found at $KEY and $KEY.pub"
fi

CONFIG="${RCC_SSH_CONFIG:-$HOME/.ssh/config}"
if [[ -f "$CONFIG" ]] && awk -v h="$ALIAS" 'BEGIN{IGNORECASE=1} /^[[:space:]]*Host[[:space:]]+/ {for(i=2;i<=NF;i++) if($i==h) found=1} END{exit !found}' "$CONFIG"; then
  pass "Explicit SSH Host block found for '$ALIAS'"
else
  fail "No explicit SSH Host block found for '$ALIAS' in $CONFIG"
fi
if command -v ssh >/dev/null 2>&1 && effective=$(ssh -G "$ALIAS" 2>/dev/null); then
  pass "SSH configuration resolves alias '$ALIAS'"
  known_name=$(awk '$1=="hostkeyalias"{print $2; exit} $1=="hostname"{host=$2} END{if(!seen && host) print host}' <<<"$effective" | head -1)
  [[ -n "$known_name" ]] || known_name="$ALIAS"
  if ssh-keygen -F "$known_name" >/dev/null 2>&1; then pass "A pinned host key exists for the configured target"; else warn "No pinned host key was found; verify the published fingerprint before the live test"; fi
else
  fail "SSH configuration does not resolve alias '$ALIAS'"
fi

if command -v code >/dev/null 2>&1; then
  pass "Visual Studio Code installed"
  if code --list-extensions 2>/dev/null | grep -Fxqi 'ms-vscode-remote.remote-ssh'; then
    pass "VS Code Remote - SSH extension installed"
  else
    warn "VS Code Remote - SSH extension not detected"
  fi
else
  warn "Visual Studio Code command 'code' not detected"
fi

if (( LIVE )); then
  if (( FAIL )); then
    fail "Live test skipped because local prerequisites failed"
  else
    printf 'INFO  Making one strict, non-interactive SSH attempt to %s\n' "$ALIAS"
    if ssh \
      -o BatchMode=yes \
      -o PasswordAuthentication=no \
      -o KbdInteractiveAuthentication=no \
      -o NumberOfPasswordPrompts=0 \
      -o ConnectionAttempts=1 \
      -o ConnectTimeout=10 \
      -o StrictHostKeyChecking=yes \
      "$ALIAS" 'printf "RCC_SSH_GATE_OK\\n"' 2>/dev/null | grep -Fxq RCC_SSH_GATE_OK; then
      pass "Bounded SSH credential and connectivity test succeeded"
    else
      fail "SSH test failed; do not create a retry loop"
    fi
  fi
else
  printf 'INFO  No network connection was attempted. Add --live after verifying the published host fingerprint.\n'
fi

exit "$FAIL"
