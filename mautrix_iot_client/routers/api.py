from typing import Annotated, Any, Dict, Optional, Union

from fastapi import APIRouter, Depends, Header
from fastapi.responses import HTMLResponse, JSONResponse

from mautrix_iot_client.commands import execute_command
from mautrix_iot_client.configuration.conf import CONF
from mautrix_iot_client.utils import determine_command

router = APIRouter(prefix="/api/v1")


@router.get(f"/ping")
async def ping():
    return JSONResponse({})


@router.get("/commands")
async def list_commands():
    return JSONResponse(
        [
            {
                "name": command["name"],
                "alias": command["alias"],
                "description": command.get("description", ""),
                "args": command.get("args", []),
            }
            for command in CONF["device"]["commands"]
        ]
    )


@router.post("/command")
async def command(
    body: Dict[str, Any],
):
    if (
        "command" not in body
        or "args" not in body
        or not isinstance(body["args"], list)
    ):
        return HTMLResponse(content="Bad request", status_code=400)

    recvd_command = body["command"]
    args = body["args"]

    command = determine_command(recvd_command)
    if command is None:
        return HTMLResponse(content="Command not found", status_code=404)

    try:
        response = execute_command(command, args)
    except ValueError as error:
        return HTMLResponse(content=f"{error}", status_code=400)

    return HTMLResponse(content=response)
