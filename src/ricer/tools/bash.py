import logging
import os
from textwrap import dedent

from ricer.utils.common import append_text
from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="bash")
def parse_bash(
    theme_data: "ThemeData",
    theme_context: "ThemeContext",
    user_config: "UserConfig",
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring bash... ")
    assert theme_data.bash
    feats = theme_data.bash.feats

    if theme_data.wallpaper:
        wallpaper_file = theme_data.wallpaper.file
        wallpaper_path = os.path.expanduser(f"~/Pictures/wallpapers/{wallpaper_file}")
    else:
        wallpaper_path = ""

    prompts_dict = {
        "cowsay_fortune": (
            "fortune | cowsay -f $(ls /usr/share/cowsay/cows/ " "| shuf -n1)\n"
        ),
        "neofetch": "neofetch\n",
        "fastfetch": "fastfetch\n",
        "run_pywal": f"wal -n -e -i {wallpaper_path} > /dev/null \n",
        "git_onefetch": dedent(
            """

                function show_onefetch() {
                    if [ -d .git ]; then
                        onefetch
                    fi
                }
                function cd() { builtin cd "$@" && show_onefetch; }
                \n
            """
        ),
    }

    dest = os.path.join(destination_path, ".bashrc")

    for d in prompts_dict:
        if d in feats:
            if d == "run_pywal" and wallpaper_path is None:
                logger.error("Cannot add pywal to bash config, no wallpaper")
                continue
            if d == "neofetch":
                logger.warning("using fastfetch instead of neofetch")
            append_text(dest, prompts_dict[d])

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
