import logging

from src.utils.types import (
    BaseToolConfig,
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)
from src.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


class AlacrittyConfig(BaseToolConfig):
    pass


@tool_wrapper(tool="alacritty")
def parse_alacritty(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring rofi... ")

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
