#!/usr/bin/env python3
"""
Todo Application Entry Point

This is the main entry point for the in-memory todo console application.
"""
import sys
import os
from pathlib import Path

# Add backend/src to the Python path so we can import the todo package
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from todo.cli import TodoCLI


def main():
    """Main entry point for the todo application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()