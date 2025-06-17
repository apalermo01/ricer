from . ricer import build_theme, list_themes
from . utils.args import get_user_config


def main():

    user_cfg = get_user_config()
    if user_cfg.get("themes"):
        list_themes(user_cfg)
        return

    if not user_cfg.get("theme"):
        print("No theme provided. Please pick a theme")
        list_themes(user_cfg)
        return

    build_theme(user_cfg)


if __name__ == "__main__":
    main()
