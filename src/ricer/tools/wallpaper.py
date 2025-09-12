import logging
import os
import shutil
import random

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext

logger = logging.getLogger(__name__)




def parse_wallpaper(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    # theme_apply_script: str,
    install_script: str,
    **kwargs,
) -> ToolResult:
    logger.info("configuring wallpaper... ")

    assert theme_data.wallpaper
    method = theme_data.wallpaper.method
    theme_path = theme_context.theme_path


    if method == "feh":
        feh_theme(
            theme_data,
            theme_path,
        )
    elif method == "hyprpaper":
        hyprpaper_theme(
            theme_data,
            theme_path,
        )
    elif method == "None":
        move_wp_only(
            theme_data,
            theme_path,
        )
    else:
        raise ValueError(
            "Invalid method. Expected one of {allowed_methods} but got {method}"
        )

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=""
    )


def move_wp_only(
    config: ThemeData,
    theme_path: str,
):

    logger.info("moving wallpaper")

    assert config.wallpaper
    assert config.wallpaper.file

    wallpaper_path: str = config.wallpaper.file

    if config.wallpaper.random:
        wallpaper_path = os.path.join(theme_path, "wallpapers", wallpaper_path)

    # if just the filename was given, look in the project's wallpaper folder:
    elif "/" not in wallpaper_path:
        wallpaper_path = os.path.join(".", "wallpapers", wallpaper_path)

    wallpaper_dest: str = os.path.expanduser(
        f"~/Pictures/wallpapers/{wallpaper_path.split('/')[-1]}"
    )

    if not os.path.exists(os.path.expanduser("~/Pictures/wallpapers/")):
        os.makedirs(os.path.expanduser("~/Pictures/wallpapers/"))

    if not os.path.exists(wallpaper_path):
        logger.warning(f"could not find wallpaper {wallpaper_path}. It may already be in ~/Pictures/wallpapers")
    else:
        shutil.copy2(src=wallpaper_path, dst=wallpaper_dest)
        logger.info(f"copied {wallpaper_path} to {wallpaper_dest}")


def feh_theme(config: ThemeData, theme_path: str):
    logger.info("setting up feh")


    assert config.wallpaper
    assert config.wallpaper.file

    # random wallpaper: look in theme_path / wallpapers and pick one
    if config.wallpaper.random:
        wp_folder: str = os.path.join(theme_path, "wallpapers")

        wallpaper_path: str = os.path.join(wp_folder, config.wallpaper.file)

    else:
        wallpaper_path: str = config.wallpaper.file

        # if just the filename was given, look in the project's wallpaper folder:
        if "/" not in wallpaper_path:
            wallpaper_path = os.path.join(".", "wallpapers", wallpaper_path)

    wallpaper_dest: str = os.path.expanduser(
        f"~/Pictures/wallpapers/{wallpaper_path.split('/')[-1]}"
    )

    if not os.path.exists(os.path.expanduser("~/Pictures/wallpapers/")):
        os.makedirs(os.path.expanduser("~/Pictures/wallpapers/"))

    if not config.i3:
        raise KeyError(
            "This parser is only configured to work with i3 if feh is used. "
            + "Please add it to the theme's config"
        )

    text: str = f"exec_always feh --bg-fill {wallpaper_dest}"

    # TODO: copy text to additional i3 config file
    path: str = os.path.join(theme_path, "build", "i3", "config")

    with open(path, "r") as f:
        lines = f.readlines()

    if text not in lines:
        logger.info(f"{text} not found in theme's i3 config, appending")
        with open(path, "a") as f:
            f.write(text)

    logger.info(f"added {text} to i3 config")

    move_wp_only(config, theme_path)

    # write wallpaper cmd to a script
    # cmd_text: str = f"feh --bg-fill {wallpaper_dest}"
    # theme_apply_script += f"{cmd_text}\n"

    # wp_script_path = os.path.join(theme_path, "build", "theme_scripts")
    # if not os.path.exists(wp_script_path):
    #     os.makedirs(wp_script_path)
    # with open(os.path.join(wp_script_path, "wp.sh"), "w") as f:
    #     f.write("#!/bin/sh\n")
    #     f.write(cmd_text)
    #
    # # os.chmod(os.path.join(wp_script_path, "wp.sh"), stat.S_IRWXO)
    # logger.info(f"wrote {cmd_text} to wp script")
    # logger.info(f"theme apply script = ")
    # logger.info(theme_apply_script)
    # return config, theme_apply_script


def hyprpaper_theme(
    config: ThemeData,
    theme_path: str,
):
    assert config.wallpaper
    wallpaper_path: str = config.wallpaper.file

    hyprpaper_path: str = os.path.join(theme_path, "build", "hypr")
    if not os.path.exists(hyprpaper_path):
        os.makedirs(hyprpaper_path)

    hyprpaper_path = os.path.join(hyprpaper_path, "hyprpaper.conf")
    # hyprpaper_path: str = os.path.expanduser("~/.config/hypr/hyprpaper.conf")

    # if just the filename was given, look in the project's wallpaper folder:
    if "/" not in wallpaper_path:
        wallpaper_path = os.path.join(".", "wallpapers", wallpaper_path)

    wallpaper_dest: str = os.path.expanduser(
        f"~/Pictures/wallpapers/{wallpaper_path.split('/')[-1]}"
    )

    if not os.path.exists(os.path.expanduser("~/Pictures/wallpapers/")):
        os.makedirs(os.path.expanduser("~/Picutres/wallpapers/"))

    if not config.hyprland:
        raise KeyError(
            "This parser is only configured to work with hyprland if "
            + "hyprpaper is used. Please add it to the theme's config"
        )

    with open("./default_configs/monitors.txt", "r") as f:
        monitors = f.readlines()

    with open(hyprpaper_path, "w") as f:
        f.write(f"preload = {wallpaper_dest}\n")
        for m in monitors:
            f.write(f"wallpaper = {m[:-1]}, {wallpaper_dest}\n")

    logger.info(f"wrote wallpaper info to {hyprpaper_path}")

    shutil.copy2(src=wallpaper_path, dst=wallpaper_dest)

    logger.info(f"copied {wallpaper_path} to {wallpaper_dest}")
