# Changelog

All notable changes to this project will be documented in this file.

## [1.5.32] - 2026-06-11
### Added
- **[GUI]** Added a fully visual setup wizard interface based on CustomTkinter.
- **[GUI]** Implemented dynamic service checklist selection and custom credential wizards matching the CLI deployment flow.
- **[GUI]** Added non-blocking background deployment worker threads with real-time log piping/redirection.
- **[Main]** Integrated auto-routing entry execution to launch GUI mode if display server is present, falling back to CLI.

## [1.5.31] - 2026-06-10
### Added
- **[Updater]** Implemented intelligent environment detection to update installed setups via the native `dockersetupinstaller.exe` silently in the background, while maintaining standalone binary-swap upgrades for portable runs.

## [1.5.30] - 2026-06-10
### Fixed
- **[Installer]** Corrected Inno Setup constant definition for user's AppData path from invalid `{userlocalappdata}` to standard `{localappdata}`.

## [1.5.29] - 2026-06-10
### Fixed
- **[CI/CD]** Fixed the missing executable icon on release binaries by passing the `--icon` parameter to the PyInstaller task in GitHub Actions.
- **[Installer]** Enabled automatic remote compilation and release uploading of the Windows `dockersetupinstaller.exe` setup wrapper by leveraging pre-installed Inno Setup on GitHub Actions runners.
- **[Installer]** Renamed output installer binary to `dockersetupinstaller.exe` for streamlined user distribution.

## [1.5.28] - 2026-06-10
### Added
- **[Installer]** Added Inno Setup compiler script configuration for Windows user-writable Local AppData packaging.
- **[Installer]** Created Zenity-based native GTK GUI installer and application launcher desktop configuration for Linux.
- **[CI/CD]** Integrated Windows & Linux automated installer generation steps into the project compilation script.

## [1.5.27] - 2026-06-10
### Fixed
- **[Main]** Fixed syntax errors (`NameError`) in `strategy_servarr.py` where lowercase `true` was evaluated instead of Python's boolean `True`.
- **[Main]** Dynamically resolved Prowlarr port from registry instead of using hardcoded port `9696`.
- **[Main]** Prevented `IndexError` on malformed line parsing in `yaml_parser.py` by adding defensive splitting logic.
- **[Main]** Handled `docker compose pull` CLI parameter differences by adding fallback pulling flags.
- **[Homepage]** Decoupled Homepage dashboard layout settings generation, dynamically pulling stack categories from `services.yml` rather than hardcoded definitions.
- **[Authelia]** Automated Nginx Proxy Manager integration when both `authelia` and `npm plus (+goaccess)` are deployed by writing a reusable `authelia-auth.conf` configuration snippet.
- **[UX]** Built interactive setup wizards for Plex claim token, Tailscale keys, and Seerr connection configurations.
- **[USENET]** Implemented interactive SABnzbd newsgroup server configurations. Added free Newznab Usenet indexers (`NZBFinder`, `Tabula-Rasa`) and prompted for premium indexers (`NZBGeek`, `NinjaCentral`, `AltHub`).

## [1.5.26] - 2026-06-10
### Fixed
- **[Updater]** Unified self-update relaunch execution to use `os.execv` on Windows (using overlay mechanism) instead of `subprocess.Popen` which caused terminal stdin control to return to the shell prompt and freeze keyboard input in the child process.

## [1.5.25] - 2026-06-10
### Fixed
- **[Main]** Resolved `NoneType` value crash during environment variable mapping inside `set_env_var` function.
- **[Homepage]** Filtered dashboard rendering to exclude the `homepage` service itself from listing.
- **[Homepage]** Configured the disk widget usage path to be lowercase (`/c`) to align with container case sensitivity.
- **[CI/CD]** Removed redundant/failing `release-please` Github workflow in favor of tag-triggered asset builder.

