import logging
import os
from textwrap import dedent
from typing import Literal, Optional
from src.utils.types import (
    BaseToolConfig,
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)
from src.utils.wrapper import tool_wrapper
from src.utils.common import append_text

logger = logging.getLogger(__name__)

class FishConfig(BaseToolConfig):
    feats: Optional[list[Literal['cowsay_fortune', 'neofetch', 'fastfetch', 'run_pywal', 'git_onefetch']]]

@tool_wrapper(tool="fish")
def parse_fish(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring fish... ")
    assert theme_data['fish']
    feats: list[str] = theme_data['fish'].get('feats', [])
    
    if theme_data.get('wallpaper'):
        wallpaper_file = theme_data["wallpaper"]["file"]
        wallpaper_path = os.path.expanduser(f"~/Pictures/wallpapers/{wallpaper_file}")
    else:
        wallpaper_path = ""

    prompts_dict = {
        "cowsay_fortune": ("fortune | cowsay -rC \n"),
        "neofetch": "fastfetch\n",
        "fastfetch": "fastfetch\n",
        "run_pywal": f"wal -n -e -i {wallpaper_path} > /dev/null \n",
        "git_onefetch": dedent(
            """

            function show_onefetch
                if test -d .git
                    onefetch
                end
            end
            
            function cd
                builtin cd $argv
                show_onefetch
            end
            """
        ),
    }
    dest = os.path.join(destination_path, "config.fish")
    for d in prompts_dict:
        if d in feats:
            if d == "run_pywal" and wallpaper_path is None:
                logger.error("Cannot add pywal to fish config, no wallpaper")
                continue
            if d == "neofetch":
                logger.warning("using fastfetch instead of neofetch")
            append_text(dest, prompts_dict[d])

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
    return {"theme_data": theme_data, "install_script": install_script}
