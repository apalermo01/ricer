import sys

from ricer.switch import main as switch_main
from ricer.utils.install import detect_install

# from ricer.utils.generate_schema import main as schema_main


def main() -> None:

    if len(sys.argv) < 2:
        print("Usage: ricer switch", file=sys.stderr)
        print("       ricer switch --theme [theme name]", file=sys.stderr)
        print("       ricer switch --theme [theme name] \\", file=sys.stderr)
        print("                    --root ~/Documents/git/dotfiles \\", file=sys.stderr)
        print(" ", file=sys.stderr)
        print("                    --cfg ~/.config/ricer/ricer.yml \\", file=sys.stderr)
        print(
            "                    --global-override-before ~/.config/ricer/ricer-global-before.yml \\",
            file=sys.stderr,
        )
        print(
            "                    --global-override-after ~/.config/ricer/ricer-global-after.yml \\",
            file=sys.stderr,
        )
        print(
            "                    --template-path ~/Documents/git/dotfiles/templates \\",
            file=sys.stderr,
        )
        print(
            "                    --themes-path ~/Documents/git/dotfiles/themes \\",
            file=sys.stderr,
        )
        sys.exit(1)

    sys.argv.pop(1)
    detect_install()
    switch_main()


if __name__ == "__main__":
    main()