## [1.5.24] - 2026-06-10
### Fixed
- **[Main]** Enforced `External` authentication configurations for Sonarr, Radarr, and Lidarr by writing pre-seeded `config.xml` files prior to starting the containers, preventing double authorization prompts.
- **[Main]** Enabled episode renaming rules and default root directory paths `/movies`, `/tv`, and `/music` during servarr strategies connection calls.
- **[Main]** Auto-configured Radarr/Sonarr import lists (Plex watchlist with 3-hour refresh intervals and StevenLu popular list) when a valid `PLEX_TOKEN` is found.
- **[Prowlarr]** Configured public Usenet indexers for Minimal setups and added public Torrent indexers if a BitTorrent client is selected.
- **[Bazarr]** Integrated automated subtitle client auto-configuration linking Bazarr to Radarr and Sonarr via API.
- **[Homepage]** Filtered out all background services without an active Web UI from `services.yaml`.
- **[UX]** Expanded installer prompt detail to encourage Plex Claim tokens and updated post-setup guidelines (Tautulli, SABnzbd, Prowlarr, Seerr).
- **[Docs]** Trimmed the Key Features list in `README.md` to primary strategic highlights.

## [1.5.23] - 2026-06-10
### Fixed
- **[Docs]** Realigned the logo in `README.md` to be inline with the primary header name and scaled it down (height of 38px) for clean presentation.

## [1.5.22] - 2026-06-10
### Fixed
- **[Docs]** Added the untracked logo image file `resources/dockersetup.png` and binary icon `resources/app.ico` to the repository tracking, allowing remote GitHub rendering.

## [1.5.21] - 2026-06-10
### Fixed
- **[Homepage]** Reverted services widget key variables to double curly bracket placeholders (e.g. `{{HOMEPAGE_VAR_X}}`) and restored dynamic environmental mapping generation in `docker-compose.yml` to satisfy Homepage's strict API credential isolation rules.
- **[SABnzbd]** Expanded `host_whitelist` injection to include local subnet IPs and container hostnames (`sabnzbd, localhost, 127.0.0.1, 192.168.90.11`), resolving hostname validation access warnings in Docker networks.

## [1.5.20] - 2026-06-10
### Fixed
- **[Docs]** Replaced HTML logo tags with standard Markdown image tags in `README.md` to ensure correct rendering.
- **[Main]** Updated terminal print outputs in `dockersetup.py` using Rich OSC 8 hyperlinks to make URL shortcuts to Dashboard and Dockge clickable.

## [1.5.19] - 2026-06-10
### Fixed
- **[Homepage]** Replaced Homepage environment variable string placeholders (e.g. `{{HOMEPAGE_VAR_X}}`) with direct environmental configurations (e.g. `$X`) in `services.yaml` widgets.
### Added
- **[Homepage]** Added ChrisTitusTech Windows Debloat scripts link to `bookmarks.yaml`.
- **[Docs]** Inserted the new visual Python-Docker logo image and updated features in `README.md`.

## [1.5.18] - 2026-06-10
### Fixed
- **[Homepage]** Formatted bookmarks.yaml developer section according to the exact indentation specification.
- **[Homepage]** Replaced existing widgets.yaml content with custom resources/search/datetime setup, dynamically determining the system path disk letter based on the environment installation target location.
- **[Main]** Added trailing newlines and clean terminal relaunch headers when binary swaps are executed, avoiding console text overlaps during background process spawning.

## [1.5.17] - 2026-06-10
### Fixed
- **[Homepage]** Wrapped widget configuration blocks to only output if the corresponding service URL is successfully generated. This prevents any empty widget definitions from causing Next.js URL constructor exceptions.
### Added
- **[UX]** Added Seerr post-install manual configuration steps to notify the user how to extract the SQLite-based API Key and insert it into the environment.

## [1.5.16] - 2026-06-10
### Fixed
- **[Main]** Removed duplicate local `import re` inside `invoke_token_wizard` that was causing an `UnboundLocalError` when Python attempted to access the global name before executing the local import statement.

## [1.5.15] - 2026-06-10
### Fixed
- **[Homepage]** Avoid rendering `url` and `widget` configurations for services with unresolved ports (i.e. `port == None` or `port == "0"`). This prevents Homepage from throwing URL parsing errors.
- **[Tautulli]** Added API key extraction support for Tautulli config.ini so that Homepage widgets can query it.
- **[SABnzbd]** Injected `host_whitelist = sabnzbd, localhost` into `sabnzbd.ini` to resolve HTTP hostname validation issues when queried by the homepage container.
- **[Auto-Configure]** Triggered `.env` sync to stacks right after keys are successfully extracted and written to the master `.env`, ensuring the reloaded stacks have the latest API keys.

