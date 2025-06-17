import logging
import configparser
import os
from src.utils.types import (
    BaseToolConfig,
    ThemeContext,
    ThemeData,
    ToolResult,
    UserConfig,
)
from src.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


class OkularConfig(BaseToolConfig):
    pass


@tool_wrapper(tool="okular")
def parse_okular(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring okular... ")
    assert "okular" in theme_data
    theme_path = theme_context["theme_path"]

    okular = configparser.ConfigParser()


    # ensure case gets preserved
    okular.optionxform = lambda option: option
    okular.read(
        theme_data["okular"].get("template_path", "./default_configs/okular/okularrc")
    )
    destination_dir = os.path.join(
        theme_path, "build", "okular", "okularrc"
    )

    if "apps" in theme_data:
        app_theme_name: str = theme_data["apps"]["name"]
        if 'UiSettings' not in okular:
            okular['UiSettings'] = {}
        okular['UiSettings']['ColorScheme'] = app_theme_name
        with open(destination_dir, "w") as f:
            okular.write(f)


    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
    return {"theme_data": theme_data, "install_script": install_script}
