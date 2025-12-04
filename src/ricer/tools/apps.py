
import logging
import os
import subprocess

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)



@tool_wrapper(tool="apps")
def parse_apps(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring apps... ")
    assert theme_data.apps
    apps_config = theme_data.apps
    app_theme_name = apps_config.name

    # run any predefined scripts that download theme files and put them
    # in the right place
    installs_path = os.path.join(theme_context.theme_path, "apps")
    for file in os.listdir(installs_path):
        subprocess.call(os.path.join(installs_path, file))

    # Now parse through the theme configuration, figure out what we have, and
    # add the correct calls to the theme install script
    for key in apps_config.requires:
        if key == "qt.colorscheme":
            install_script += f"""
if command -b {apps_config.requires[key]}; then
    {apps_config.requires[key]} {app_theme_name}
else
    echo "WARNING: {apps_config.requires[key]} not found"
fi
            """
            # install_script += f"if command -v {apps_config.requires[key]}; then\n"
            # install_script += f"    {apps_config.requires[key]} {app_theme_name}\n"
            # install_script += f"fi\n\n"
        elif key in ["kvantum", "gtk"]:
            logger.warning(f"{key} support is in progress, skipping")
            continue
        else:
            logger.error(f"{key} is unsupported, skipping")
            continue

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
