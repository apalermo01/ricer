import sys
from ricer.switch import main as switch_main
from ricer.utils.generate_schema import main as schema_main

def main() -> None:

    if len(sys.argv) < 2:
        print("Usage: ricer switch [options] or ricer schema", file = sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "switch":
        sys.argv.pop(1)
        switch_main()
    
    if sys.argv[1] == 'schema':
        sys.argv.pop(1)
        schema_main()

if __name__ == '__main__':
    main()
