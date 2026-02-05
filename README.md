# Assistive Robot Decision-Making System

> An interactive AI decision-making simulator for assistive robotics with visual GUI, parameter tuning, and performance metrics.

## Platform Setup

Choose your operating system for detailed setup instructions:

| Platform | Setup Guide | Quick Command |
|----------|-------------|---------------|
| **Windows** | **[Windows Setup](docs/setup/windows.md)** | `python main.py` |
| **Ubuntu/Linux** | **[Ubuntu Setup](docs/setup/ubuntu.md)** | `python3 main.py` |

## Quick Start

```bash
python main.py  # Launches the visual simulator GUI
```

Then click any scenario button to see the AI in action!

---

## Installation and Setup

**Platform-Specific Guides:**
- **[Windows Setup Guide](docs/setup/windows.md)** - Recommended for Windows users
- **[Ubuntu/Linux Setup Guide](docs/setup/ubuntu.md)** - Recommended for Ubuntu users

### Quick Setup (All Platforms)

**Prerequisites:** Python 3.8+ and pip

```bash
# Install dependencies
pip install -r requirements.txt

# Ubuntu users: Install tkinter first
sudo apt install python3-tk
```

### Run the Application

**Option 1: Main Simulator GUI** (Recommended)
```bash
python main.py
```
This launches the visual simulator with all 12 preset scenarios. Use this to:
- Test your AI implementation
- Switch between custom and reference solutions
- Run all scenarios at once
- Compare performance metrics

**Option 2: Parameter Tuning GUI**
```bash
python -m gui.tuning_window
```
This launches the parameter tuning interface where you can:
- Adjust AI parameters using sliders
- Test different configurations in real-time
- Export tuned parameters to implementation files

**Option 3: Command-Line Comparison**
```bash
python -m tests.test_comparison
```
This runs a headless comparison between your custom implementation and the reference solution, showing detailed metrics in the terminal.

---

## Overview

This project explores **AI decision-making** through a simulated assistive robot. The robot must balance competing priorities: helping users, managing its battery, and ensuring safety.

**Key Concept**: There's no single "correct" AI behavior — the system demonstrates how different value judgments affect decision outcomes.

## Implementation

The robot's "brain" can be customized by editing **only 2 files** in the `implementation/` directory:

1. **`implementation/scoring.py`** — Define how the robot evaluates each action
2. **`implementation/decision.py`** — Implement the logic to choose the best action

---

## The Robot's World

### State (What the robot knows)
- **Battery Level**: 0-100 (critical below 20)
- **Current Task**: idle, helping, navigating
- **User Need**: urgency level (0-3)
- **Environment**: distances to user/charger, time pressure

### Actions (What the robot can do)
- **HELP_USER** — Assist the user (costs 15% battery, reduces urgency by 1)
- **RECHARGE** — Go to charging station (gains 50% battery, takes 2 time steps)
- **WAIT** — Do nothing (costs 2% battery, **always** increases urgency by 1)
- **CALL_FOR_HELP** — Request human assistance (ends scenario, costs 5% battery)

### Tradeoffs (The hard part!)
- Should it help when battery is low?
- When is it okay to make the user wait?
- Is efficiency more important than safety?

**These choices define the AI's "personality".**

---

## Getting Started

### 1. Launch the Visual Simulator

```bash
python main.py
```

This opens a GUI where you can:
- Run 12 different preset scenarios
- Toggle between custom implementation and the reference solution
- See real-time decision-making output
- Compare performance instantly

### 2. Edit the implementation files

Open `implementation/scoring.py` and `implementation/decision.py`. Follow the TODO comments.

### 3. Test the AI

**In the GUI:**
- Click any scenario button to run it with the custom implementation
- Use the toggle to switch between "Custom Implementation" and "Reference Solution"
- Click "Run All Scenarios" to test all 12 scenarios at once
- Results are **deterministic** - same scenario = same output every time

### 4. Compare implementations

Use the toggle button to switch between implementations and see how they differ on the same scenarios!

---

## File Structure

```
decision-maker/
├── main.py              # GUI launcher (run this!)
├── README.md            # This file
├── requirements.txt     # Python dependencies
│
├── gui/                 # GUI modules
│   ├── main_window.py   # Visual simulator interface
│   └── tuning_window.py # Parameter tuning interface
│
├── implementation/      # AI implementation (edit these files)
│   ├── decision.py      # Decision-making logic
│   └── scoring.py       # Action evaluation & scoring
│
├── core/                # Simulation framework (deterministic)
│   ├── state.py         # Robot and environment state
│   ├── actions.py       # Available actions
│   ├── simulator.py     # Simulation engine
│   ├── constraints.py   # Safety constraints
│   └── metrics.py       # Performance metrics system
│
├── solutions/           # Reference implementations
│   ├── solution.py      # Advanced AI example
│   ├── solution_decision.py
│   ├── solution_scoring.py
│   └── README.md
│
├── tests/               # Testing and comparison
│   └── test_comparison.py
│
├── docs/                # Documentation
│   ├── COMPARISON.md    # Comparative analysis
│   ├── METRICS.md       # Metrics documentation
│   └── setup/           # Platform-specific guides
│       ├── windows.md   # Windows setup
│       └── ubuntu.md    # Ubuntu/Linux setup
│
├── config/              # Configuration files
│   └── default_params.yml
│
└── output/              # Generated files (auto-created)
    ├── gui_metrics.json
    └── gui_results.json
```

