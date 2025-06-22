from src.ricer import build_theme
import os

args = {
    "cfg": "./tests/test_cfg.yml",
    "template_path": "./tests/templates/",
    "theme": "color_test_pywal_i3",
}

theme_path = os.path.join(os.getcwd(), "tests", "themes", "color_manual")


def test_build_pywal_colors():
    build_theme(args)

    assert os.path.exists(
        os.path.join(theme_path, "build"),
    )
    assert os.path.exists(
        os.path.join(theme_path, "pallet.png"),
    )
