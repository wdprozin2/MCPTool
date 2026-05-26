# Codebase Concerns

**Analysis Date:** 2026-05-26

## Tech Debt

**Hybrid process execution bridge (`subprocess` with `shell=True`):**
- Issue: Python commands trigger Node.js helper scripts using shell subprocesses (`subprocess.run(command, shell=True)`).
- Files: `src/commands/connect.py` (lines ~40-46), `src/commands/kick.py`, `src/commands/login.py`, `src/commands/pinlogin.py`, `src/commands/sendcmd.py`.
- Why: Done to easily bridge Python CLI interface and Node.js `mineflayer` libraries.
- Impact: Highly prone to OS command injections if input arguments are not sanitized, and can cause platform pathing issues (especially on Windows with spaces in directories).
- Fix approach: Transition from string commands with `shell=True` to lists of command arguments with `shell=False`, e.g., `subprocess.run(["node", "./src/scripts/connect.js", ip, port, username, version])`.

**Local duplication of dependencies (`mcstatus_mcpt` and `mcrcon_mcpt`):**
- Issue: Custom copies of `mcstatus` and `mcrcon` libraries are checked into the source tree instead of using standard package managers.
- Files: Directories `mcstatus_mcpt/` and `mcrcon_mcpt/`.
- Why: Modified to adapt output formats or fix specific protocol compatibility issues.
- Impact: Hard to keep upstream security patches and version updates. Clutters the source repository.
- Fix approach: Move these libraries into the `requirements.txt` or subclass the upstream packages dynamically rather than copying entire repositories.

## Known Bugs

**Syntax Error in `main.py` (`import tiheme`):**
- Symptoms: App fails to start with `ModuleNotFoundError: No module named 'tiheme'`.
- Trigger: Simply executing `python main.py`.
- Files: `main.py` (line 2).
- Workaround: Manually edit `main.py` to change `import tiheme` to `import time`.
- Root cause: Typo during development or refactoring.

**API default fallback reset logic:**
- Symptoms: Configuration is overwritten to default when invalid api is parsed.
- Trigger: If API value inside `config/config.json` doesn't match `['localhost', 'mcsrvstat.us', 'mcstatus.io']`, it resets the JSON.
- Files: `src/startup.py` (lines ~36-39).
- Root cause: Restrictive check prevents custom APIs from being registered.

## Security Considerations

**Command Injection Vulnerability:**
- Risk: Arguments like `username`, `version`, or `ip` read from user input are concatenated directly into a shell execution string. If a user supplies inputs with shell characters (e.g., `&` or `;`), it could trigger arbitrary command execution on the host machine.
- Files: `src/commands/connect.py`, `src/commands/login.py`, `src/commands/kick.py`.
- Current mitigation: Basic input checking, but insufficient shell escaping is implemented.
- Recommendations: Avoid `shell=True` and sanitize all inputs before passing them to subprocesses.

**Flask API Authentication:**
- Risk: The local API server launched in `src/api/api.py` does not require authentication or token validation, potentially allowing other users on the network to probe local services if the server binds to `0.0.0.0` or if local ports are exposed.
- Current mitigation: Runs on localhost by default.
- Recommendations: Enforce strict localhost binding and add basic bearer token authentication if external access is ever allowed.

## Performance Bottlenecks

**Blocking Command Execution:**
- Problem: The CLI terminal blocks execution and is completely non-responsive while waiting for subprocess connections or port scans to finish.
- Measurement: Handlers block for up to several minutes during slow port scans or brute force attacks.
- Cause: Synchronous `subprocess.run` calls block the main Python event thread.
- Improvement path: Migrate subprocess runs to asynchronous loops (using `asyncio.create_subprocess_exec`) so the UI can process cancellation inputs or remain active.

## Scaling Limits

**RCON Brute Force Limitations:**
- Current capacity: Dependent on server thread limits.
- Limit: High brute force thread counts can easily cause high CPU loads and trigger server-side IP blocks or rate limits.
- Symptoms at limit: Target server stops responding to RCON commands, or local system slows down.
- Scaling path: Introduce progressive delay intervals and automatic proxy rotation configurations.

## Test Coverage Gaps

**Zero Test Coverage:**
- What's not tested: The entire codebase lacks unit, integration, or end-to-end tests.
- Risk: Changes in scripts or dependencies could break command parsing, bot spawning, or scanning unnoticed.
- Priority: High.
- Difficulty to test: Spawning interactive Minecraft clients is difficult to mock; requires a mock Minecraft server fixture.

---

*Concerns audit: 2026-05-26*
*Update as issues are fixed or new ones discovered*