## [1.5.14] - 2026-06-10
### Fixed
- **[Homepage]** Jellyfin widget now correctly uses `apiKey:` field instead of `key:` — the `key:` field caused Homepage to pass a raw object reference into the Jellyfin API URL, producing `api_key=[object%20Object]` and 401 authentication failures.
### Added
- **[UX]** Post-install NEXT STEPS now includes contextual guidance for Tautulli (how to retrieve the permanent Plex auth token) and Bazarr (manual Sonarr/Radarr connection steps), shown only when those services are in the selected stack.

## [1.5.13] - 2026-06-09
### Fixed
- **[Main]** Added missing `import re` to `dockersetup.py` — caused a `NameError` crash in the post-install summary when parsing credentials from the `.env` file.

## [1.5.12] - 2026-06-09
### Fixed
- **[Updater]** Clean up leftover `.old` binary backup on startup after a self-update swap completes, instead of waiting until the next update cycle.

## [1.5.11] - 2026-06-09
### Fixed
- **[Templates]** Removed `5353:5353/udp` (mDNS) from Plex compose template — conflicts with `DNS Client` on Windows and `systemd-resolved` on Linux, causing the entire `media-server` stack to fail on startup. LAN discovery still works via ports 1900/udp and 32410–32414/udp.
- **[Stitching]** Fixed Prowlarr→PVR linking returning `400 Bad Request`: moved `syncLevel` from the `fields` array to a top-level property, added required `syncProfileIds: [1]`, `implementationName`, per-app `syncCategories` and `animeSyncCategories` to match the current Prowlarr API schema.

## [1.5.10] - 2026-06-09
### Fixed
- **[Updater]** Replaced `subprocess.Popen` + `sys.exit` restart with `os.execv` on Linux/macOS, eliminating the PyInstaller temp dir race condition that caused `libpython3.11.so.1.0` to fail loading after a self-update.
- **[CI]** Switched `build-assets` workflow trigger from `release: published` to `push: tags: v*` so binaries are automatically built for every version tag without requiring a manual release first. Added `certifi` to the workflow pip install.

## [1.5.9] - 2026-06-09
### Added
- **[Self-Update]** Fully implemented update checking and binary swapping for compiled/frozen executables (Linux and Windows).
- **[UI]** Added dynamic version display to the main menu header.
- **[Permissions]** Resolved write permission issues for containers deployed on Linux (specifically immutable setups like Bazzite/SteamOS) by auto-detecting `SUDO_UID`/`SUDO_GID` and applying proper owner mapping recursively.
- **[Security]** Hardened compiled binary updater SSL verification by establishing a dedicated `certifi` CA Cert Bundle context (resolving issuer verification crashes on immutable Linux distributions).
- **[Bugfix]** Patched temporary path resolution logic (`get_resource_path`) in `dockersetup.py` for compiled executables to prevent startup `templates.yml` and `services.yml` FileNotFound crashes on reconfigurations/removals.
- **[Wizards]** Upgraded confirmation prompts to require explicit `Enter` key validation (Yes/No select lists) to prevent accidental keystroke selections.

## [1.5.8] - 2026-06-09
### Added
- **[Homepage]** Added automatic generation of `bookmarks.yaml` providing a clickable GitHub shortcut directly to the source repository.
- **[Homepage]** Added automatic generation of `docker.yaml` mapping the local `/var/run/docker.sock` to enable live container statistics and status indicators.
- **[Testing]** Extended `test_runtime.py` to assert that `bookmarks.yaml` and `docker.yaml` files are correctly generated in the Homepage configuration folder.

## [1.5.7] - 2026-06-09
### Fixed
- **[Security]** Refactored `winget` update execution in `utils/updater.py` to run as a structured list of arguments, eliminating `shell=True`.
- **[Deployment]** Enhanced concurrent image pull error handling in `modules/deploy_start.py` to return structured success/failure dictionaries, halting deployment in headless mode or presenting retry/abort/ignore menus in interactive mode.
### Added
- **[Testing]** Implemented integration test coverage in `tests/test_runtime.py` for deployment start and uninstallation procedures, using fully mocked subprocesses and user input prompts.

## [1.5.6] - 2026-06-06
### Fixed
- **[Deployment]** Enabled shell execution on all operating systems for docker compose deployment commands, resolving subprocess `[Errno 2] No such file or directory` errors on Linux.
- **[Deployment]** Ensured docker compose commands are executed in the context of their respective stack directory (`cwd=path`) so `docker-compose.yml` config files are found correctly.

