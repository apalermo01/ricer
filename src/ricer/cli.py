import argparse
import os
import sys


def main() -> None:
    from ricer.switch import main as switch_main

    # from ricer.utils.generate_schema import main as schema_main

    if len(sys.argv) < 2:
        print("Usage: ricer switch [options]", file=sys.stderr)
        sys.exit(1)

    sys.argv.pop(1)

    switch_main()

    # elif sys.argv[1] == "schema":
    #     sys.argv.pop(1)
    #     schema_main()


if __name__ == "__main__":
    if not __package__:
        package_source_path = os.path.dirname(os.path.dirname(__file__))
        print(f"package source path = ", package_source_path)
        sys.path.insert(0, package_source_path)
    main()