**Edit files in `implementation/` to customize the AI behavior.**

**Note:** The `solutions/` folder contains an optimized reference implementation. Try your own approach first, then use the GUI toggle to compare behaviors!

---

## Analysis Questions

After implementing the AI:

1. What values does the robot prioritize?
2. When does the AI make surprising choices?
3. How would this design translate to a **real** assistive robot?
4. What ethical concerns arise when AI makes decisions for vulnerable users?

---

## Success Criteria

There's no single "correct" answer! An AI implementation is successful if:

- It completes scenarios without breaking constraints
- The decision logic is explainable and traceable
- It handles edge cases (low battery + high urgency)
- It behaves meaningfully differently from the reference solution
- The tradeoffs are well-justified

**Bonus Challenge:** Can a custom implementation outperform the reference solution on all 12 scenarios?

---

## Visual Simulator Features

### Interactive GUI
- **12 Preset Scenarios**: From "Balanced Start" to "Critical Battery" situations
- **Toggle Switch**: Instantly switch between custom implementation and the reference solution
- **Real-time Output**: Watch decisions unfold step-by-step with color-coded results
- **Batch Testing**: Run all scenarios at once with one click

### Scenario Types
- **Balanced Start**: Standard operating conditions
- **Low Battery Crisis**: Managing critical battery with urgent user
- **High Urgency**: Critical user needs with various battery levels
- **Efficiency Tests**: Long-running scenarios testing resource management
- **Edge Cases**: Close to charger, close to user, multiple competing needs

### Example Output (from GUI)

```
==================================================================
  Scenario: Low Battery Crisis
==================================================================
Initial State: [Step 0] Battery=25%, Task=idle, Urgency=MEDIUM

Step 1: [Step 0] Battery=25%, Task=idle, Urgency=MEDIUM
  -> Decision: HELP_USER
    Helped user (urgency 2->1)

Step 2: [Step 1] Battery=10%, Task=helping, Urgency=LOW
  -> Decision: RECHARGE
    Recharged battery (10->60%)
    
[SUCCESS] User need fully resolved.
```

### Deterministic Behavior
- **Same scenario = Same results** every time
- **No randomness** - fully predictable for testing
- **Consistent comparisons** between implementations

---

## Comparing Implementations

The GUI makes comparison easy:

### In the Visual Simulator:

1. **Run with custom implementation** (default mode)
   - Click "Run All Scenarios" to test all 12 scenarios
   - Observe the decisions and outcomes

2. **Toggle to Reference Solution** 
   - Click the big toggle button at the top
   - Button turns orange when using reference solution
   - Run the same scenarios again

3. **Compare Results**
   - See which implementation completes more scenarios
   - Compare decision strategies
   - Analyze battery management approaches

### Export Results:
- Click "Export Results" to save performance data
- Results saved to `output/gui_results.json` and `output/gui_metrics.json`
- Analyze detailed metrics offline

See `docs/COMPARISON.md` for behavioral analysis tips.

---

## Troubleshooting

### Common Issues

**"No module named 'yaml'" or similar import errors**
```bash
# Make sure you installed dependencies
pip install -r requirements.txt
```

**"No module named 'tkinter'" (Linux only)**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

**GUI window doesn't appear or crashes**
- Make sure you're using Python 3.8 or higher
- On Windows, tkinter comes with Python by default
- On Mac, tkinter comes with Python by default
- On Linux, you need to install python3-tk separately (see above)

**Files not found or import errors**
- Make sure you're running commands from the project root directory (decision-maker/)
- Check that all folders (core/, implementation/, solutions/) are present

**Custom implementation not working**
- Check that `implementation/decision.py` and `implementation/scoring.py` exist
- Make sure they contain the required functions: `choose_action()` in decision.py and `score_action()` in scoring.py
- Try using the parameter tuning GUI (`python -m gui.tuning_window`) to generate valid implementation files

**Parameters not loading in tuning GUI**
- The tuning GUI will use hardcoded defaults if `config/default_params.yml` is missing
- This is normal and expected - you can still use all features
