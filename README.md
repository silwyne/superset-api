# Superset API CLI

A powerful command-line interface (CLI) tool built with Python and Typer for interacting with an Apache Superset instance via its REST API. This tool simplifies user, role, and permission management.

## Features

- **Basic API Calls**: Make direct, authenticated calls to any Superset API endpoint.
- **User Management**: List existing users and create new ones.
- **Role Management**: List existing roles and create new ones.
- **Permission Management**: List all available permissions and assign them to roles.

## Prerequisites

- Python 3.7+
- An Apache Superset instance running and accessible
- Admin credentials for the Superset instance (or a user with appropriate permissions)

## Installation

1.  **Clone or download the script** to your local machine.
2.  **Create and activate a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # OR
    .\venv\Scripts\activate  # On Windows
    ```

3.  **Install the required dependencies**. Create a `requirements.txt` file with the following content:

    ```txt
    typer
    requests
    rich
    ```

    Then install them:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The tool uses command-line options for configuration. The default connection parameters are:
- `--url` / `-h`: `http://localhost:8088`
- `--user` / `-u`: `admin`
- `--pass` / `-p`: `admin`

You can override these defaults with each command.

## Usage

The general syntax for any command is:
```bash
python superset-api.py [GLOBAL-OPTIONS] COMMAND [COMMAND-OPTIONS]

Use `--help` on any command to see its specific options and usage.

### Global Help
Get an overview of all available commands.
bash
python superset-api.py --help

### 1. Basic API Call (`basic-api`)
A flexible command to make any authenticated API call to your Superset instance.

**Help:**
bash
python superset-api.py basic-api --help

**Example: Get database list**
bash
python superset-api.py basic-api \
  --url http://your-superset-host:8088 \
  --user your_admin_user \
  --pass your_admin_password \
  --api /api/v1/database/

**Example: Create a new dataset (POST request)**
*Note: You would typically need to provide a JSON body via stdin or a file for POST/PUT requests, which might require extending the script.*
bash
# This demonstrates the structure, though sending a body might need script modification.
python superset-api.py basic-api \
  -m POST \
  -a /api/v1/dataset/ \
  -h http://your-superset-host:8088
# You would then pipe your JSON data into the command

### 2. List Roles (`list-roles`)
Fetches and displays all roles defined in the Superset instance.

**Help:**
bash
python superset-api.py list-roles --help

**Example: List roles on a specific instance**
bash
python superset-api.py list-roles \
  -h http://superset.prod.example.com:8088 \
  -u admin \
  -p secure_password_123

### 3. List Users (`list-users`)
Fetches and displays all users registered in the Superset instance.

**Help:**
bash
python superset-api.py list-users --help

**Example: List users using short options**
bash
python superset-api.py list-users -h http://localhost:8088 -u admin -p admin

### 4. List Permissions (`list-perms`)
Fetches and displays permissions available in Superset. Results are paginated.

**Help:**
bash
python superset-api.py list-perms --help

**Example: List the first 100 permissions**
bash
python superset-api.py list-perms \
  --page 0 \
  --page-size 100 \
  -h http://localhost:8088

**Example: List the second page of permissions (items 25-49)**
bash
python superset-api.py list-perms --page 1 --page-size 25

### 5. Create Role (`create-role`)
Creates a new role in Superset.

**Help:**
bash
python superset-api.py create-role --help

**Example: Create a new role named "Analyst"**
bash
python superset-api.py create-role \
  --name "Analyst" \
  -h http://localhost:8088 \
  -u admin \
  -p admin

### 6. Create User (`create-user`)
Creates a new user account in Superset.

**Help:**
bash
python superset-api.py create-user --help

**Example: Create an active user named "jane.doe"**
bash
python superset-api.py create-user \
  --username "jane.doe" \
  --firstname "Jane" \
  --lastname "Doe" \
  --email "jane.doe@example.com" \
  --roles "Public" \  # Use the exact role name(s) from your Superset instance. For multiple roles, provide a comma-separated string: "Alpha, Gamma"
  --active \
  --password "SecurePass789!" \
  -h http://localhost:8088
*Note: The `--roles` argument expects the exact name(s) of existing roles as a string. Check available roles first with `list-roles`.*

### 7. Add Permissions (`add-perms`)
Adds a set of permissions to an existing role.

**Help:**
bash
python superset-api.py add-perms --help

**Example: Add permissions to role ID 5**
bash
python superset-api.py add-perms \
  --id 5 \  # Use the role ID obtained from 'list-roles'
  --permissions "[{'permission_name': 'can_read', 'view_menu_name': 'Dashboard'}, {'permission_name': 'menu_access', 'view_menu_name': 'Security'}]" \
  -h http://localhost:8088
*Crucial: The `--permissions` argument must be a valid JSON string representing a list of permission objects. The exact structure (`permission_name`, `view_menu_name`) must match the Superset API expectations. Use `list-perms` to find valid permission names and view menus. The `--id` requires the numeric ID of the role, which you can get from the `list-roles` command output.*

## Getting Role IDs for `add-perms`

The `add-perms` command requires the numeric ID of the role. Run `list-roles` and look for the `id` field in the output for the role you want to modify.

Example `list-roles` output snippet:
json
{
  "id": 5,
  "name": "Analyst",
  ...
}
In this case, you would use `--id 5` for the "Analyst" role.

## Troubleshooting

- **Connection Errors**: Verify the `--url`, `--user`, and `--pass` values. Ensure the Superset instance is running and accessible from your machine.
- **Authentication Errors (401)**: Double-check the username and password. The user must have the necessary permissions to perform the requested actions (e.g., admin rights for creating users/roles).
- **Permission Errors (403)**: The authenticated user lacks the required permissions for the specific API endpoint.
- **Not Found Errors (404)**: The API endpoint specified (especially in `basic-api`) might be incorrect or not available in your version of Superset.
- **Invalid JSON for `add-perms`**: Ensure the string passed to `--permissions` is valid JSON. Use single quotes around the string and double quotes inside for the JSON keys/values, or escape the quotes appropriately for your shell.

## Security Note

- Avoid passing passwords directly on the command line in production scripts, as they may be visible in process lists and shell history. Consider using environment variables or secure password prompts for sensitive data. You could extend the script to read credentials from a config file or environment variables (e.g., `SUPERSET_URL`, `SUPERSET_USERNAME`, `SUPERSET_PASSWORD`).

## License

This project is provided as-is.
