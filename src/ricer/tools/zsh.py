import logging
import os
from textwrap import dedent

from ricer.utils.common import append_text
from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)



@tool_wrapper(tool="zsh")
def parse_zsh(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring zsh... ")
    assert theme_data.zsh

    feats = theme_data.zsh.feats

    if theme_data.wallpaper:
        wallpaper_file = theme_data.wallpaper.file
        wallpaper_path = os.path.expanduser(f"~/Pictures/wallpapers/{wallpaper_file}")
    else:
        wallpaper_path = ""

    prompts_dict = {
        "cowsay_fortune": ("fortune | cowsay -r \n"),
        "neofetch": "if command -v fastfetch >/dev/null 2>&1\nthen\n\tfastfetch\nfi\n",
        "fastfetch": "if command -v fastfetch >/dev/null 2>&1\nthen\n\tfastfetch\nfi\n",
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

    if theme_data.zsh.zoxide:
        append_text(dest, """
if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init zsh)"
    alias cd="z" 
fi
""")

    if theme_data.zsh.direnv:
        append_text(dest, """
if command -v direnv >/dev/null 2>&1; then
    eval "$(direnv hook zsh)"
fi
""")

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
