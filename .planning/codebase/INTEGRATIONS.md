# External Integrations

**Analysis Date:** 2026-05-26

## APIs & External Services

**Shodan Search API:**
- Service: Shodan Search Engine
- SDK/Client: `shodan` Python package
- Auth: API key stored in `config/config.json` under `shodanApiKey`
- Endpoints used: Shodan search APIs to locate Minecraft servers using queries

**Minecraft Server Status APIs:**
- Services: `mcsrvstat.us`, `mcstatus.io`
- Integration method: REST API requests via `requests` Python library
- Auth: Public endpoints, no authentication required
- Usage: Queries info, player lists, and version info for Minecraft servers when local pinging is not selected or fails

**Discord Rich Presence:**
- Service: Discord client local IPC
- SDK/Client: `pypresence` Python library
- Auth: Client application ID hardcoded in `src/presence/rich_presence.py`
- Usage: Displays user status on Discord (e.g., active server connections, tool version, status)

**PaperMC Downloads API:**
- Service: PaperMC downloads server
- Integration method: GET request to retrieve `.jar` files
- Endpoints used: `https://api.papermc.io/v2/projects/waterfall/versions/...` and `https://api.papermc.io/v2/projects/velocity/versions/...` to download proxy software

## Data Storage

**Databases:**
- None - MCPTool does not interact with any external or local relational/NoSQL databases.

**File Storage:**
- Local JSON Configuration: Configurations are persisted locally in `config/config.json`, `config/bruteforce_config.json`, and `config/sendcmd_config.json`.
- Local logs: Server player lists and scan outputs are stored as plain text files under `logs/` and `files/`.

## Authentication & Identity

- None: The tool does not manage user accounts or user sessions.

## Monitoring & Observability

- None: No external tracking or observability tools (like Sentry, Loggly, or Datadog) are integrated.

## CI/CD & Deployment

- None: This is a client-side execution utility meant to run locally on Windows, Linux, or Termux.

## Environment Configuration

- No environment variables are used. The configuration is purely file-based via `config/config.json`.
- API keys: The Shodan API key is stored directly in `config/config.json`.
- Proxy credentials: If proxy is used, connection details are stored in files specified by the configuration (e.g., `./proxy.txt`).

## Webhooks & Callbacks

- None: There are no incoming or outgoing webhooks configured in this application.

---

*Integration audit: 2026-05-26*
*Update when adding/removing external services*
