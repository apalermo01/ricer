# everything needed to generate a porject configuration
import argparse
import os
import sys
import pprint
import yaml
import pprint

from ricer.config import (
    RICER_DEFAULT_CFG,
    RICER_DEFAULT_OVERRIDE,
    RICER_DEFAULT_SCRIPTS_PATH,
    RICER_DEFAULT_WALLPAPER_PATH,
)
from ricer.utils.types import UserConfig
from ricer.utils.theme_data import ThemeData

import logging

logger = logging.getLogger(__name__)
def sub_variables(d: dict, s: dict) -> dict:
    for entry in d:
        if isinstance(d[entry], dict):
            d[entry] = sub_variables(d[entry], s)
        elif isinstance(d[entry], str):
            for varname in s:
                if varname in d[entry]:
                    d[entry] = d[entry].replace(varname, s[varname])
    return d


def init_theme_config(theme_data_dict: dict[str, str | dict], user_config: UserConfig) -> ThemeData:
    sub_dict = {
        "$THIS_THEME": os.path.join(user_config.themes_path, user_config.theme)
    }
    theme_data_cleaned = sub_variables(theme_data_dict, sub_dict)
    args = {k: theme_data_cleaned.get(k) for k in ThemeData.model_fields}
    theme_data = ThemeData(
        **args
    )

    return theme_data


def parse_args():
    """parse cli args"""
    parser = argparse.ArgumentParser()
    # list themes
    parser.add_argument(
        "--themes",
        action=argparse.BooleanOptionalAction,
        required=False,
        help="list available themes",
    )

    # config path
    parser.add_argument(
        "--cfg", required=False, default=os.path.expanduser(RICER_DEFAULT_CFG)
    )

    parser.add_argument(
        "--global-override",
        required=False,
        default=os.path.expanduser(RICER_DEFAULT_OVERRIDE),
    )

    parser.add_argument("--template-path", required=False)
    parser.add_argument("--themes-path", required=False)
    parser.add_argument("--theme", required=False)

    args = parser.parse_args()
    return args


def get_user_config() -> UserConfig:
    """get all the variables we need for the project"""
    args = parse_args()
    cfg_path = os.path.expanduser(args.cfg)

    if not os.path.exists(cfg_path):
        logger.warning(f"config at {cfg_path} not found. auto-generating...")
        os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
        import sys, shutil
        pkgdir = sys.modules['ricer'].__path__[0]
        shutil.copy(os.path.join(pkgdir, "default_cfg_files", "ricer.yml"), cfg_path)

    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)

    if not cfg.get("wallpaper_path"):
        cfg["wallpaper_path"] = os.path.expanduser(RICER_DEFAULT_WALLPAPER_PATH)

    if not cfg.get("scripts_root"):
        cfg["scripts_root"] = os.path.expanduser(RICER_DEFAULT_SCRIPTS_PATH)
    
    themes_path = os.path.expanduser(cfg["themes_path"])
    if not args.theme:
        themes = sorted(os.listdir(themes_path))
        for i, t in enumerate(themes):
            print(f"[{i}] {t}")
        idx = input()
        print("select a theme: ")
        if not idx.isdigit() or int(idx) < 0 or int(idx) > len(themes):
            print("invalid theme index")
            sys.exit(1)
        theme = themes[int(idx)]
    else:
        theme = args.theme

    if not os.path.exists(args.global_override):
        logger.warning(f"{args.global_override} not found. Auto-generating...")
        os.makedirs(os.path.dirname(args.global_override), exist_ok=True)
        import sys, shutil
        pkgdir = sys.modules['ricer'].__path__[0]
        shutil.copy(os.path.join(pkgdir, "default_cfg_files", "ricer-global.yml"), cfg_path)
    user_config = UserConfig(
        cfg_path = cfg_path,
        override_path = os.path.expanduser(args.global_override),
        list_themes = cfg.get("themes"),
        template_path = os.path.expanduser(cfg["template_path"]),
        themes_path = themes_path,
        wallpaper_path = os.path.expanduser(cfg["wallpaper_path"]),
        scripts_root = os.path.expanduser(cfg["scripts_root"]),
        dotfiles_path = os.path.expanduser(cfg["dotfiles_path"]),
        theme = theme,
        tools = cfg["tools"],
    )

    return user_config
