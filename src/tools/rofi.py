from src.utils.types import BaseToolConfig, ThemeContext, ThemeData, ToolResult, UserConfig
from src.utils.wrapper import tool_wrapper
import logging

logger = logging.getLogger(__name__)

class RofiConfig(BaseToolConfig):
    pass

@tool_wrapper(tool="rofi")
def parse_rofi(
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
    return {"theme_data": theme_data, "install_script": install_script}
