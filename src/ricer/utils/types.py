from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ToolConfig(BaseModel):
    config_path: str
    jinja: Optional[bool] = None


class ThemeContext(BaseModel):
    template_path: str
    theme_path: str
    theme_name: str
    theme_cfg: str
    build_dir: str


class UserConfig(BaseModel):
    cfg_path: str
    before_override_path: str
    after_override_path: str
    template_path: str
    themes_path: str
    dotfiles_path: str
    theme: str
    tools: dict[str, ToolConfig]
    list_themes: Optional[bool] = None
    wallpaper_path: Optional[str] = None
    scripts_root: Optional[str] = None
