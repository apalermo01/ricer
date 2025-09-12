import os
import sys
import logging
from ricer.ricer import (
    build_theme,
    move_to_dotfiles,
    prepare_paths,
)
from ricer.utils.args import get_user_config
import subprocess

logger = logging.getLogger(__name__)

def main():
    user_config = get_user_config()

    # if not user_config["theme"]:
    #     themes = sorted(os.listdir(user_config["themes_path"]))
    #     print("select a theme: ")
    #     for i, t in enumerate(themes):
    #         print(f"[{i}] {t}")
    #     idx = input()
    #     if not idx.isdigit() or int(idx) < 0 or int(idx) > len(themes):
    #         print("invalid theme index")
    #         sys.exit(1)
    #     user_config["theme"] = themes[int(idx)]

    theme_data = build_theme(user_config)
    theme_context = prepare_paths(user_config)

    move_to_dotfiles(user_config, theme_context, dry_run=False)
    if theme_data.hook_path:
        assert isinstance(theme_data.hook_path, list)
        for f in theme_data.hook_path:
            if '$THIS_THEME' in f:
                f = f.replace('$THIS_THEME', theme_context.theme_name)
            if '$THEME_NAME' in f:
                f = f.replace('$THEME_NAME', theme_context.theme_name)
            logger.warning(f"running theme build hook: {f}")
            hook_list = f.split(" ")
            args = hook_list[1:]
            script = os.path.expanduser(hook_list[0])
            subprocess.run(["bash", script, *args])


if __name__ == "__main__":
    main()
