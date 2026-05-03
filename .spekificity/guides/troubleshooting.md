# Troubleshooting Guide: Spekificity Platform

## Setup Phase (`spek setup`)

### Error: "Python not found"

**Cause**: Python 3.11+ not installed or not in PATH

**Solutions**:
- **macOS**: `brew install python@3.11`
- **Ubuntu**: `sudo apt update && sudo apt install -y python3.11`
- **Verify**: Run `python3 --version` (should show 3.11 or higher)

---

### Error: "uv not found"

**Cause**: uv package manager not installed

**Solution**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify**: Run `uv --version`

---

### Error: "git not found"

**Cause**: git not installed

**Solutions**:
- **macOS**: `brew install git`
- **Ubuntu**: `sudo apt install -y git`
- **Verify**: Run `git --version`

---

### Error: "Permission denied" on setup script

**Cause**: Setup scripts not executable

**Solution**:
```bash
chmod +x .spekificity/setup-scripts/*.sh .spekificity/bin/spek
```

---

## Initialization Phase (`spek init`)

### Error: "specify not found globally"

**Cause**: speckit/specify not installed globally

**Solution**:
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Then retry: `spek init`

---

### Error: "graphify not found"

**Cause**: graphify not installed

**Solution**:
```bash
uv tool install graphifyy
```

Then retry: `spek init`

---

### Error: "Obsidian vault setup failed"

**Cause**: Obsidian app not installed (or permission issue)

**Solution**:
Obsidian is **optional**. Initialization can proceed without it:
```bash
spek init --skip-obsidian
```

To use Obsidian later:
1. Install Obsidian from https://obsidian.md/
2. Run: `spek init`

---

### Error: "Skills installation failed"

**Cause**: Permission issue or disk space

**Solutions**:
- Ensure `.spekificity/` directory is writable: `ls -la .spekificity/`
- Check disk space: `df -h .`
- Manually create skills dir: `mkdir -p .spekificity/skills/`

---

### Error: "Config file corrupted"

**Cause**: `.spekificity/config.json` is invalid JSON

**Solution**:
```bash
# Backup corrupted config
cp .spekificity/config.json .spekificity/config.json.bak

# Repair config (auto-fill defaults)
.spekificity/setup-scripts/config-handler.sh repair_config

# Or manually create new config:
rm .spekificity/config.json
spek init
```

---

## Runtime Issues

### Error: "spek: command not found"

**Cause**: spek script not in PATH or not executable

**Solutions**:
1. Make it executable: `chmod +x .spekificity/bin/spek`
2. Use full path: `./.spekificity/bin/spek setup`
3. Or add to PATH: `export PATH="$PWD/.spekificity/bin:$PATH"`

---

### Error: "/spek.context-load: command not found"

**Cause**: Spekificity skills not installed or not discoverable

**Solutions**:
1. Verify initialization: `spek status`
2. Check skills exist: `ls .spekificity/skills/`
3. Regenerate skill index: `.spekificity/setup-scripts/skill-discovery.sh`
4. Re-run init: `spek init`

---

### Error: "orchestration_history" not found in config

**Cause**: Config schema mismatch (old version)

**Solution**:
```bash
# Repair config to add missing fields
spek status --json | jq . > /tmp/config-check.json
# If needed, regenerate:
rm .spekificity/config.json
spek init
```

---

## Idempotency & Recovery

### "Partial failure detected. Attempting recovery..."

**Cause**: Previous `spek init` was interrupted

**Solution**:
1. Review the last failed step:
   ```bash
   jq '.orchestration_history[-1]' .spekificity/config.json
   ```
2. Address the failure (e.g., install missing tool)
3. Re-run: `spek init`

The system will resume from where it left off.

---

### "Setup did not complete successfully"

**Cause**: Unknown error during setup

**Solution**:
1. Run with verbose output: `spek setup --verbose`
2. Review error messages carefully
3. Install missing prerequisites manually
4. Retry setup

---

## Multi-Platform Issues

### macOS (Monterey/Ventura/Sonoma)

**Python not in PATH**:
- After `brew install python@3.11`, add to `.zshrc`:
  ```bash
  export PATH="/usr/local/opt/python@3.11/bin:$PATH"
  ```
- Then: `source ~/.zshrc`

**Obsidian permissions**:
- If Obsidian hangs: Preferences → Security & Privacy → Allow Obsidian

---

### Linux (Ubuntu 20.04/22.04)

**uv installation issues**:
- Ensure `curl` installed: `sudo apt install -y curl`
- Run installation with `-k` flag if SSL issues: `curl -LsSfk https://astral.sh/uv/install.sh | sh`

**WSL (Windows Subsystem for Linux)**:
- Use Ubuntu 22.04 LTS or newer
- Ensure line endings are LF (not CRLF): `git config --global core.autocrlf false`

---

## Configuration Issues

### "spek_initialized = false but has history entries"

**Cause**: Partial failure detected

**Solution**:
Review history and address blocking issue:
```bash
jq '.orchestration_history | map(select(.status=="failure"))' .spekificity/config.json
```

Then re-run: `spek init`

---

### "Custom preferences not persisted"

**Cause**: Changes to config made outside standard path

**Solution**:
Use config handler to update preferences:
```bash
# Don't edit config.json manually — use:
.spekificity/setup-scripts/config-handler.sh update_config \
  '.spek_custom_preferences.my_setting' '"my_value"'
```

---

## Namespace/Discovery Issues

### Skills not discoverable by AI agent

**Cause**: Skill index stale or invalid

**Solution**:
```bash
# Regenerate skill index
.spekificity/setup-scripts/skill-discovery.sh generate_skill_index

# Verify index
cat .spekificity/skill-index.md | head -30

# Validate namespace consistency
.spekificity/setup-scripts/validate-namespace.sh
```

---

### Namespace collision between spekificity and speckit

**Cause**: Skill naming violation

**Solution**:
```bash
# Validate and auto-fix namespace issues
.spekificity/setup-scripts/validate-namespace.sh --fix
```

---

## Getting Help

1. **Check this guide first**: Most issues are covered above
2. **Review logs**: `spek init --verbose` for detailed output
3. **Check status**: `spek status --json` for full state
4. **Consult guides**: `.spekificity/guides/troubleshooting.md` (project-specific)
5. **Contact support**: Include output of `spek status --json` and error messages

---

**Still stuck?** Run with `--verbose` and capture full output for debugging.
