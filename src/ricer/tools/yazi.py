import logging
from typing import Optional

from utils.types import (
    BaseToolConfig,
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)
from utils.wrapper import tool_wrapper
import os 
import toml 

logger = logging.getLogger(__name__)


class YaziConfig(BaseToolConfig):
    dark: Optional[str]
    light: Optional[str]


@tool_wrapper(tool="yazi")
def parse_yazi(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring yazi... ")
    assert "yazi" in theme_data
    assert isinstance(theme_data['yazi'], dict)

    theme_path = theme_context["theme_path"]

    if "dark" not in theme_data["yazi"] or "light" not in theme_data["yazi"]:
        return {
            "theme_data": theme_data,
            "install_script": install_script,
            "destination_path": destination_path,
        }
        return {"theme_data": theme_data, "install_script": install_script}

    yazi_theme_path: str = os.path.join(theme_path, "build", "yazi/theme.toml")
    if os.path.exists(yazi_theme_path):
        yazi_cfg = toml.load(yazi_theme_path)
        # with open(yazi_theme_path, "rb") as f:
    else:
        yazi_cfg = {}

    if "flavor" not in yazi_cfg:
        yazi_cfg["flavor"] = {}

    if "dark" in theme_data["yazi"]:
        yazi_cfg["flavor"]["dark"] = theme_data["yazi"]["dark"]
    if "light" in theme_data["yazi"]:
        yazi_cfg["flavor"]["light"] = theme_data["yazi"]["light"]

    # toml.dump
    with open(yazi_theme_path, "w") as f:
        toml.dump(yazi_cfg, f)

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
    return {"theme_data": theme_data, "install_script": install_script}
