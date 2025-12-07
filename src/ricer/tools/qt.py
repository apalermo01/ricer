"""
use kvantum to set qt theme
- make a theme config in ~/.config/kvantum/<theme_name>
- update ~/.config/Kvantum/kvantum.kvconfig
- make sure correct env vars are sourced in ~/.profile

TODO: icons?
"""

import logging
import os
import shutil
from textwrap import dedent

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="qt")
def parse_qt(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring qt... ")
    assert theme_data.qt

    assert theme_data.qt.method in [
        "default",
        "manual",
    ], f"method must be one of 'default' or 'manual'. Got {theme_data.qt.method}"

    if theme_data.qt.method == "default":
        assert theme_data.qt.kv_theme
        _handle_default(destination_path, theme_data)

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )


def _handle_default(destination_path: str, theme_data: ThemeData):
    # option 1: pick a default kvantum theme
    kv_default_themes = [
        "KvAdapta",
        "KvAdaptaDark",
        "KvAmbiance",
        "KvAmbience",
        "KvArc",
        "KvArcDark",
        "KvBeige",
        "KvBlender",
        "KvBrown",
        "KvCurves",
        "KvCurves3d1",
        "KvCurvesLight",
        "KvCyan",
        "KvDark",
        "KvDarkRed",
        "KvFlat",
        "KvFlatLight",
        "KvFlatRed",
        "KvGnome",
        "KvGnomeAlt",
        "KvGnomish",
        "KvGray",
        "KvMojave",
        "KvMojaveLight",
        "KvMojaveMixed",
        "KvMojaveMixed1",
        "KvOxygen",
        "KvRoughGlass",
        "KvSimplicity",
        "KvSimplicityDark",
        "KvSimplicityDarkLight",
        "KvSimplicityTurquoise",
        "KvYaru",
        "KvantumAlt",
    ]

    errmsg = f"Invalid kv theme. Must be one of the themes found here: https://github.com/tsujan/Kvantum/tree/master/Kvantum/themes/colors. Got {theme_data.qt.kv_theme} If you think one is missing or there is a typo, please open an issue"


    assert theme_data.qt.kv_theme in kv_default_themes, errmsg

    content = dedent(
        f"""
        [General]
        theme={theme_data.qt.kv_theme}
        """
    )
    with open(os.path.join(destination_path, "kvantum.kvconfig"), "w") as f:
        f.write(content)

    # re-arrange template directory
    dest_files = os.listdir(destination_path)
    assert len(dest_files) in [1, 2], "Expected 1 or 2 files in build path"

    if len(dest_files) == 2:
        logger.info("2 config files for kvantum detected")
        colors_file = [e for e in dest_files if "kvantum" not in e][0]
        logger.info(f"detected colors file: {colors_file}")
        colors_folder = os.path.join(destination_path, theme_data.qt.kv_theme)
        os.mkdir(colors_folder)
        logger.info(f"created colors folder: {colors_folder}")
        src = os.path.join(destination_path, colors_file)
        dst = os.path.join(
            destination_path, colors_folder, f"{theme_data.qt.kv_theme}.kvconfig"
        )
        shutil.move(src, dst)
        logger.info(f"{src} -> {dst}")
