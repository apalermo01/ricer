import configparser
import json
import logging
import os
import shutil
from typing import Optional

from src.utils.common import overwrite_or_append_line
from src.utils.types import (
    BaseToolConfig,
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)
from src.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


class PolybarConfig(BaseToolConfig):
    bars: Optional[list[str]]
    start_script: Optional[str]


@tool_wrapper(tool="polybar")
def parse_polybar(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:

    logger.info("Loading polybar...")
    assert "polybar" in theme_data
    assert isinstance(theme_data["polybar"], dict)

    theme_path = theme_context["theme_path"]
    polybar = configparser.ConfigParser()

    polybar_files = os.walk(destination_path)

    for root, dirs, files in polybar_files:
        for file in files:
            config_subfile = os.path.join(root, file)
            polybar = configparser.ConfigParser()
            polybar.read(config_subfile)
            if "colors" in polybar:
                polybar = _parse_colors(polybar, theme_path)
                with open(config_subfile, "w") as f:
                    polybar.write(f)
                logger.info(f"wrote polybar config with colors to {config_subfile}")

    # launch script
    # print("user config = ", user_config.keys())
    if 'scripts_root' in user_config:
        assert 'scripts_root' in user_config
        assert isinstance(user_config['scripts_root'], str)
        scripts_root = os.path.expanduser(user_config['scripts_root'])
    else:
        scripts_root = "./scripts"

    src_script = os.path.join(scripts_root, "i3_polybar_start.sh")
    destination_dir_script = os.path.join(destination_path, "i3_polybar_start.sh")

    with open(destination_dir_script, "w") as f:
        pass

    shutil.copy2(src_script, destination_path)
    logger.info(f"copied polybar startup script from {src_script} to {destination_path}")

    if theme_data["polybar"].get("bars"):
        assert isinstance(theme_data["polybar"]["bars"], list)
        bar_names: list = theme_data["polybar"]["bars"]
    else:
        bar_names: list = ["main"]
    bar_names_str = ""
    for b in bar_names:
        bar_names_str += f' "{b}"'

    overwrite_or_append_line(
        "declare -a bar_names=()",
        f"declare -a bar_names=({bar_names_str})",
        os.path.join(destination_path, "i3_polybar_start.sh"),
    )

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }

    return {"theme_data": theme_data, "install_script": install_script}


def _parse_colors(polybar: configparser.ConfigParser, theme_path: str):

    colorscheme_path: str = os.path.join(theme_path, "colors", "colorscheme.json")

    with open(colorscheme_path, "r") as f:
        colorscheme: dict = json.load(f)

    for c in polybar["colors"]:
        color_str = polybar["colors"][c]
        if "<" not in color_str:
            continue
        color_key = color_str.split("<")[1].split(">")[0]
        if color_key in colorscheme:
            polybar["colors"][c] = colorscheme[color_key]

    return polybar
