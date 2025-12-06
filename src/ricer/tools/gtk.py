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


    if theme_data.gtk.gtk_install_script:
        hook_path = os.path.join(theme_context.theme_path, "gtk", theme_data.gtk.gtk_install_script)

    else:
        assert gtk_theme in allowed_gtk_themes, f"unsupported gtk theme. Must be one of {allowed_gtk_themes}, got {gtk_theme}"
        pkgdir = sys.modules["ricer"].__path__[0]
        hook_path = os.path.join(pkgdir, "hooks", f"{gtk_theme}.sh")

    with open(hook_path, "r") as f:
        build_script = f.read()

    if not theme_data.gtk.gtk_install_script:
        build_scss_path = os.path.join(theme_context.build_dir, "gtk", f"{gtk_theme}.scss")
        build_script = build_script.replace(
            "TEMPLATE_DEFAULT_SCSS_PATH=",
            f"TEMPLATE_DEFAULT_SCSS_PATH={build_scss_path}"
        )
    install_script += f"\n#install gtk theme\n{build_script}\n"

    theme_name = gtk_theme 
    if theme_data.gtk.mode:
        theme_name = f"{theme_name}-{theme_data.gtk.mode}"
    overwrite_or_append_line(
        pattern="GTK_THEME=",
        replace_text=f"export GTK_THEME='{theme_name}'",
        dest=os.path.join(theme_context.theme_path, "build", "global", ".profile")
    )

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
