#!/usr/bin/env python
import os
from pathlib import Path

from api.cli import cli

if __name__ == "__main__":
    directory = Path(__file__).parent
    os.chdir(directory)
    cli()
