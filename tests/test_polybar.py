from src.ricer import build_theme
import os

args = {
    "cfg": "./tests/test_cfg.yml",
    "template_path": "./tests/templates/",
    "theme": "polybar",
}

theme_path = os.path.join(
    os.getcwd(),
    "tests",
    "themes",
    "polybar"
)

def test_polybar():
    build_theme(args)

    assert os.path.exists(
        os.path.join(theme_path, "build"),
    )
    assert os.path.exists(
        os.path.join(theme_path, "build", ".config", "polybar"),
    )
