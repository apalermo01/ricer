import logging
import os
from typing import Optional

from utils.common import append_if_not_present, overwrite_or_append_line
from utils.types import (
    BaseToolConfig,
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)
from utils.validate import available_terminals
from utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


class i3Config(BaseToolConfig):
    font: Optional[str]
    font_size: Optional[int]


@tool_wrapper(tool="i3")
def parse_i3(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring i3... ")
    _configure_terminal(theme_data, destination_path, theme_context["theme_path"])
    _configure_picom(theme_data, destination_path, theme_context["theme_path"])
    _configure_font(theme_data, destination_path, theme_context["theme_path"])
    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
    return {"theme_data": theme_data, "install_script": install_script}


def _configure_terminal(config: ThemeData, dest: str, theme_path: str):

    terminal: str = "gnome-terminal"

    # check the theme config for a terminal. If it is specified, then
    # start that using $mod+Return in i3
    for i in available_terminals:
        if i in config:
            terminal = i
            logger.info(
                f"Found {i} in theme's config. "
                + "Assigning this terminal to $mod+Return"
            )

    # TODO: experiment more with this pattern. I don't know
    # if this is actually necessary
    # if "terminal" not in config["i3"]:
    terminal_path = "i3/config"
    # else:
    #     terminal_path = config["i3"]["terminal"].get("terminal_path", "i3/config")

    terminal_path = os.path.join(theme_path, "build", terminal_path)

    pattern: str = "bindsym $mod+Return exec"
    replace_text: str = f"bindsym $mod+Return exec {terminal}"

    overwrite_or_append_line(
        pattern=pattern, replace_text=replace_text, dest=terminal_path
    )

    logger.info(f"updated terminal: {terminal}")


def _configure_picom(config: ThemeData, dest: str, theme_path: str):

    if "picom" not in config:
        return

    dest_path = os.path.join(dest, "config")

    logger.info("picom found in this theme's config")
    append_if_not_present("\nexec killall picom\n", dest_path)
    append_if_not_present(
        "\nexec_always picom --backend glx --config ~/.config/picom/picom.conf\n",
        dest_path,
    )


def _configure_font(config: ThemeData, dest: str, theme_path: str):
    font = (
        os.environ.get("FONT")
        or config["i3"].get("font")
        or config.get("font_family")
        or "xft:URWGothic-Book"
    )

    font_size = config["i3"].get("font_size", 11)
    i3_config_path = os.path.join(theme_path, "build", "i3/config")
    pattern: str = "font "
    txt: str = f"font {font} {font_size}"
    overwrite_or_append_line(pattern=pattern, replace_text=txt, dest=i3_config_path)
