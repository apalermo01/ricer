import glob
import logging
import os
import readline
import sys

import yaml

logger = logging.getLogger(__name__)


def complete(text, state):
    return (glob.glob(text + "*") + [None])[state]


def detect_install():
    if not os.path.exists(os.path.expanduser("~/.config/ricer/ricer.yml")):
        print("~/.config/ricer/ricer.yml does not exist. Initializing default paths...")
        install()


def install():

    readline.set_completer_delims(" \t\n;")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    pkgdir = sys.modules["ricer"].__path__[0]

    with open(os.path.join(pkgdir, "default_cfg_files", "ricer.yml")) as f:
        default_cfg = yaml.safe_load(f)

    print("Generating ricer.yml...")
    print("To configure ricer, you must set:")
    print("1. template_path (where the base config files live)")
    print("2. scripts_root: directory of user scripts. These will land in ~/Scripts")
    print(
        "3. dotfiles_path: where the built dotfiles should go. Symlink these directly to ~/.config"
    )
    print("4. themes_path: root directory for all theme configs.")
    print("")
    print("Do these paths have a common root? (y/n)")
    common_path = input()

    if common_path.lower()[0] == "y":
        common_path = True
        root_path = input("Enter the base directory: ")
        # root_path = "/home/alex/Documents/git/dotfiles"

        print(f"template folder name (enter nothing for the default: 'templates')")
        template_path = input()
        if len(template_path) == 0:
            template_path = os.path.join(root_path, "templates")
        else:
            template_path = os.path.join(root_path, template_path)

        print(f"scripts folder name: (enter nothing for the default: 'user_scripts')")
        scripts_path = input()
        if len(scripts_path) == 0:
            scripts_path = os.path.join(root_path, "user_scripts")
        else:
            scripts_path = os.path.join(root_path, scripts_path)

        print(f"built dotfiles path: (enter nothing for the default: 'built_themes')")
        dotfiles_path = input()
        if len(dotfiles_path) == 0:
            dotfiles_path = os.path.join(root_path, "built_themes")
        else:
            dotfiles_path = os.path.join(root_path, dotfiles_path)

        print(f"themes path: (enter nothing for the default: 'themes')")
        themes_path = input()
        if len(themes_path) == 0:
            themes_path = os.path.join(root_path, "themes")
        else:
            themes_path = os.path.join(root_path, themes_path)
    else:
        template_path = input("Enter the root directory for the template paths: ")
        scripts_path = input("Enter the root directory for the scripts path: ")
        dotfiles_path = input("Enter the root directory for the built themes path: ")
        themes_path = input("Enter the root directory for the theme config path: ")

    print("directory for wallpaper path. Leave blank for ~/Pictures/wallpapers")
    wallpaper_path = input()
    if len(wallpaper_path) == 0:
        wallpaper_path = "~/Pictures/wallpapers/"

    default_cfg["template_path"] = template_path
    default_cfg["scripts_root"] = scripts_path
    default_cfg["dotfiles_path"] = dotfiles_path
    default_cfg["themes_path"] = themes_path
    default_cfg["wallpaper_path"] = wallpaper_path

    __import__("pprint").pprint(default_cfg)
    ricer_root = os.path.expanduser("~/.config/ricer")
    if not os.path.exists(ricer_root):
        logger.info("making directory %s", ricer_root)
        os.makedirs(ricer_root)

    with open(os.path.join(ricer_root, "ricer.yml"), "w") as f:
        yaml.dump(default_cfg, f)

    logger.info("generating blank global-before.yml...")
    with open(os.path.join(ricer_root, "ricer-global-before.yml"), "w") as f:
        yaml.dump({}, f)

    logger.info("generating blank global-after.yml...")
    with open(os.path.join(ricer_root, "ricer-global-after.yml"), "w") as f:
        yaml.dump({}, f)
