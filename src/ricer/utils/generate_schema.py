import json
import os

from ricer.utils.types import ThemeData


def main():
    schema_path = os.path.expanduser("~/.config/ricer/")
    schema = ThemeData.model_json_schema()
    print("writing json schema to ", schema_path)
    with open(schema_path, "w") as f:
        json.dump(schema, f, indent=2)
