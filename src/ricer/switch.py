import os
import sys
from ricer.ricer import (
    build_theme,
    move_to_dotfiles,
    prepare_paths,
)
from ricer.utils.args import get_user_config
import subprocess

def main():
    user_config = get_user_config()

    if not user_config['theme']:
        themes = sorted(os.listdir(user_config['themes_path']))
        print("select a theme: ")
        for i, t in enumerate(themes):
            print(f"[{i}] {t}")
        idx = input()
        if not idx.isdigit() or int(idx) < 0 or int(idx) > len(themes):
            print("invalid theme index")
            sys.exit(1)
        user_config['theme'] = themes[int(idx)]

    theme_data = build_theme(user_config)
    theme_context = prepare_paths(user_config)

    move_to_dotfiles(user_config, theme_context, dry_run=False) 
    if 'hook_path' in theme_data:
        assert isinstance(theme_data['hook_path'], str)
        subprocess.run(['bash', theme_data['hook_path'], theme_context['theme_name']])

if __name__ == "__main__":
    main()
