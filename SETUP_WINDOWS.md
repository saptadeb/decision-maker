# Windows Setup Guide

Quick setup guide for running the Assistive Robot Decision-Making System on Windows.

## Prerequisites

- **Windows 10 or Windows 11**
- **Python 3.8 or higher** (Python 3.9+ recommended)

## Step 1: Check Python Installation

Open **PowerShell** or **Command Prompt** and run:

```powershell
python --version
```

You should see something like `Python 3.9.x` or higher.

### Don't have Python?

Download from [python.org](https://www.python.org/downloads/):
1. Download the latest Python 3.x installer
2. **Important:** Check "Add Python to PATH" during installation
3. Restart your terminal after installation

## Step 2: Navigate to Project Directory

```powershell
cd path\to\decision-maker
```

Example:
```powershell
cd C:\Users\YourName\code-extras\decision-maker
```

## Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs PyYAML (the only external dependency). Everything else is built into Python.

### Troubleshooting

If `pip` is not found, try:
```powershell
python -m pip install -r requirements.txt
```

If you get permission errors, try:
```powershell
pip install --user -r requirements.txt
```

## Step 4: Run the Application

### Main Simulator GUI (Recommended)
```powershell
python main.py
```

This launches the visual simulator with all 12 scenarios.

### Parameter Tuning GUI
```powershell
python tuning_gui.py
```

Adjust AI parameters using sliders and see results in real-time.

### Command-Line Comparison
```powershell
python test_comparison.py
```

Headless comparison with detailed metrics in the terminal.

## Common Issues

### Issue: "python is not recognized"
**Solution:** Python is not in your PATH. Reinstall Python and check "Add Python to PATH", or add it manually:
1. Search "Environment Variables" in Windows
2. Edit "Path" variable
3. Add Python installation directory (e.g., `C:\Python39`)

### Issue: tkinter not working
**Solution:** Reinstall Python and ensure "tcl/tk and IDLE" is checked during installation.

### Issue: "No module named 'yaml'"
**Solution:** PyYAML not installed. Run:
```powershell
pip install pyyaml
```

## Quick Test

To verify everything works:

```powershell
python test_comparison.py
```

You should see a comparison table with metrics. If this works, you're all set!

## Next Steps

1. **Learn the basics:** Read the main [README.md](README.md)
2. **Run scenarios:** Launch `python main.py` and click scenario buttons
3. **Tune parameters:** Try `python tuning_gui.py` to optimize settings
4. **Review metrics:** Check `docs/METRICS.md` for performance details

## Performance Tips for Windows

- Use **Windows Terminal** (from Microsoft Store) for better experience
- Run PowerShell as administrator if you encounter permission issues
- Close other applications if the GUI feels slow
- Python 3.10+ has better performance on Windows

## Uninstall

To remove the dependencies:
```powershell
pip uninstall pyyaml
```

To remove the project, just delete the `decision-maker` folder.

---

**Need help?** Check the main [README.md](README.md) or the [docs](docs/) folder for detailed information.
