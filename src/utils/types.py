from typing import Optional, TypedDict, TYPE_CHECKING




if TYPE_CHECKING:
    from src.tools.i3 import i3Config
    from src.tools.apps import AppsConfig
    from src.tools.bash import BashConfig
    from src.tools.colors import ColorsConfig
    from src.tools.dunst import DunstConfig
    from src.tools.fish import FishConfig
    from src.tools.nvim import NvimConfig
    from src.tools.okular import OkularConfig
    from src.tools.picom import PicomConfig
    from src.tools.polybar import PolybarConfig
    from src.tools.rofi import RofiConfig
    from src.tools.tmux import TmuxConfig
    from src.tools.wallpaper import WallpaperConfig
    from src.tools.yazi import YaziConfig
    from src.tools.zsh import ZshConfig


class ToolConfig(TypedDict):
    # path relative to the home directory where config files should go
    config_path: str
    jinja: Optional[bool]


class UserConfig(TypedDict):
    cfg_path: str
    override_path: str

    list_themes: Optional[bool] # if this is true, program should list themes then exit

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
