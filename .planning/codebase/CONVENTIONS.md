# Coding Conventions

**Analysis Date:** 2026-05-26

## Naming Patterns

**Files:**
- snake_case.py for Python source files (e.g., `check_utilities.py`, `rich_presence.py`).
- camelCase.js for Node.js javascript files (e.g., `pinlogin.js`, `connect.js`).
- UPPERCASE files for generic project assets (`LICENSE`, `README.md`).

**Functions:**
- snake_case for Python functions (e.g., `connect_command`, `print_banner`).
- camelCase for JavaScript functions.

**Variables:**
- snake_case for Python variables (e.g., `api_process`, `server_data`).
- camelCase for JavaScript variables.

**Classes:**
- PascalCase for Python classes (e.g., `Startup`, `JsonManager`, `CheckUtilities`, `GetMinecraftServerData`).
- Note: Many modules use static methods on classes to encapsulate helper scripts rather than instantiating objects.

## Code Style

**Formatting:**
- No automated formatter (like Prettier or Black) config files exist in the codebase.
- Indentation: 4 spaces for Python; variable spaces (usually 2 or 4) for JavaScript.
- Strings: Single and double quotes are used interchangeably.

**Linting:**
- No lint rules are configured (no `.eslintrc` or `pyproject.toml` linter rules).

## Import Organization

**Python Imports:**
- Standard library modules (like `subprocess`, `sys`, `os`, `time`) are imported first.
- Empty line separates standard imports from project-local imports.
- Relative imports from the root namespace are used (e.g., `from src.decoration.paint import paint`).

**JavaScript Imports:**
- Standard Node.js `require` syntax at the top of scripts.
- Example: `const mineflayer = require('mineflayer')`.

## Error Handling

**Patterns:**
- **KeyboardInterrupt Handling:** Loop runners and command runners handle KeyboardInterrupt to print a clean termination message instead of showing stack traces to users.
- **Subprocess Error Handling:** Commands wrap subprocess runs in try-catch to print descriptive error messages if Java, Node, or Nmap is not present or aborts.
- **Node.js Bot Error Handlers:** JavaScript scripts register handlers for mineflayer events (e.g., `bot.on('error', ...)`, `bot.on('kicked', ...)`, `bot.on('end', ...)`) to log connection problems without throwing unhandled exceptions.

## Logging

**Console output decoration:**
- Console outputs are colored using custom utilities: `paint` function in Python (via `colorama`) and `minecraft-colors` package in Node.js.
- Logging of player logins and query results is written to plain text files inside the `logs/` directory using file streams.

## Comments

- Standard comments detailing why steps are performed, particularly for platform compatibility (like Android Termux fixes).
- Basic docstrings are provided for major Python classes and functions, outlining args and actions.

---

*Convention analysis: 2026-05-26*
*Update when patterns change*
