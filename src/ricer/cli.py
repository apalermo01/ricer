import sys
from ricer.switch import main as switch_main

def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "switch":
        sys.argv.pop(1)
        switch_main()

    else:
        print("Usage: ricer switch [options]", file = sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
