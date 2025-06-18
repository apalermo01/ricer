from ricer.utils.types import BaseToolConfig, ThemeContext, ThemeData, ToolResult, UserConfig
from ricer.utils.wrapper import tool_wrapper
import logging

logger = logging.getLogger(__name__)

class FastfetchConfig(BaseToolConfig):
    pass

@tool_wrapper(tool="fastfetch")
def parse_fastfetch(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring fastfetch... ")

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
    return {"theme_data": theme_data, "install_script": install_script}
