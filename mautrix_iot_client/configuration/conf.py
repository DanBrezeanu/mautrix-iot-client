import os
from typing import Any, Dict

import jsonschema
import yaml

from mautrix_iot_client.configuration.schema import configuration_schema


def read_configuration(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file {path} does not exist.")

    conf = yaml.full_load(open(path, "r"))

    jsonschema.validate(conf, schema=configuration_schema)

    return conf


CONF = read_configuration("./device.yaml")
