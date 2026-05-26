# Codebase Structure

**Analysis Date:** 2026-05-26

## Directory Layout

```
MCPTool/
├── config/                  # Configuration files
│   └── lang/                # Language localization JSONs (en, es, pt, etc.)
├── docs/                    # Command & API guides
├── files/                   # Saved output files (e.g., players list, host IPs)
├── logs/                    # Process log files
├── mcrcon_mcpt/             # Packaged custom python RCON library
├── mcstatus_mcpt/           # Packaged custom python mcstatus library
├── node_modules/            # Node.js dependency directory
├── src/                     # Core source code
│   ├── api/                 # Flask API endpoints
│   ├── commands/            # Command execution controllers
│   ├── decoration/          # Terminal style and banners
│   ├── managers/            # File configuration managers
│   ├── menu/                # User input CLI reader
│   ├── minecraft/           # Server details retrieval helper
│   ├── presence/            # Discord RPC integrations
│   ├── proxy/               # Waterfall/Velocity proxy controls
│   ├── scan/                # Port scanning and checking scripts
│   ├── scripts/             # Node.js scripts for Minecraft interactions
│   ├── termux/              # Termux Android-specific patches
│   ├── updater/             # Project updates checker
│   └── utilities/           # Shared helper functions
├── main.py                  # Main entry point file
├── requirements.txt         # Python dependencies manifest
├── setup.py                 # Setup install script
├── package.json             # Node.js dependency manifest
├── package-lock.json        # Node.js lockfile
├── masscan.exe              # Executable binary of Masscan for Windows
├── ngrok.exe                # Executable binary of Ngrok for Windows
└── LICENSE                  # MIT License
```

## Directory Purposes

**config/**
- Purpose: Application options and language strings.
- Contains: `config.json` (general options), `bruteforce_config.json` (attack settings), `sendcmd_config.json`.
- Subdirectories: `lang/` containing JSON translations.

**files/**
- Purpose: Default directory where commands output extracted text files (e.g. player lists, resolved IPs).
- Contains: Text files (`*.txt`).

**logs/**
- Purpose: Application system logs.
- Contains: Log files.

**mcrcon_mcpt/ & mcstatus_mcpt/**
- Purpose: Custom local libraries derived from `mcrcon` and `mcstatus` to query servers and send console commands.
- Contains: Python modules (`*.py`).

**src/commands/**
- Purpose: Defines individual CLI command controllers.
- Contains: 26 python scripts, each mapping to a command name (e.g. `connect.py`, `rconbrute.py`, `kick.py`).

**src/scripts/**
- Purpose: Javascript bridge executing Minecraft protocol behaviors with Node.js.
- Contains: Node.js scripts (`*.js`) invoked as sub-processes by Python commands.

**src/api/**
- Purpose: Local API server supporting server pinging and status queries.
- Contains: `api.py` (Flask server), `minecraft_server_data.py` (query endpoints).

**src/minecraft/**
- Purpose: Handles connections to query status data from servers.
- Contains: `get_minecraft_server_data.py` (processes pings via API or local).

## Key File Locations

**Entry Points:**
- `main.py` - Application command line UI starter.
- `src/startup.py` - Pre-flight checks and configuration initializer.
- `setup.py` - Installer script for third-party tools and modules.

**Configuration:**
- `config/config.json` - System, scanner, and proxy configs.
- `package.json` - Node dependencies.
- `requirements.txt` - Python requirements.

**Core Logic:**
- `src/menu/command_input.py` - Terminal command reader.
- `src/scripts/connect.js` - Connection handler via `mineflayer`.
- `src/api/api.py` - Flask local host web listener.

## Naming Conventions

**Files:**
- snake_case.py - All Python source files (e.g., `command_input.py`, `print_banner.py`).
- camelCase.js - JavaScript scripts (e.g., `pinlogin.js`, `sendcmd.js`).
- kebab-case.json - Localization and package configurations.

**Directories:**
- snake_case or standard words (e.g., `mcrcon_mcpt`, `commands`, `decoration`).

## Where to Add New Code

**Adding a New CLI Command:**
1. Create a command script in `src/commands/[command_name].py`.
2. Register the command and route input parameters inside `src/menu/command_input.py`.
3. If it requires Minecraft client protocol logic, create a Node script under `src/scripts/[command_name].js` and execute it from the Python script using `subprocess.run()`.

**Adding a Translation:**
- Add translated keys inside respective JSON files under `config/lang/` (e.g., `pt.json`).

---

*Structure analysis: 2026-05-26*
*Update when directory structure changes*
