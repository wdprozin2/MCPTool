# Architecture

**Analysis Date:** 2026-05-26

## Pattern Overview

**Overall:** CLI Command Utility with Hybrid Python-Node.js Execution Model and local Flask API Server.

**Key Characteristics:**
- **Hybrid Scripting Bridge:** Core CLI and general logic are written in Python, while complex Minecraft protocol actions (such as client bot creation, authentication, proxy spoofing, and brute force) are delegated to Node.js scripts using `subprocess` calls.
- **Multiprocessing REST API:** Launches an optional Flask web server in a background process to support server data queries locally.
- **Localization System:** Translates console banners and outputs dynamically using language-specific JSON files.
- **Console-based Interface:** Command execution loops interactively through a text-based menu.

## Layers

**UI & Input Layer (`src/menu/` & `src/decoration/`):**
- Purpose: Display interactive menus, banners, and read user commands.
- Contains: `src/menu/command_input.py` (CLI command parser loop) and formatting tools under `src/decoration/`.
- Depends on: Command Layer, Utilities Layer.
- Used by: CLI Entry Point (`main.py`).

**Command Handler Layer (`src/commands/`):**
- Purpose: Execute specific operational commands, parsing parameters, and routing tasks to Python helpers or Node.js sub-processes.
- Contains: Single-purpose modules for each command (e.g., `src/commands/connect.py`, `src/commands/scan.py`, `src/commands/rconbrute.py`).
- Depends on: Core Logic Layer, Utilities Layer, Node.js Scripts.
- Used by: UI & Input Layer.

**Node.js Scripting Bridge Layer (`src/scripts/`):**
- Purpose: Interact directly with Minecraft server instances using the JavaScript-based `mineflayer` framework.
- Contains: Node.js scripts executed as standalone processes (e.g., `src/scripts/connect.js`, `src/scripts/login.js`, `src/scripts/kick.js`).
- Depends on: Node modules (`mineflayer`, `socks`, etc.).
- Used by: Command Handler Layer via subprocess.

**Core Logic Layer (`src/minecraft/`, `src/proxy/`, `src/scan/`, `src/api/`):**
- Purpose: Perform business logic, including scanning, server status retrieval, proxy downloads, and REST APIs.
- Contains: `src/minecraft/get_minecraft_server_data.py` (querying servers) and `src/api/api.py` (Flask server).
- Depends on: External libraries, Managers.
- Used by: Command Handler Layer.

**Infrastructure & Managers Layer (`src/managers/` & `src/utilities/`):**
- Purpose: Common utility routines, OS checks, translation handling, and configuration I/O.
- Contains: `src/managers/json_manager.py` (config files), `src/utilities/get_utilities.py` (i18n), `src/utilities/check_utilities.py` (OS/network checks).
- Depends on: Built-in libraries only.
- Used by: All layers.

## Data Flow

**Interactive Command Execution (e.g., `connect` command):**

1. User enters command in terminal: `connect play.example.com wrrulos 1.20`
2. `CommandInput.command_input` (`src/menu/command_input.py`) parses the input arguments.
3. The connector command handler (`src/commands/connect.py` → `connect_command`) is invoked.
4. Python resolves the server details using `GetMinecraftServerData.get_data` (`src/minecraft/get_minecraft_server_data.py`).
5. Python starts a Node.js process: `node ./src/scripts/connect.js <ip> <port> <username> <version>` using `subprocess.run()`.
6. Node.js executes the script using `mineflayer` to log into the Minecraft server.
7. Node.js prints Minecraft server messages directly to stdout, which are streamed to the user's terminal.
8. When the Node.js process exits, control returns to Python's interactive prompt.

**State Management:**
- State is stateless across commands except for local configuration files (`config/config.json`) and output directories (`logs/`, `files/`).
- The API process (`src/api/api.py`) runs as a background process daemon with its own independent memory.

## Key Abstractions

**Command Handlers:**
- Purpose: Wrap command logic and parameters.
- Examples: `src/commands/connect.connect_command`, `src/commands/scan.scan_command`.
- Pattern: Standalone functional modules containing a main entry function.

**JSON Configuration Manager:**
- Purpose: Direct access to local configuration files.
- Examples: `src/managers/json_manager.JsonManager`.
- Pattern: Static class/utility wrapping JSON reading, path lookup, and writing.

**Localizer:**
- Purpose: Translate key identifiers into the user's configured language.
- Examples: `src/utilities/get_utilities.GetUtilities.get_translated_text`.
- Pattern: Dict lookup inside files under `config/lang/`.

## Entry Points

**Python Main Entry:**
- Location: `main.py`
- Triggers: Command line execution (`python main.py`).
- Responsibilities: Set Windows console title, display startup banners, and call `Startup.run()`.

**Flask API Server Entry:**
- Location: `src/api/api.py` → `run_flask_app`
- Triggers: Background multiprocessing spawn when `api` config is set to `localhost`.
- Responsibilities: Listen on a local port and serve Minecraft server details over HTTP.

## Error Handling

**Strategy:** Bubbled exceptions are caught locally within each command handler or the main input loop to prevent application crashes. KeyboardInterrupt (Ctrl+C) is handled in loops to abort active actions gracefully.

**Patterns:**
- Try/Except blocks wrapping subprocess calls.
- Checking output of system commands (like `nmap` or `java`) and alerting the user if they are missing or return errors.

## Cross-Cutting Concerns

**Localization (i18n):**
- System loads messages from `config/lang/[lang].json` dynamically based on configuration.

**Console Decoration:**
- Colorization of console texts and banners via `src/decoration/paint.py` using `colorama` ANSI escape characters.

---

*Architecture analysis: 2026-05-26*
*Update when major patterns change*
