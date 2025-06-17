import sys
import os
from pathlib import Path
from .switch import main as switch_main

def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "switch":
        switch_main()
    else:
        print("Usage: ricer switch [options]", file = sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
