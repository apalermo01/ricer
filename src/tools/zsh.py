import logging
import os
from textwrap import dedent
from typing import Literal, Optional

from src.utils.common import append_text
from src.utils.types import (
    BaseToolConfig,
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)
from src.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


class ZshConfig(BaseToolConfig):
    feats: Optional[
        list[
            Literal[
                "cowsay_fortune", "neofetch", "fastfetch", "run_pywal", "git_onefetch"
            ]
        ]
    ]
    zsh: Optional[bool]


@tool_wrapper(tool="zsh")
def parse_zsh(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring zsh... ")
    assert "zsh" in theme_data
    assert isinstance(theme_data["zsh"], dict)

    if "feats" in theme_data["zsh"]:
        assert isinstance(theme_data["zsh"]["feats"], list)
        feats = theme_data["zsh"]["feats"]
    else:
        feats = []

    if theme_data.get("wallpaper"):
        assert isinstance(theme_data["wallpaper"], dict)
        wallpaper_file = theme_data["wallpaper"]["file"]
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

    dest = os.path.join(destination_path, ".zshrc")

    for d in prompts_dict:
        if d in feats:
            if d == "run_pywal" and wallpaper_path is None:
                logger.error("Cannot add pywal to bash config, no wallpaper")
                continue
            if d == "neofetch":
                logger.warning("using fastfetch instead of neofetch")
            append_text(dest, prompts_dict[d])
    if theme_data['zsh'].get('zoxide'):
        append_text(dest, 'alias cd="z"\n')
        append_text(dest, 'eval "$(zoxide init zsh)"\n')

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
