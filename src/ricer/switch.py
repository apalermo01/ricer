import argparse
import logging
import os
import subprocess
import sys
from typing import Optional

from ricer.config import (
    RICER_DEFAULT_CFG,
    RICER_DEFAULT_OVERRIDE,
)
from ricer.ricer import build_theme, move_to_dotfiles, prepare_paths
from ricer.utils.args import get_user_config

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
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


def main():
    args = parse_args()
    user_config = get_user_config(args)

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
    return
    theme_context = prepare_paths(user_config)

    move_to_dotfiles(user_config, theme_context, dry_run=False)
    if theme_data.hook_path:
        assert isinstance(theme_data.hook_path, str)
        build_hook = os.path.expanduser(theme_data.hook_path)
        logger.warning(f"running theme build hook: {build_hook}")
        subprocess.run(["bash", build_hook, theme_context.theme_name])


if __name__ == "__main__":
    main()