## [1.5.5] - 2026-06-06
### Fixed
- **[Timezone]** Fixed an issue where the resolved timezone name fell back to Python's `"None"` string or `None` object instead of UTC/offset deduction on certain Linux hosts.
- **[Testing]** Added unit tests covering robust timezone detection, fallback flows, and headless resolution.

## [1.5.4] - 2026-06-06
### Added
- **[Interactive UI]** Implemented interactive confirmation and a filtered timezone selection menu grouped by UTC offset.

## [1.5.3] - 2026-06-06
### Added
- **[Portability]** Added robust, container-friendly timezone detection fallback methods on Linux (TZ env variable, /etc/timezone file, /etc/localtime symlink resolution, and timedatectl check).

## [1.5.2] - 2026-06-06
### Added
- **[Release]** Compiled standalone Windows (.exe) and Linux ELF binaries for distribution.

## [1.5.1] - 2026-06-05
### Fixed
- **[Error Handling]** `modules/deploy_start.py`: Fixed `NameError: name 're' is not defined` inside `test_container_conflict` by moving the import statement to the top of the file.
- **[Security]** `modules/env_wizard.py`: Replaced platform-specific `win32api` dependency with standard library `getpass.getuser()` for Windows local username queries to ensure NTFS .env permissions hardening works out-of-the-box.
- **[Security]** `modules/auto_configure.py`: Changed `re.sub` replacement parameters to use lambda functions to avoid credential injection failures and backreference corruption for passwords containing regex special characters.
- **[Portability]** `modules/env_wizard.py`: Imported `resolve_path_slash` to prevent `NameError` crash when running the environment configuration wizard on Linux.
- **[Portability]** `modules/env_wizard.py`: Hardened timezone auto-detection to fallback to `"UTC"` if `get_localzone_name()` returns `None` (common on atomic/immutable Linux distributions like Bazzite).

## [1.5.0] - 2026-06-05
### Added
- **[Monitoring]** Added native Docker container healthchecks to MariaDB and PostgreSQL templates, and a post-deployment container state audit to `modules/deploy_start.py`.
- **[Network Isolation]** Added declarative setup of `npm_proxy` and `media-internal` custom networks in `modules/network.py`. Database engines are now isolated to `media-internal` while other apps bind to both networks for ingress/egress.
- **[Config Management]** Refactored `Get-MultilineInput` prompts and updated the batch `Save-EnvVars` caching function in `utils/state.py` to cleanly double-quote and escape multi-line values in `.env`.

## [1.4.3] - 2026-06-05
### Added
- **[Error Handling]** Implemented request retries with exponential backoff and connection timeout resilience inside `Invoke-RobustRestMethod`.
- **[Testing]** Added a live networking transient failure test to `tests/test_runtime.py` under the `$env:DS_LIVE_TESTS = "true"` hook.
- **[Portability]** Refactored drive-letter resolution in `modules/directories.py` to cleanly map to standard Unix `/mnt` layouts on Linux/macOS.
- **[Security]** Added a template auditing preflight task to warning-log floating `:latest` versions in `templates.yml` on critical databases.

