import logging
import os
import shutil

from src.utils.types import (
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)

logger = logging.getLogger(__name__)


def parse_global(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:

    logger.info("Loading global settings...")
    theme_path = theme_context["theme_path"]
    template_dir = theme_context["template_path"]
    if "wsl" not in theme_path:
        parse_profile(theme_data, template_dir, theme_path)
    else:
        logger.info("wsl detected, not parsing profile")

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }


def parse_profile(config: ThemeData, template_dir: str, theme_path: str):
    if "global" in config:
        profile_src: str = config["global"].get(
            "template_dir", os.path.join(template_dir, "profile")
        )
    else:
        profile_src: str = os.path.join(template_dir, "global", ".profile")
    print("theme path = ", theme_path)
    print("template_dir = ", template_dir)
    profile_dst: str = os.path.join(theme_path, "build", "global", ".profile")

    # set up profile
    os.mkdir(os.path.join(theme_path, "build", "global"))
    shutil.copy2(src=profile_src, dst=profile_dst)
    logger.info(f"{profile_src} -> {profile_dst}")
