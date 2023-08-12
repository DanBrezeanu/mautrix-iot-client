from typing import Any, Dict

from mautrix_iot_client.configuration.conf import CONF


def determine_command(command: str) -> Dict[str, Any] | None:
    for available_command in CONF["device"]["commands"]:
        if command == available_command["name"]:
            return available_command

        if command in available_command.get("alias", ""):
            return available_command

    return None
