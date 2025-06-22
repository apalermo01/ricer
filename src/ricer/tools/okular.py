import configparser
import logging
import os

from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="okular")
def parse_okular(
    theme_data: "ThemeData",
    theme_context: "ThemeContext",
    user_config: "UserConfig",
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring okular... ")
    assert theme_data.okular
    theme_path = theme_context.theme_path

    okular = configparser.ConfigParser()

    # ensure case gets preserved
    okular.optionxform = lambda option: option
    if theme_data.okular.template_path:
        template_path = theme_data.okular.template_path
    else:
        template_path = "./default_configs/okular/okularrc"
    okular.read(template_path)
    destination_dir = os.path.join(theme_path, "build", "okular", "okularrc")

    if theme_data.apps:
        app_theme_name: str = theme_data.apps.name
        if "UiSettings" not in okular:
            okular["UiSettings"] = {}
        okular["UiSettings"]["ColorScheme"] = app_theme_name
        with open(destination_dir, "w") as f:
            okular.write(f)

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
