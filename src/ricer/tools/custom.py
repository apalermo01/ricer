import logging
import os
import shutil

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


# @tool_wrapper(tool="custom")
def parse_custom(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    # destination_path: str,
    install_script: str,
):
    tool_config = getattr(theme_data, "custom")

    strip_slash = lambda s: s.lstrip(os.path.sep)
    for custom_tool in tool_config:
        name = custom_tool.name
        cfg_folder = custom_tool.cfg_folder

        src_path = os.path.join(theme_context.theme_path, custom_tool)
        destination_path = os.path.join(theme_context.build_dir, cfg_folder)

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            logger.info(f"created {destination_path}")

        for root, _, files in os.walk(src_path):
            subfolder = root.replace(src_path, "")
            folder = os.path.join(destination_path, strip_slash(subfolder))

            if not os.path.exists(folder):
                os.makedirs(folder)

            for file in files:
                src = os.path.join(root, strip_slash(file))
                dst = os.path.join(
                    destination_path, strip_slash(subfolder), strip_slash(file)
                )
                shutil.copy2(src, dst)
                logger.info(f"{src} -> {dst}")

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
