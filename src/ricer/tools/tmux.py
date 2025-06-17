from utils.types import BaseToolConfig, ThemeContext, ThemeData, ToolResult, UserConfig
from utils.wrapper import tool_wrapper
import logging
import os

logger = logging.getLogger(__name__)

class TmuxConfig(BaseToolConfig):
    pass

@tool_wrapper(tool="tmux")
def parse_tmux(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:
    logger.info("configuring tmux... ")
    # put the run command for tpm at the very bottom

    with open(os.path.join(destination_path, ".tmux.conf"), "a") as f:
        f.write("run '~/.tmux/plugins/tpm/tpm'")

    return {
        "theme_data": theme_data,
        "install_script": install_script,
        "destination_path": destination_path,
    }
    return {"theme_data": theme_data, "install_script": install_script}
