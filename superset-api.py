import typer
import requests
import json
import sys
from datetime import datetime
from typing import Optional, List


app = typer.Typer()


class Logger():

    @staticmethod
    def info(message: str):
        time = datetime.now()
        typer.echo(f"[{time}] INFO: {message}")

    @staticmethod
    def error(message: str):
        time = datetime.now()
        typer.secho(f"[{time}] ERROR: {message}", fg=typer.colors.BRIGHT_RED)


class RequestHandler():

    @staticmethod
    def request_with_token(
        access_token: str,
        method: str,
        api_endpoint: str,
        headers: dict = None,
        json_payload: dict = None,
        params: dict = None,
        timeout: int = 5,
    ) -> requests.Response:
        
        pre_prepared_header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        # adding user headers to pre prepared headers
        if headers:
            for key, value in headers.item():
                pre_prepared_header[key] = value

        method = method.upper()
        Logger.info(f"headers: {pre_prepared_header}")
        Logger.info(f"Sending {method} request to {api_endpoint}")
        try:
            response = requests.request(
                method=method,
                url=api_endpoint,
                headers=pre_prepared_header,
                json=json_payload,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            Logger.error(f"Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                Logger.error(f"Response content: {e.response.text}")
                sys.exit(1)

    @staticmethod
    def get_access_token(
        superset_host: str,
        user: str,
        password: str
        ) -> str:
        login_endpoint = f"{superset_host}/api/v1/security/login"
        login_payload = {
            "username": user,
            "password": password,
            "provider": "db"
        }
        try:
            Logger.info("Logging in to get access token...")
            login_response = requests.post(login_endpoint, json=login_payload, timeout=5)
            login_response.raise_for_status()
            access_token = login_response.json()["access_token"]
            Logger.info("Access token obtained successfully!")
            return access_token
        except requests.exceptions.RequestException as e:
            Logger.error(f"Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                Logger.error(f"Response content: {e.response.text}")
                sys.exit(1)


class Utils():

    @staticmethod
    def log_http_response(response: requests.Response):
        Logger.info(f"API result: {json.dumps(response.json(), indent=2)}")


SUPERSET_HOST_TYPER_OPTION = typer.Option("http://localhost:8088", "--url", "-h", help="Superset host URL")
USERNAME_TYPER_OPTION = typer.Option("admin", "--user", "-u", help="Username to connect to superset")
PASSWORD_TYPER_OPTION = typer.Option("admin", "--pass", "-p", help="Password for authentication")
METHOD_TYPER_OPTION = typer.Option("GET", "--method", "-m", help="HTTP method of request GET/PUT/POST/DELETE")
API_TYPER_OPTION = typer.Option(..., "--api", "-a", help="The superset api example: /api/v1/security/roles")
PAGE_SIZE_TYPER_OPTION = typer.Option(25, "--page-size", help="How many permissions in a page you want to see")
PAGE_TYPER_OPTION = typer.Option(0, "--page", help="The page number you want to see")

USERNAME_TO_CREATE_TYPER_OPTION = typer.Option(..., "--username", help="Username of the user you want to create")
FIRSTNAME_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--firstname", help="Firstname of the user you want to create")
LASTNAME_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--lastname", help="Lastname of the user you want to create")
ACTIVE_STATUS_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--active", help="Active status of the user you want to create")
ROLES_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--roles", help="Roles of the user you want to create")
EMAIL_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--email", help="Email of the user you want to create")
PASSWORD_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--password", help="Password of the user you want to create")

PERMISSIONS_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--permissions", help="Permissions you want to give to role")
ROLENAME_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--name", help="Name you wanna assign to role")
ROLE_ID_TO_ASSIGN_TYPER_OPTION = typer.Option(..., "--id", help="Role id you wanna work with")

@app.command(name="basic-api")
def basic_v1_api(
        superset_host: str = SUPERSET_HOST_TYPER_OPTION,
        user: str = USERNAME_TYPER_OPTION,
        password: str = PASSWORD_TYPER_OPTION,
        method: str = METHOD_TYPER_OPTION,
        api: str = API_TYPER_OPTION
    ):
    access_token = RequestHandler.get_access_token(
        superset_host=superset_host,
        user=user,
        password=password,
    )
    api_endpoint = f"{superset_host}{api}"
    api_response = RequestHandler.request_with_token(
        access_token=access_token,
        method=method,
        api_endpoint=api_endpoint
    )
    Utils.log_http_response(api_response)


@app.command(name="list-roles")
def list_roles(
        superset_host: str = SUPERSET_HOST_TYPER_OPTION,
        user: str = USERNAME_TYPER_OPTION,
        password: str = PASSWORD_TYPER_OPTION,
    ):
    access_token = RequestHandler.get_access_token(
        superset_host=superset_host,
        user=user,
        password=password,
    )
    api_endpoint = f"{superset_host}/api/v1/security/roles/"
    api_response = RequestHandler.request_with_token(
        access_token=access_token,
        method="GET",
        api_endpoint=api_endpoint
    )
    Utils.log_http_response(api_response)


@app.command(name="list-users")
def list_users(
        superset_host: str = SUPERSET_HOST_TYPER_OPTION,
        user: str = USERNAME_TYPER_OPTION,
        password: str = PASSWORD_TYPER_OPTION,
    ):
    access_token = RequestHandler.get_access_token(
        superset_host=superset_host,
        user=user,
        password=password,
    )
    api_endpoint = f"{superset_host}/api/v1/security/users/"
    api_response = RequestHandler.request_with_token(
        access_token=access_token,
        method="GET",
        api_endpoint=api_endpoint
    )
    Utils.log_http_response(api_response)
    

@app.command(name="list-perms")
def list_perms(
        superset_host: str = SUPERSET_HOST_TYPER_OPTION,
        user: str = USERNAME_TYPER_OPTION,
        password: str = PASSWORD_TYPER_OPTION,
        page: int = PAGE_TYPER_OPTION,
        page_size: int = PAGE_SIZE_TYPER_OPTION
    ):
    access_token = RequestHandler.get_access_token(
        superset_host=superset_host,
        user=user,
        password=password,
    )
    api_endpoint = f"{superset_host}/api/v1/security/permissions-resources/?q=(page:{page},page_size:{page_size})"
    api_response = RequestHandler.request_with_token(
        access_token=access_token,
        method="GET",
        api_endpoint=api_endpoint
    )
    Utils.log_http_response(api_response)


@app.command(name="create-user")
def create_user(
        superset_host: str = SUPERSET_HOST_TYPER_OPTION,
        user: str = USERNAME_TYPER_OPTION,
        password: str = PASSWORD_TYPER_OPTION,
        username: str = USERNAME_TO_CREATE_TYPER_OPTION,
        firstname: str = FIRSTNAME_TO_ASSIGN_TYPER_OPTION,
        lastname: str = LASTNAME_TO_ASSIGN_TYPER_OPTION,
        email: str = EMAIL_TO_ASSIGN_TYPER_OPTION,
        roles: str = ROLES_TO_ASSIGN_TYPER_OPTION,
        active: bool = ACTIVE_STATUS_TO_ASSIGN_TYPER_OPTION,
        password_to_assign: str = PASSWORD_TO_ASSIGN_TYPER_OPTION
    ):
    roles_list = [int(role.strip()) for role in roles.split(',')] if roles else []
    access_token = RequestHandler.get_access_token(
        superset_host=superset_host,
        user=user,
        password=password,
    )
    api_endpoint = f"{superset_host}/api/v1/security/users/"
    payload = {
        "active": active,
        "email": email,
        "first_name": firstname,
        "last_name": lastname,
        "password": password_to_assign,
        "roles": roles_list,
        "username": username
    }
    Logger.info(f"payload : {payload}")
    api_response = RequestHandler.request_with_token(
        access_token=access_token,
        method="POST",
        api_endpoint=api_endpoint,
        json_payload=payload
    )
    Utils.log_http_response(api_response)


@app.command(name="create-role")
def create_role(
        superset_host: str = SUPERSET_HOST_TYPER_OPTION,
        user: str = USERNAME_TYPER_OPTION,
        password: str = PASSWORD_TYPER_OPTION,
        role_name: str = ROLENAME_TO_ASSIGN_TYPER_OPTION
    ):
    access_token = RequestHandler.get_access_token(
        superset_host=superset_host,
        user=user,
        password=password,
    )
    Logger.info(f"Creating the Role")
    api_endpoint = f"{superset_host}/api/v1/security/roles"
    payload = {
        "name": role_name
    }
    Logger.info(f"payload : {payload}")
    api_response = RequestHandler.request_with_token(
        access_token=access_token,
        method="POST",
        api_endpoint=api_endpoint,
        json_payload=payload
    )
    Utils.log_http_response(api_response)


@app.command(name="add-perms")
def add_perms(
        superset_host: str = SUPERSET_HOST_TYPER_OPTION,
        user: str = USERNAME_TYPER_OPTION,
        password: str = PASSWORD_TYPER_OPTION,
        permissions: str = PERMISSIONS_TO_ASSIGN_TYPER_OPTION,
        role_id: str = ROLE_ID_TO_ASSIGN_TYPER_OPTION
    ):
    access_token = RequestHandler.get_access_token(
        superset_host=superset_host,
        user=user,
        password=password,
    )
    Logger.info(f"Creating the Role")
    api_endpoint = f"{superset_host}/api/v1/security/roles/{role_id}/permissions"
    permission_list = [int(permission.strip()) for permission in permissions.split(',')] if permissions else []
    payload = {
        "permission_view_menu_ids": permission_list
    }
    Logger.info(f"payload : {payload}")
    api_response = RequestHandler.request_with_token(
        access_token=access_token,
        method="POST",
        api_endpoint=api_endpoint,
        json_payload=payload
    )
    Utils.log_http_response(api_response)


if __name__ == "__main__":
    app()
