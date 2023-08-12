from typing import Any, Dict, List, Literal, TypedDict

from typing_extensions import NotRequired


class _GenericCommand(TypedDict):
    type: str


class _RequestCommandBody(TypedDict):
    format: str
    type: Literal["json", "data"]


class _RequestCommand(_GenericCommand):
    type: Literal["request"]
    method: Literal["GET", "PUT", "POST", "DELETE", "PATCH"]
    host: str
    headers: NotRequired[Dict[str, str]]
    body: NotRequired[_RequestCommandBody]
    format: str


class _CLICommand(_GenericCommand):
    type: Literal["cli"]
    command: str


class Command(TypedDict):
    name: str
    args: NotRequired[List[str]]
    alias: NotRequired[str]
    description: NotRequired[str]
    allow_contains_alias: NotRequired[bool]
    command: _GenericCommand


class RequestCommand(Command):
    command: _RequestCommand


class CLICommand(Command):
    command: _CLICommand
