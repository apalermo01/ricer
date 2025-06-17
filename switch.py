import os
import argparse
from src.ricer import (
    RICER_CONFIG,
    build_theme,
    list_themes,
    move_to_dotfiles,
    prepare_paths,
)
from src.utils.args import get_user_config


if __name__ == "__main__":

    user_config = get_user_config()

    if not user_config['theme']:
        themes = sorted(os.listdir(user_config['themes_path']))
        for i, t in enumerate(themes):
            print(f"[{i}] {t}")
        print("select a theme: ")
        idx = input()
        if not idx.isdigit() or int(idx) < 0 or int(idx) > len(themes):
            print("invalid theme index")
            exit
        user_config['theme'] = themes[int(idx)]

    build_theme(user_config)
    theme_context = prepare_paths(user_config)

    move_to_dotfiles(user_config, theme_context, dry_run=False) 
