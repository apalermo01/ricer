from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


class FileAction(BaseModel):
    src: str
    dst: str


class BaseToolConfig(BaseModel):
    append: list[FileAction] = []
    overwrite: list[FileAction] = []
    template_path: Optional[str] = None


class AlacrittyConfig(BaseToolConfig):
    pass


class AppsConfig(BaseToolConfig):
    provides: dict
    requires: dict
    name: str


class BashConfig(BaseToolConfig):
    feats: list[
        Literal["cowsay_fortune", "neofetch", "fastfetch", "run_pywal", "git_onefetch"]
    ] = []


class ColorsConfig(BaseToolConfig):
    method: Literal["manual", "pywal"]


class DunstConfig(BaseToolConfig):
    font_size: Optional[int] = None


class FastfetchConfig(BaseToolConfig):
    pass


class FishConfig(BaseToolConfig):
    feats: list[
        Literal["cowsay_fortune", "neofetch", "fastfetch", "run_pywal", "git_onefetch"]
    ] = []


class GlobalConfig(BaseToolConfig):
    pass


class i3Config(BaseToolConfig):
    font: Optional[str] = None
    font_size: Optional[int] = 11

class KittyConfig(BaseToolConfig):
    pass

class NvimConfig(BaseToolConfig):
    colorscheme: Optional[str | dict] = None
    nvchad_colorscheme: Optional[str] = None
    nvchad_separator: Optional[str] = None


class OkularConfig(BaseToolConfig):
    UiSettings: Optional[dict] = {}


class PicomConfig(BaseToolConfig):
    pass


class PolybarConfig(BaseToolConfig):
    bars: Optional[list[str]] = []
    start_script: Optional[str] = None


class RofiConfig(BaseToolConfig):
    pass

class SioyekConfig(BaseToolConfig):
    pass 

class TmuxConfig(BaseToolConfig):
    pass


class WPValidator(BaseModel):
    @model_validator(mode='after')
    def check_file(self):
        data = self.model_dump()
        if data['file'] is None and data['random'] == False:
            raise ValueError("file required if not using a random wallpaper")
        return self

class WallpaperConfig(WPValidator):
    method: Literal["feh", "hyprpaper", "None"] = "None"
    file: str | None = None
    random: bool = False


class YaziConfig(BaseToolConfig):
    dark: Optional[str]
    light: Optional[str]


class ZshConfig(BaseToolConfig):
    feats: list[
        Literal["cowsay_fortune", "neofetch", "fastfetch", "run_pywal", "git_onefetch"]
    ] = []
    zoxide: Optional[bool]
    direnv: Optional[bool]


class ThemeData(BaseModel):
    font: Optional[str] = None
    font_size: Optional[int] = None
    hook_path: Optional[list] = None

    alacritty: Optional[AlacrittyConfig] = None
    apps: Optional[AppsConfig] = None
    bash: Optional[BashConfig] = None
    colors: Optional[ColorsConfig] = None
    dunst: Optional[DunstConfig] = None
    fastfetch: Optional[FastfetchConfig] = None
    fish: Optional[FishConfig] = None
    global_settings: Optional[GlobalConfig] = None
    i3: Optional[i3Config] = None
    kitty: Optional[KittyConfig] = None
    nvim: Optional[NvimConfig] = None
    okular: Optional[OkularConfig] = None
    picom: Optional[PicomConfig] = None
    polybar: Optional[PolybarConfig] = None
    rofi: Optional[RofiConfig] = None
    sioyek: Optional[SioyekConfig] = None
    tmux: Optional[TmuxConfig] = None
    wallpaper: Optional[WallpaperConfig] = None
    yazi: Optional[YaziConfig] = None
    zsh: Optional[ZshConfig] = None


class ToolResult(BaseModel):
    theme_data: ThemeData
    install_script: str
    destination_path: str
