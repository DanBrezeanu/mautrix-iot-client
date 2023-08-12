request_command_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "pattern": "^request$"},
        "method": {"type": "string", "enum": ["GET", "PUT", "POST", "DELETE", "PATCH"]},
        "host": {"type": "string", "format": "hostname"},
        "headers": {
            "type": "object",
            "additionalProperties": True,
        },
        "body": {
            "type": "object",
            "properties": {
                "format": {"type": "string"},
                "type": {"type": "string", "enum": ["json", "data"]},
            },
            "required": [
                "format",
                "type",
            ],
        },
        "format": {"type": "string"},
    },
    "required": [
        "type",
        "method",
        "host",
        "format",
    ],
    "additionalProperties": False,
}

cli_command_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "pattern": "^cli$"},
        "command": {"type": "string"},
    },
    "required": [
        "type",
        "command",
    ],
    "additionalProperties": False,
}


configuration_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "type": "object",
    "properties": {
        "appservice": {
            "type": "object",
            "properties": {
                "addresses": {
                    "type": "array",
                    "items": {"type": "string", "format": "hostname"},
                }
            },
            "required": [
                "addresses",
            ],
            "additionalProperties": False,
        },
        "device": {
            "type": "object",
            "properties": {
                "api_key": {"type": "string"},
                "commands": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "args": {"type": "array", "items": {"type": "string"}},
                            "alias": {"type": "string"},
                            "description": {"type": "string"},
                            "allow_contains_alias": {"type": "boolean"},
                            "command": {
                                "anyOf": [
                                    request_command_schema,
                                    cli_command_schema,
                                ],
                            },
                        },
                        "required": [
                            "name",
                            "command",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            "required": [
                "api_key",
                "commands",
            ],
            "additionalProperties": False,
        },
    },
    "required": [
        "appservice",
        "device",
    ],
    "additionalProperties": False,
}
