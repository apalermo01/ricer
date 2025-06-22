import logging
import os

from ricer.utils.common import append_text
from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)




@tool_wrapper(tool="kitty")
def parse_kitty(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring kitty... ")

    if theme_data.fish:
        append_text(
            os.path.join(destination_path, "kitty.conf"), "chsh -s /usr/bin/fish\n"
        )

    if theme_data.font or os.environ.get("FONT"):
        font = os.environ.get("FONT") or theme_data.font

        append_text(
            os.path.join(destination_path, "kitty.conf"),
            f'font_family   family="{font}"\n',
        )
        append_text(
            os.path.join(destination_path, "kitty.conf"),
            f"bold_font     auto\n",
        )
        append_text(
            os.path.join(destination_path, "kitty.conf"),
            f"italic_font     auto\n",
        )
        append_text(
            os.path.join(destination_path, "kitty.conf"),
            f"bold_italic_font     auto\n",
        )

    font_size = os.environ.get("FONTSIZEPX") or theme_data.font_size or None
    if font_size:
        append_text(
            os.path.join(destination_path, "kitty.conf"),
            f"font_size     {font_size}\n",
        )

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
