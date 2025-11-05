import logging

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="sioyek")
def parse_sioyek(
    theme_data: "ThemeData",
    theme_context: "ThemeContext",
    user_config: "UserConfig",
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring sioyek... ")

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
