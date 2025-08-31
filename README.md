# Superset API CLI

A powerful command-line interface (CLI) tool built with Python and Typer for interacting with an Apache Superset instance via its REST API. This tool simplifies user, role, and permission management.

## Features

- **Basic API Calls**: Make direct, authenticated calls to any Superset API endpoint.
- **User Management**: List existing users and create new ones.
- **Role Management**: List existing roles and create new ones.
- **Permission Management**: List all available permissions and assign them to roles.

## Installation

1.  **Clone or download the script** to your local machine.
2.  **Create and activate a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# OR
.\venv\Scripts\activate  # On Windows
```

## Usage

The general syntax for any command is:
```bash
python superset-api.py [GLOBAL-OPTIONS] COMMAND [COMMAND-OPTIONS]

Use `--help` on any command to see its specific options and usage.

## License

This project is provided as-is.
