"""
Main launcher for the Assistive Robot Decision-Making System.

This now launches the GUI instead of console simulations.
Run this file to start the visual simulator!
"""

import sys
import os

# Ensure the GUI module can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main as gui_main


def main():
    """Launch the GUI."""
    print("Launching Assistive Robot Decision-Making System GUI...")
    gui_main()


if __name__ == "__main__":
    main()

