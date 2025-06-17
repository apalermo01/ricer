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


class DunstConfig(BaseToolConfig):
    pass


@tool_wrapper(tool="dunst")
def parse_dunst(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring dunst... ")

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
    return {"theme_data": theme_data, "install_script": install_script}