## [1.4.2] - 2026-06-05
### Changed
- **[Architectural Design]** Externalized metadata/arrays (`$recMap`, `$supportedWidgets`, `$configurableApps`, and `$arrApps`) from script modules into [services.yml](file:///c:/odysseus/projects/dockersetupscript/scripts/services.yml) under metadata blocks, parsed dynamically by the central YAML parser.
- **[Testing]** Updated `tests/test_runtime.py` to correctly load functions from their refactored utility modules (`utils/paths.py` and `utils/logger.py`) rather than from `dockersetup.py`.
- **[Testing]** Expanded Pester unit tests in `tests/test_runtime.py` to cover the new metadata sections.
- **[Configuration Management]** Audited `templates.yml` floating tags and reverted version pins back to `latest` per user instructions.

## [1.4.1] - 2026-06-05
### Fixed
- **[Security]** `modules/auto_configure.py`: Scoped SSL certificate bypass to individual API calls using save/restore in `try/finally`. Previously the global bypass affected the entire PowerShell session.
- **[Security]** `modules/compose_build.py`: Fixed `$matches` variable collision in secret filtering logic. The user-defined `$matches` variable shadowed the `-match` automatic variable, causing stack-local `.env` files to be incorrectly generated. Renamed to `$varMatches`.
- **[Security]** `tests/test_runtime.py`: Applied same `$matches` → `$varMatches` fix so the security test accurately validates the filtering logic.
- **[Config Management]** `modules/auto_configure.py`: Removed hardcoded `"password"` fallback for management credentials. Auth injection now loads from env vars, falls back to `.env` file, and skips gracefully with a warning if credentials are unavailable.
- **[Code Quality]** `modules/env_wizard.py`: Removed corrupted dead code at end of file (orphaned string fragments from a broken edit).
- **[Error Handling]** `modules/auto_configure.py`: Replaced empty catch blocks with structured warning logs on API stitching failures, and changed qbittorrent selection `-match` check to `-contains` to prevent false matches with `qbittorrent-vpn`.
- **[Error Handling]** `modules/directories.py`: Removed obsolete `.selected_services` flat file reading logic in favor of metadata lookup (`Get-Metadata`).
- **[Error Handling]** `modules/deploy_start.py`: Fixed deployment crash by reading stack information from `.metadata.json` (`Get-Metadata`) instead of the non-existent `.generated_stacks` file.
- **[Error Handling]** `modules/network.py`: Added a `$env:TEST_MODE` guard to bypass docker network configuration during headless E2E syntax/runtime checks.
- **[Architectural Design]** Split `utils/logger.py` into `utils/logger.py` (pure logging/external command runner) and `utils/state.py` (metadata/env file caching and persistence helpers).
- **[Performance]** `modules/env_wizard.py`: Batched all `Set-EnvVar` calls using the new `Save-EnvVars` helper in `utils/state.py`, reducing .env disk writes from 25 separate write cycles to a single batched operation.
- **[Code Quality]** Fully retired `.selected_services` flat file reads across the remaining components (`02a-port-check.ps1`, `modules/compose_build.py`, and setup routine).
- **[Security]** `.gitignore`: Updated to use case-insensitive matching for `AGENTS.md` to guarantee it is ignored on case-sensitive filesystems like Linux.
- **[Code Quality]** Unified path discovery: Introduced `Get-ProjectRoot` and `Get-DeployDir` in [utils/paths.py](file:///c:/odysseus/projects/dockersetupscript/scripts/utils/utils/paths.py) and replaced duplicated split-path inline calculations across all modules.
- **[Code Quality]** Unified registry flattening: Created `Get-RegistryList` in [utils/yaml_parser.py](file:///c:/odysseus/projects/dockersetupscript/scripts/utils/utils/yaml_parser.py) and removed duplicate array mapping logic in setup, compose-build, and auto-configure scripts.




## [1.4.0] - 2026-06-04
### Added
- **Automated Bootstrap Update**: Script now checks for project updates on launch and hot-reloads if found.
- **Smart Reconfiguration Menu**: Detected existing deployments now offer specialized sub-options (Add/Remove Services, Upgrade Templates, Full Reset).
- **Git Dependency Auto-Install**: Automatically offers to install Git via winget if missing during update checks.
- **Template Hashing**: Implemented SHA256 version tracking for `templates.yml` to signal when deployments are out of date.
- **One-Command Install**: Added a streamlined PowerShell one-liner to the README for new users.

## [1.3.0] - 2026-06-04
### Added
- **New Services**: Added FlareSolverr (Minimal), Audiobookshelf (Advanced), Scrutiny (Advanced), Vaultwarden (Advanced), and Navidrome (Advanced).
- **FlareSolverr Stitching**: Automatically configure FlareSolverr as a proxy in Prowlarr if selected.
- **Enhanced Health Checks**: Added the new services to the post-deployment health check summary.

## [1.2.0] - 2026-06-04
### Added
- **Expanded Auto-Stitching**: Automatically link SABnzbd and qBittorrent-VPN to PVRs, and PVRs to Seerr.
- **CrowdSec Integration**: Added CrowdSec to Advanced tier with automatic NPM Plus integration.
- **Service Health Check**: Added a real-time TCP port-check table to the final installation summary.
- **Privacy Rule**: qBittorrent auto-linking is now restricted to the VPN-enabled version only.

### Fixed
- Resolved "NewerThan" parameter binding error in `dockersetup.py` caused by operator misparsing.
- Optimized AIT test execution by bypassing initialization waits and health checks in `TEST_MODE`.
