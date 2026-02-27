# Copyright 2025 Peter Mitrano
# Licensed under the Apache License, Version 2.0

from pathlib import Path
import json
from jinja2 import Template

from colcon_core.plugin_system import satisfies_version
from colcon_core.verb import VerbExtensionPoint

# This will be converted to json string, then template expanded, then written to defaults.json
DEFAULTS_DICT = {
    "build": {
        "build-base": "{{WS}}/build",
        "install-base": "{{WS}}/install",
        "base-paths": ["{{WS}}"],
        "symlink-install": True,
        "cmake-args": [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
        ],
    }
}


class direnvVerb(VerbExtensionPoint):
    """initialize COLCON_DEFAULTS_FILE and set up .envrc file for direnv tool"""

    def __init__(self):
        super().__init__()
        satisfies_version(VerbExtensionPoint.EXTENSION_POINT_VERSION, "^1.0")

    def argument_parser(self, *, parser):
        pass

    def main(self, *, context):
        as_json_str = json.dumps(DEFAULTS_DICT)
        tpl = Template(as_json_str)
        workspace_path = Path.cwd()
        rendered_str = tpl.render(WS=str(workspace_path))
        rendered_dict = json.loads(rendered_str)

        defaults_path = workspace_path / "defaults.json"
        with defaults_path.open("w") as f:
            json.dump(rendered_dict, f, indent=4)

        envrc_path = workspace_path / ".envrc"

        lines = [
            f"source {workspace_path}/install/setup.bash",
            f"export COLCON_DEFAULTS_FILE={defaults_path}",
            f"export COLCON_LOG_PATH={workspace_path}/log",
        ]

        lines = [line + "\n" for line in lines]
        with envrc_path.open("w") as f:
            f.writelines(lines)
