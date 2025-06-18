# everything needed to generate a porject configuration
import argparse
import os

import yaml

from ricer.config import RICER_DEFAULT_CFG, RICER_DEFAULT_OVERRIDE, RICER_DEFAULT_SCRIPTS_PATH, RICER_DEFAULT_WALLPAPER_PATH
from ricer.utils.types import ThemeData, UserConfig
import logging

logger = logging.getLogger(__name__)
def sub_variables(d: dict, s: dict) -> dict:
    for key in d:
        if isinstance(d[key], dict):
            d[key] = sub_variables(d[key], s)
        elif isinstance(d[key], str):
            for varname in s:
                if varname in d[key]:
                    d[key] = d[key].replace(varname, s[varname])
    return d

def init_theme_config(theme_data: ThemeData, user_config: UserConfig):
    sub_dict = {
        '$THIS_THEME': os.path.join(user_config['themes_path'], user_config['theme'])
    }

    theme_data_cleaned: ThemeData = sub_variables(theme_data, sub_dict)
    
    
    return theme_data_cleaned

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
        "--global-override", required=False, default=os.path.expanduser(RICER_DEFAULT_OVERRIDE)
    )

    parser.add_argument(
        "--template-path", required=False
    )
    parser.add_argument(
        "--themes-path", required=False
    )
    parser.add_argument("--theme", required=False)

    args = parser.parse_args()
    return args


def get_user_config() -> UserConfig:
    """get all the variables we need for the project"""
    args = parse_args()
    cfg_path = os.path.expanduser(args.cfg)

    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)

    if not cfg.get("wallpaper_path"):
        cfg["wallpaper_path"] = os.path.expanduser(RICER_DEFAULT_WALLPAPER_PATH)

    if not cfg.get('scripts_root'):
        cfg['scripts_root'] = os.path.expanduser(RICER_DEFAULT_SCRIPTS_PATH)
    

    user_config: UserConfig = {
        'cfg_path': cfg_path,
        'override_path': os.path.expanduser(args.global_override),
        'list_themes': cfg.get('themes'),
        'template_path': os.path.expanduser(cfg['template_path']),
        'themes_path': os.path.expanduser(cfg['themes_path']),
        'wallpaper_path': os.path.expanduser(cfg['wallpaper_path']),
        'scripts_root': os.path.expanduser(cfg['scripts_root']),
        'dotfiles_path': os.path.expanduser(cfg['dotfiles_path']),
        'theme': args.theme,
        'tools': cfg['tools']
    }

    print("user config = ", user_config)
    return user_config
