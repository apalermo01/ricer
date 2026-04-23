import json
import logging
import os
import fileinput

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="hyprland")
def parse_hyprland(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring hyprland...")

    parse_colors(theme_data, destination_path, theme_context.theme_path)
    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )


def parse_colors(theme_data: ThemeData, dest: str, theme_path: str):
    """{{ colorname(transparency) }} -> rgba(....)"""

    with open(os.path.join(theme_path, "colors", "colorscheme.json")) as f:
        colors = json.load(f)
    for f in os.listdir(dest):
        path = os.path.join(dest, f)
        with fileinput.input(files=path, inplace = True) as hypr_config_file:
            for line in hypr_config_file:
                if '{{' in line and '}}' in line:
                    line = _run_template(line, colors)
                print(line, end='')


def _run_template(line: str, colors: dict):
    newchars = ''

    max_iter, i = 10, 0
    while '{{' in line and i <= max_iter:
        newchars += line[:line.index('{{')] 
        color_id = line.split('{{')[1].split('}}')[0].strip()

        if '(' in color_id and ')' in color_id:
            key = color_id.split('(')[0]
            trans = color_id.split('(')[1].split(')')[0]
            new_color = f'rgba({colors.get(key, "#000000")[1:]}{trans})'
        else:
            key = color_id.split('(')[0]
            new_color = f'rgb({colors.get(key, "#000000")[1:]})'
        newchars += new_color

        new_start_idx = line.index('}}') + 2
        if new_start_idx >= len(line):
            break
        line = line[new_start_idx:]

        i += 1

    if len(line) >= 0:
        newchars += line

    return newchars

    
