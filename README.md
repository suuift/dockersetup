# Docker Setup Suite (Python Version)

This is a cross-platform, Python-based version of the Docker Setup Suite, migrated from the original PowerShell codebase. It orchestrates deployment of a self-hosted media stack using Dockge on both Windows and Linux environments.

---

## 🛠️ Tech Stack & Requirements

- **Python**: 3.10 or higher
- **Docker**: Engine & Docker Compose V2
- **Key Libraries**:
  - `questionary` (Interactive CLI menus)
  - `rich` (Terminal styles and logs)
  - `ruamel.yaml` (YAML preservation parsing)
  - `python-dotenv` (Environment variables loader)
  - `requests` (API integration client)

---

## 🚀 How to Run

### Option 1: Using Virtual Environment (Recommended)

1. Clone/Navigate to the project root:
   ```bash
   cd C:/odysseus/projects/dockersetupscriptpy
   ```
2. Activate the virtual environment:
   * **Windows**:
     ```powershell
     .venv\Scripts\activate
     ```
   * **Linux/macOS**:
     ```bash
     source .venv/bin/activate
     ```
3. Execute the setup manager:
   ```bash
   python dockersetup.py
   ```

### Option 2: Running Tests

To verify code integrity, execute the pytest suite:
```bash
pytest tests/test_runtime.py
```
