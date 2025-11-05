import logging

from ricer.utils.common import append_text, overwrite_or_append_line
from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper
import os 
logger = logging.getLogger(__name__)


@tool_wrapper(tool="dunst")
def parse_dunst(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring dunst... ")
    
    if theme_data.font or os.environ.get("FONT"):
        font = os.environ.get("FONT", theme_data.font)

        font_size = theme_data.dunst.font_size or \
                        os.environ.get("FONTSIZEPX", 11)

        overwrite_or_append_line(
            "font = ",
            f'font = "{font} {font_size}"\n',
            os.path.join(destination_path, "dunstrc"),
        )

    install_script += "dunstctl reload \n"
    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
