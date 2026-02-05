# Ubuntu Setup Guide

Quick setup guide for running the Assistive Robot Decision-Making System on Ubuntu Linux.

## Prerequisites

- **Ubuntu 20.04 LTS or higher** (also works on Debian-based distros)
- **Python 3.8 or higher** (usually pre-installed)

## Step 1: Check Python Installation

Open a terminal (`Ctrl+Alt+T`) and run:

```bash
python3 --version
```

You should see `Python 3.8.x` or higher.

### Install Python (if needed)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

## Step 2: Install tkinter

tkinter (GUI library) is not included by default on Ubuntu:

```bash
sudo apt update
sudo apt install python3-tk
```

## Step 3: Navigate to Project Directory

```bash
cd ~/path/to/decision-maker
```

Example:
```bash
cd ~/code-extras/decision-maker
```

## Step 4: Install Dependencies

```bash
pip3 install -r requirements.txt
```

This installs PyYAML (the only external dependency).

### Using Virtual Environment (Recommended)

For a cleaner setup, use a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

To deactivate later:
```bash
deactivate
```

### Troubleshooting

If you get "pip not found":
```bash
sudo apt install python3-pip
```

If you get permission errors:
```bash
pip3 install --user -r requirements.txt
```

## Step 5: Run the Application

### Main Simulator GUI (Recommended)
```bash
python3 main.py
```

This launches the visual simulator with all 12 scenarios.

### Parameter Tuning GUI
```bash
python3 tuning_gui.py
```

Adjust AI parameters using sliders and see results in real-time.

### Command-Line Comparison
```bash
python3 test_comparison.py
```

Headless comparison with detailed metrics in the terminal.

## Common Issues

### Issue: "No module named '_tkinter'"
**Solution:** tkinter not installed.
```bash
sudo apt install python3-tk
```

### Issue: "python: command not found"
**Solution:** Use `python3` instead of `python` on Ubuntu:
```bash
python3 main.py
```

Or create an alias in `~/.bashrc`:
```bash
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

### Issue: "No module named 'yaml'"
**Solution:** PyYAML not installed.
```bash
pip3 install pyyaml
```

### Issue: GUI is slow or unresponsive
**Solution:** Install Pillow for better GUI performance:
```bash
pip3 install pillow
```

## Quick Test

To verify everything works:

```bash
python3 test_comparison.py
```

You should see a comparison table with metrics. If this works, you're all set!

## Next Steps

1. **Learn the basics:** Read the main [README.md](README.md)
2. **Run scenarios:** Launch `python3 main.py` and click scenario buttons
3. **Tune parameters:** Try `python3 tuning_gui.py` to optimize settings
4. **Review metrics:** Check `docs/METRICS.md` for performance details

## Performance Tips for Ubuntu

- Use **GNOME Terminal** or **Terminator** for better experience
- Enable hardware acceleration if running in a VM
- Close unnecessary applications if GUI feels slow
- Use virtual environment to avoid dependency conflicts

## Shell Script (Optional)

Create a launcher script for convenience:

```bash
#!/bin/bash
# File: run.sh

echo "Assistive Robot Decision-Making System"
echo "======================================"
echo "1. Main Simulator GUI"
echo "2. Parameter Tuning GUI"
echo "3. Comparison Test"
echo ""
read -p "Choose option (1-3): " choice

case $choice in
    1) python3 main.py ;;
    2) python3 tuning_gui.py ;;
    3) python3 test_comparison.py ;;
    *) echo "Invalid option" ;;
esac
```

Make it executable:
```bash
chmod +x run.sh
./run.sh
```

## Uninstall

### Remove dependencies:
```bash
pip3 uninstall pyyaml
```

### Remove virtual environment (if used):
```bash
rm -rf venv
```

### Remove the project:
```bash
cd ..
rm -rf decision-maker
```

## Additional Packages (Optional)

For development or testing:

```bash
# Code formatting
pip3 install black

# Type checking
pip3 install mypy

# Better terminal output
pip3 install rich
```

---

**Need help?** Check the main [README.md](README.md) or the [docs](docs/) folder for detailed information.
