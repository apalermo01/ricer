from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from ricer.tools.apps import AppsConfig
    from ricer.tools.bash import BashConfig
    from ricer.tools.colors import ColorsConfig
    from ricer.tools.dunst import DunstConfig
    from ricer.tools.fish import FishConfig
    from ricer.tools.i3 import i3Config
    from ricer.tools.nvim import NvimConfig
    from ricer.tools.okular import OkularConfig
    from ricer.tools.picom import PicomConfig
    from ricer.tools.polybar import PolybarConfig
    from ricer.tools.rofi import RofiConfig
    from ricer.tools.tmux import TmuxConfig
    from ricer.tools.wallpaper import WallpaperConfig
    from ricer.tools.yazi import YaziConfig
    from ricer.tools.zsh import ZshConfig


class ToolConfig(TypedDict):
    # path relative to the home directory where config files should go
    config_path: str
    jinja: Optional[bool]


class UserConfig(TypedDict):
    cfg_path: str
    override_path: str

    list_themes: Optional[bool]  # if this is true, program should list themes then exit

    # where user-specific dotfiles live
    template_path: str

    # where the yaml files and additional files for each theme live
    themes_path: str

    # tools: sub-key = tool name (i3, bash, colors, etc.)
    tools: dict[str, ToolConfig]

    wallpaper_path: Optional[str]

    scripts_root: Optional[str]

    dotfiles_path: str

    # name of the theme to parse & build
    # TODO: handle case for parsing all themes
    theme: str


class ThemeContext(TypedDict):
    template_path: str
    theme_path: str
    theme_name: str
    theme_cfg: str
    build_dir: str


class FileAction(TypedDict):
    src: str
    dst: str


class BaseToolConfig(TypedDict):
    append: list[FileAction]
    template_path: Optional[str]


class ThemeData(TypedDict):
    font: Optional[str]
    hook_path: Optional[str]
    apps: "Optional[AppsConfig]"
    bash: "Optional[BashConfig]"
    colors: "Optional[ColorsConfig]"
    dunst: "Optional[DunstConfig]"
    fish: "Optional[FishConfig]"
    i3: "Optional[i3Config]"
    nvim: "Optional[NvimConfig]"
    okular: "Optional[OkularConfig]"
    picom: "Optional[PicomConfig]"
    polybar: "Optional[PolybarConfig]"
    rofi: "Optional[RofiConfig]"
    tmux: "Optional[TmuxConfig]"
    wallpaper: "Optional[WallpaperConfig]"
    yazi: "Optional[YaziConfig]"
    zsh: "Optional[ZshConfig]"


class ToolResult(TypedDict):
    # full theme config. Returned from each tool in case
    # a tool needs to conditionally edit the configuration for
    # another tool
    theme_data: ThemeData

    # text block representing a script to run when installing a theme
    install_script: str

    destination_path: str
