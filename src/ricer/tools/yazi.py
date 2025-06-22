import logging
import os

import toml

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="yazi")
def parse_yazi(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring yazi... ")
    assert theme_data.yazi

    theme_path = theme_context.theme_path

    if not theme_data.yazi.dark or not theme_data.yazi.light:
        return ToolResult(
            theme_data=theme_data,
            install_script=install_script,
            destination_path=destination_path,
        )

    yazi_theme_path: str = os.path.join(theme_path, "build", "yazi/theme.toml")
    if os.path.exists(yazi_theme_path):
        yazi_cfg = toml.load(yazi_theme_path)
        # with open(yazi_theme_path, "rb") as f:

    else:
        yazi_cfg = {}

    if "flavor" not in yazi_cfg:
        yazi_cfg["flavor"] = {}

    if theme_data.yazi.dark:
        yazi_cfg["flavor"]["dark"] = theme_data.yazi.dark
    if theme_data.yazi.light:
        yazi_cfg["flavor"]["light"] = theme_data.yazi.light

    # toml.dump
    with open(yazi_theme_path, "w") as f:
        toml.dump(yazi_cfg, f)

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
