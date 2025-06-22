import logging
import os

from ricer.utils.common import overwrite_or_append_line
from ricer.utils.theme_data import NvimConfig, ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="nvim")
def parse_nvim(
    theme_data: "ThemeData",
    theme_context: "ThemeContext",
    user_config: "UserConfig",
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring nvim... ")
    assert theme_data.nvim

    nvim_config = theme_data.nvim
    theme_path = theme_context.theme_path

    if nvim_config.colorscheme:
        _configure_colorscheme(nvim_config, theme_path)

    if nvim_config.nvchad_colorscheme:
        _configure_nvchad_colorscheme(nvim_config, theme_path)

    if nvim_config.nvchad_separator:
        _configure_nvchad_separator(nvim_config, theme_path)

    font = os.environ.get("FONT") or theme_data.font or None

    if font:
        _configure_font(font, theme_path)
    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )


def _configure_colorscheme(nvim_config: NvimConfig, theme_path: str):
    if isinstance(nvim_config.colorscheme, str):
        colorscheme: str = nvim_config.colorscheme
        colorscheme_path: str = os.path.join(theme_path, "build", "nvim", "init.lua")

    # TODO: need to test this
    else:
        assert nvim_config.colorscheme
        assert isinstance(nvim_config.colorscheme, dict)
        assert nvim_config.colorscheme["colorscheme"]

        colorscheme: str = nvim_config.colorscheme["colorscheme"]
        colorscheme_path: str = os.path.join(
            theme_path, "build", "nvim", nvim_config.colorscheme["file"]
        )
        if not os.path.exists(os.path.split(colorscheme_path)[0]):
            os.makedirs(os.path.split(colorscheme_path)[0])

    if not os.path.exists(colorscheme_path):
        raise ValueError(
            f"could not find neovim config file {colorscheme_path} when parsing colorscheme"
        )

    cmd: str = f'vim.cmd.colorscheme("{colorscheme}")'

    overwrite_or_append_line(
        pattern="vim.cmd.colorscheme(", replace_text=cmd, dest=colorscheme_path
    )


def _configure_font(font: str, theme_path: str):
    logger.info("Configuring font")
    path = os.path.join(theme_path, "build", "nvim", "init.lua")

    if not os.path.exists(path):
        logger.error(f"Cannot parse font - expected to find {path}")
        return
    c = font.replace(" ", "\ ")
    cmd = f"vim.cmd([[set guifont={c}]])"
    overwrite_or_append_line(
        pattern="vim.cmd([[set guifont", replace_text=cmd, dest=path
    )


def _configure_nvchad_colorscheme(nvim_config: NvimConfig, theme_path: str):
    colorscheme = nvim_config.nvchad_colorscheme
    pattern = 'theme = "'
    text = f'    theme = "{colorscheme}",'
    path = os.path.join(theme_path, "build", "nvim", "lua", "chadrc.lua")
    if not os.path.exists(path):
        raise FileNotFoundError(
            """
            could not find chadrc.lua to configure colorscheme.
            Are you using nvchad? 
            You must pass 'template_dir': 'default_configs/nvim/' 
            in the theme file for this to work."""
        )

    overwrite_or_append_line(dest=path, pattern=pattern, replace_text=text)


def _configure_nvchad_separator(nvim_config: NvimConfig, theme_path: str):
    separator = nvim_config.nvchad_separator
    if not separator:
        return

    pattern: str = 'separator_style = "'
    text: str = f'       separator_style = "{separator}",'
    path: str = os.path.join(theme_path, "build", "nvim", "lua", "chadrc.lua")

    if not os.path.exists(path):
        raise FileNotFoundError(
            """
            could not find chadrc.lua to configure colorscheme.
            Are you using nvchad? 
            You must pass 'template_dir': 'default_configs/nvim/' 
            in the theme file for this to work."""
        )
    overwrite_or_append_line(dest=path, pattern=pattern, replace_text=text)
