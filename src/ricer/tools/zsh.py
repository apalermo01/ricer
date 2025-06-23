import logging
import os
from textwrap import dedent

from ricer.utils.common import append_text
from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

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
    direnv: Optional[bool]

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
        "neofetch": "fastfetch\n",
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
<<<<<<< HEAD

    if theme_data.zsh.zoxide:
||||||| parent of d4943d6 (small changes to zsh)

    if theme_data['zsh'].get('zoxide'):
=======
    
    if theme_data['zsh'].get('env'):
        assert 'env' in theme_data['zsh']
        assert isinstance(theme_data['zsh']['env'], dict)
        for k in theme_data['zsh']['env']:
            append_text(dest, f"export {k}=\"{theme_data['zsh']['env'][k]}\"\n")
    if theme_data['zsh'].get('zoxide'):
>>>>>>> d4943d6 (small changes to zsh)
        append_text(dest, 'alias cd="z"\n')
        append_text(dest, 'eval "$(zoxide init zsh)"\n')

    if theme_data.zsh.direnv:
        append_text(dest, 'eval "$(direnv hook zsh)"\n')

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
