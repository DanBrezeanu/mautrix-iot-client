import json
import re
from typing import Dict, List, cast

import requests

from mautrix_iot_client.consts import REQUEST_CLI_TYPE, REQUEST_COMMAND_TYPE
from mautrix_iot_client.types import CLICommand, Command, RequestCommand


def execute_command(command: Command, args: List[str]) -> str:
    if command["command"]["type"] == REQUEST_CLI_TYPE:
        return execute_cli_command(cast(CLICommand, command), args)
    elif command["command"]["type"] == REQUEST_COMMAND_TYPE:
        return execute_request_command(cast(RequestCommand, command), args)

    raise ValueError("Invalid command type")


def execute_request_command(command: RequestCommand, args: List[str]) -> str:
    def _replace_args(value: str, args: Dict[str, str]):
        for arg_name, arg_value in args.items():
            value = value.replace(f"${arg_name}", arg_value)
        return value

    if len(args) != len(command.get("args", [])):
        raise ValueError("All arguments must be provided.")

    arguments = {
        **{name: value for name, value in zip(command.get("args", []), args)},
        "host": command["command"]["host"],
    }

    format = _replace_args(command["command"]["format"], arguments)
    body = None
    headers = None
    request_kwargs = {}

    if "body" in command["command"]:
        body = _replace_args(command["command"]["body"]["format"], arguments)

        if command["command"]["body"]["type"] == "json":
            try:
                request_kwargs["json"] = json.loads(body)
            except json.JSONDecodeError:
                raise ValueError("Could not convert body to JSON.")
        elif command["command"]["body"]["type"] == "data":
            request_kwargs["data"] = body

    if "headers" in command["command"]:
        headers = command["command"]["headers"].copy()
        for header, value in headers.items():
            headers[header] = _replace_args(value, arguments)

        request_kwargs["headers"] = headers

    response = getattr(requests, command["command"]["method"].lower())(
        format, **request_kwargs
    )

    if response.text:
        return response.text

    return "OK"


def execute_cli_command(command: CLICommand, args: List[str]) -> str:
    pass
