# Technology Stack

**Analysis Date:** 2026-05-26

## Languages

**Primary:**
- Python 3.x - Core application logic, command CLI interface, API servers, and system orchestration.

**Secondary:**
- JavaScript (ES6) - Node.js integration scripts located in `src/scripts/` for Minecraft server connection, bot commands execution, and ping queries.

## Runtime

**Environment:**
- Python 3.x interpreter.
- Node.js 18.x/20.x runtime environment.
- Java Runtime Environment (JRE) (optional, version 17+ or 19+) for waterfall and velocity proxy utilities.
- Nmap command line utility (optional) for port scanning.

**Package Managers:**
- pip - Python package manager (uses `requirements.txt`).
- npm - Node.js package manager (uses `package.json` and `package-lock.json`).

## Frameworks

**Core:**
- Flask 3.x (implied) - Used in `src/api/api.py` for the local Web API.
- Waitress - Production WSGI server for serving the Flask API on Windows.

**Testing:**
- None - No automated test suites configured in the codebase.

**Build/Dev:**
- None - Vanilla scripting setup with direct execution of Python and Node.js.

## Key Dependencies

**Critical (Python):**
- requests - Fetching data from web APIs, download utilities, and setup download routines.
- flask & waitress - Local REST API implementation.
- shodan - Interfacing with Shodan Search Engine to find Minecraft servers.
- colorama - CLI colored output console decoration.
- pypresence - Discord Rich Presence integration.
- aiohttp & asyncio_dgram - Asynchronous networking tools for scanning and querying.
- dnspython - Querying DNS records and domain mapping.

**Critical (Node.js):**
- mineflayer - Minecraft client bot creation framework for joining servers, logging, and sending commands.
- minecraft-colors - Parsing and rendering Minecraft text color formatting in console.
- proxy-agent - Node.js proxy agent support (SOCKS, HTTP, HTTPS) for bot traffic routing.
- telebit - Local tunnel generation proxying utility.
- socks - SOCKS proxy client wrapper.

## Configuration

**Environment:**
- No environment variables are strictly required by default.
- Shodan API key and other configurations are saved inside `config/config.json`.

**Build:**
- No build configuration files (e.g., tsconfig, webpack) are present.
- `package.json` for Node.js package resolution.
- `requirements.txt` for Python dependencies.

## Platform Requirements

**Development & Production:**
- Windows (8, 8.1, 10, 11) - Full support.
- Linux - Full support.
- Android Termux - Fully supported with custom configurations (like DNS lookup fixes).

---

*Stack analysis: 2026-05-26*
*Update after major dependency changes*
