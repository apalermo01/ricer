from ricer.utils.types import  ThemeContext, UserConfig
from ricer.utils.theme_data import ThemeData, ToolResult
import logging
import os
import shutil


logger = logging.getLogger(__name__)


def parse_global(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:

    logger.info("Loading global settings...")
    assert theme_context.theme_path
    assert theme_context.template_path
    theme_path = theme_context.theme_path
    template_dir = theme_context.template_path
    if "wsl" not in theme_path:
        parse_profile(theme_data, template_dir, theme_path)
    else:
        logger.info("wsl detected, not parsing profile")
    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path
    )


def parse_profile(config: ThemeData, template_dir: str, theme_path: str):
    if config.global_settings:
        if config.global_settings.template_path:
            profile_src = config.global_settings.template_path
        else:
            profile_src = os.path.join(template_dir, "profile")
    else:
        profile_src: str = os.path.join(template_dir, "global", ".profile")

    profile_dst: str = os.path.join(theme_path, "build", "global", ".profile")

    # set up profile
    global_path = os.path.join(theme_path, "build", "global")
    if not os.path.exists(global_path):
        os.mkdir(global_path)
    shutil.copy2(src=profile_src, dst=profile_dst)
    logger.info(f"{profile_src} -> {profile_dst}")
