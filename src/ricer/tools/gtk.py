import logging
import os
import sys

from ricer.utils.common import overwrite_or_append_line
from ricer.utils.theme_data import ThemeData, ToolResult
from ricer.utils.types import ThemeContext, UserConfig
from ricer.utils.wrapper import tool_wrapper
from textwrap import dedent
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

    """
    How to make this easily tweakable? 

    1. Make a script that compiles any given gtk theme
    2. Provide a template for editing scss files 

    scss files may change theme-by-theme, so maybe I should make a template folder 
    for each gtk theme that ricer supports, make a build script, and provide a starter file for people to mess with. 

    Challenge here is that the template will now be defined by ricer itself, not the user-provided template folder. 

    How should this be modeled? 

    key for theme name. This will look up the build script 
    for now, this will just be adw-gtk3. Maybe have the script live in <project_root>/scripts/install-adw-gtk3.sh? This will be the contents of the additions to install_script below. 

    Actually, maybe a better option is to write the snippet to install_script. Then, it will download the source (if needed) and recompile with the changes any time the theme installed (install_theme.sh is put in ~/.config/install_theme.sh and is intended to be run by the same utility that runs stow on the dotfiles directory.)

    It feels a little hacky to put a substantial portion of the logic in a python module like this. What if I put the script hooks to append in ~/.config/ricer? Problem with that is that implies that it can be changed by the end user, which this really shouldn't be. Maybe set up a hooks directory in the package and source the hook content from that. It could follow a pattern like: 

    pkgdir = sys.modules["ricer"].__path__[0]
    with open(os.path.join(pkgdir, "hooks", f"{gtk_theme_name}.sh") "r") as f:
        content = f.read()

    install_script += f"\n#install gtk theme\n{content}\n"

    So that handles the theme installation / compilation. What about customizing the scss? How about this: in the README, link to the _default.scss that users are expected to be able to tweak, instruct them to download that file and rename it to "<gtk_theme_name>.scss" and place it in their templates/gtk directory. In a different feature I'll enable bootstrapping of specific template files, which will include gtk themes. 
    """

    pkgdir = sys.modules["ricer"].__path__[0]
    gtk_theme = theme_data.gtk.gtk_theme

    assert gtk_theme in ['adw-gtk3']

    hook_path = os.path.join(pkgdir, "hooks", f"{gtk_theme}.sh")
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
        replace_text="export GTK_THEME='adw-gtk3'",
        dest=os.path.join(theme_context.theme_path, "build", "global", ".profile")
    )

    return ToolResult(
        theme_data=theme_data,
        install_script=install_script,
        destination_path=destination_path,
    )
