import logging
import pprint
import os
import random
import shutil
from typing import Optional

import yaml

from ricer.tools import modules
from ricer.tools.wallpaper import move_wp_only
from ricer.utils.args import init_theme_config
from ricer.utils.colors import configure_colors
from ricer.utils.common import merge_dicts
from ricer.utils.theme_data import ThemeData
from ricer.utils.types import ThemeContext, UserConfig
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

RICER_CONFIG = {
    "order": [
        "colors",
        "apps",
        "i3",
        "polybar",
        "nvim",
        "tmux",
        "rofi",
        "picom",
        "fish",
        "bash",
        "zsh",
        "kitty",
        "alacritty",
        "fastfetch",
        "okular",
        "yazi",
        "sioyek",
        "dunst",
        "wallpaper",
    ],
}


def list_themes(user_config: UserConfig):
    theme_path = user_config.themes_path
    print(os.listdir(theme_path))


def prepare_paths(cfg: UserConfig) -> ThemeContext:
    print("********************** user config *********************")
    pprint.pp(cfg.model_dump())
    theme_name = cfg.theme
    theme_path = os.path.join(cfg.themes_path, theme_name)
    build_dir = os.path.join(theme_path, "build")
    template_path = cfg.template_path

    # make sure theme.yml exists
    theme_files = os.listdir(theme_path)

    if "theme.yml" in theme_files:
        theme_cfg = os.path.join(theme_path, "theme.yml")
    elif "theme.yaml" in theme_files:
        theme_cfg = os.path.join(theme_path, "theme.yaml")
    else:
        raise RuntimeError("theme.yml or theme.yaml not found")

    return ThemeContext(
        template_path=template_path,
        theme_path=theme_path,
        theme_name=theme_name,
        theme_cfg=theme_cfg,
        build_dir=build_dir,
    )


def build_theme(user_config: UserConfig) -> ThemeData:
    """Builds a suite of dotfiles based on config file"""

    print("************************ user config ************************")
    pprint.pp(user_config)
    theme_context = prepare_paths(user_config)
    build_dir = theme_context.build_dir
    if os.path.exists(build_dir):
        logger.warning(f"build directory exists. Clearing...")
        shutil.rmtree(build_dir)

    os.makedirs(build_dir)
    logger.info(f"created {build_dir}")

    # load config
    with open(theme_context.theme_cfg, "r") as f:
        _theme_data = yaml.safe_load(f)

    with open(user_config.before_override_path, "r") as f:
        default_dict = yaml.safe_load(f)

    with open(user_config.after_override_path, "r") as f:
        override_dict = yaml.safe_load(f)

    # have theme data override anything in default_dict
    theme_data_dict = merge_dicts(default_dict, _theme_data, warn = True)

    # override dict should overwrite anything set in the theme dict
    theme_data_dict = merge_dicts(theme_data_dict, override_dict, warn = True)

    theme_data: ThemeData = init_theme_config(theme_data_dict, user_config)

    install_script_path = os.path.join(
        theme_context.theme_path, "scripts", "install_theme.sh"
    )
    if os.path.exists(install_script_path):
        with open(install_script_path, "r") as f:
            theme_install_script = "\n".join(f.readlines())
    else:
        theme_install_script = "#!/usr/bin/env bash\n\n"
    tools_updated = {}

    res = modules["global"](
        theme_data=theme_data,
        theme_context=theme_context,
        user_config=user_config,
        install_script=theme_install_script,
        destination_path="",
    )


    # random wallpaper selection
    if theme_data.wallpaper and theme_data.wallpaper.random:
        wp_folder = os.path.join(theme_context.theme_path, "wallpapers")
        wp_file = random.choice(os.listdir(wp_folder))
        theme_data.wallpaper.file = wp_file


    theme_data_dict = theme_data.model_dump()
    print("******************* theme data *******************")
    pprint.pp(theme_data_dict)

    # make sure wallpaper is in the correct place 
    print("moving wallpaper...")
    if theme_data.wallpaper:
        move_wp_only(theme_data, theme_context.theme_path)

    # loop over all tools in the config
    # call the associated parser each time
    for tool in RICER_CONFIG["order"]:
        if tool in theme_data_dict and theme_data_dict[tool] is not None:
            logger.info("*" * 80)
            logger.info(f"*** {tool} " + "*" * (80 - len(tool) - 5))
            logger.info("*" * 80)
            res = modules[tool](
                theme_data=theme_data,
                theme_context=theme_context,
                user_config=user_config,
                install_script=theme_install_script,
            )

            theme_install_script = res.install_script
            theme_data = res.theme_data
            destination_path = res.destination_path

            tools_updated[tool] = {"destination_path": destination_path}

    # color templating for all modules that need it
    configure_colors(theme_context.theme_path, user_config)

    # write install script
    install_script_path = os.path.join(theme_context.build_dir, "install_theme.sh")
    with open(install_script_path, "w") as f:
        f.write(theme_install_script)
    return theme_data


def move_to_dotfiles(
    user_config: UserConfig, theme_context: ThemeContext, dry_run: Optional[bool] = True
):
    print("=" * 80)
    print("moving built theme to dotfiles")
    print("=" * 80)
    theme_name = theme_context.theme_name
    dotfiles_path = os.path.expanduser(
        os.path.join(user_config.dotfiles_path, theme_name)
    )
    build_path = os.path.expanduser(theme_context.build_dir)

    path_config = user_config.tools

    if os.path.exists(dotfiles_path):
        logger.info(f"removing {dotfiles_path}")
        if not dry_run:
            shutil.rmtree(dotfiles_path)

    if not dry_run:
        os.makedirs(dotfiles_path)
        os.mkdir(os.path.join(dotfiles_path, ".config"))
        logger.info(f"created {dotfiles_path}")

    # deal with global settings
    if "wsl" not in theme_name:
        profile_src = os.path.join(build_path, "global", ".profile")
        profile_dst = os.path.join(dotfiles_path, "profile")

        if not dry_run:
            shutil.copy2(profile_src, profile_dst)
        logger.info(f"{profile_src} -> {profile_dst}")

    for t in os.listdir(build_path):
        if t in ["colors", "wallpaper"] or not os.path.isdir(
            os.path.join(build_path, t)
        ):
            continue
        tool_config = path_config[t]
        logger.info(f"moving {t} to dotfiles repo...")
        dst_path = os.path.expanduser(
            os.path.join(dotfiles_path, tool_config.config_path)
        )

        src_path = os.path.expanduser(os.path.join(build_path, t))
        logger.info(f"src path = {src_path}")
        if not dry_run and not os.path.exists(dst_path):
            os.mkdir(dst_path)
        for f in os.listdir(src_path):
            src = os.path.join(src_path, f)
            dst = os.path.join(dst_path, f)
            logger.info(f"{src!r} -> {dst!r}")

            if not dry_run and os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)

            if not dry_run and os.path.isfile(src):
                shutil.copy2(src, dst)

    # copy install scripts
    install_src = os.path.join(build_path, "install_theme.sh")
    install_dst = os.path.join(dotfiles_path, ".config", "install_theme.sh")

    if not dry_run:
        shutil.copy2(install_src, install_dst)

    logger.info(f"{install_src} -> {install_dst}")
