# Testing Patterns

**Analysis Date:** 2026-05-26

## Test Framework

**Runner:**
- No automated test runners (like `pytest`, `unittest`, `Jest`, or `Mocha`) are configured or installed in this codebase.

**Assertion Library:**
- None.

**Run Commands:**
- There are no test scripts configured in `package.json` or `setup.py`.

## Test File Organization

**Location:**
- No test files or directories exist in the codebase.
- There are no `.test.ts`, `.test.js`, or `test_*.py` files.

## Manual Verification

As the codebase does not have automated unit or integration tests, verification of features must be conducted manually using the following procedures:

**1. Main CLI Routine:**
- Launch the main console script: `python main.py`.
- Select various numeric/string commands in the main menu to verify that the UI updates correctly and outputs are formatted.

**2. Local API Server verification:**
- Change the `api` configuration value inside `config/config.json` to `"localhost"`.
- Run `python main.py` and verify that Flask initializes on port `55455`.
- Verify using a web browser or curl by querying `http://localhost:55455/`.

**3. Node.js Script execution:**
- Execute scripts manually from the CLI to confirm they run without syntax errors. For example:
  `node src/scripts/connect.js <valid_ip> <port> <username> <version> 2`
- Verify that the connection initializes, prints colors, and terminates upon server kick or disconnect.

**4. Scanning tools verification:**
- Verify that `nmap`, `masscan`, and `quboscannerCommand` function correctly by triggering a scan option inside the menu.
- Ensure correct configuration variables are parsed from `config/config.json`.

## Recommended Future Testing Patterns

If automated testing is added to the codebase in the future, the following frameworks and structures are recommended:

**For Python Logic:**
- Framework: `pytest`
- Location: `tests/` directory at the project root with files prefixed with `test_*.py`.
- Mocking: `unittest.mock` to mock `subprocess.run` calls, `requests.get` API responses, and file system I/O.

**For Node.js Logic:**
- Framework: `Jest`
- Location: `tests/scripts/` directory matching Node scripts names.
- Mocking: Mocking of `mineflayer` connection events to test connection state machines in `connect.js` and `login.js`.

---

*Testing analysis: 2026-05-26*
*Update when test patterns change*
