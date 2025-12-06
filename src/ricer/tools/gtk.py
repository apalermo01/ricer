import logging
import os
import sys

from ricer.utils.common import overwrite_or_append_line
from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper

logger = logging.getLogger(__name__)


@tool_wrapper(tool="gtk")
def parse_gtk(
    theme_data: ThemeData,
    theme_context: ThemeContext,
    user_config: UserConfig,
    destination_path: str,
    install_script: str,
) -> ToolResult:

    logger.info("configuring gtk theme...")
    assert theme_data.gtk
    assert theme_data.gtk.gtk_theme

    allowed_gtk_themes = ['adw-gtk3']
    gtk_theme = theme_data.gtk.gtk_theme
    if not theme_data.gtk.mode:
        mode = ''
    else:
        mode = theme_data.gtk.mode

    hook_mapping = {
        'adw-gtk3': 'adw-gtk3.sh',
        'adw-gtk3-dark': 'adw-gtk3.sh'
    }

    pkgdir = sys.modules["ricer"].__path__[0]

    assert gtk_theme in allowed_gtk_themes, f"unsupported gtk theme. Must be one of {allowed_gtk_themes}, got {gtk_theme}"

    hook_path = os.path.join(pkgdir, "hooks", hook_mapping[gtk_theme])
    with open(hook_path, "r") as f:
        build_script = f.read()

    logger.info(f"template_path={theme_context.template_path}")
    build_scss_path = os.path.join(theme_context.build_dir, "gtk", f"{gtk_theme}.scss")
    build_script = build_script.replace(
        "TEMPLATE_DEFAULT_SCSS_PATH=",
        f"TEMPLATE_DEFAULT_SCSS_PATH={build_scss_path}"
    )
    install_script += f"\n#install gtk theme\n{build_script}\n"

    overwrite_or_append_line(
        pattern="GTK_THEME=",
        replace_text=f"export GTK_THEME='{gtk_theme}-{mode}'",
        dest=os.path.join(theme_context.theme_path, "build", "global", ".profile")
    )

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
