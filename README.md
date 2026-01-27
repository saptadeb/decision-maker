# Assistive Robot Decision-Making AI Workshop

## Overview

This workshop explores **AI decision-making** through a simulated assistive robot. The robot must balance competing priorities: helping users, managing its battery, and ensuring safety.

**Key Learning Goal**: There's no single "correct" AI behavior — students make value judgments about what matters most.

---

## Your Task

You will implement the robot's "brain" by editing **only 2 files** in the `implementation/` directory:

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
- **HELP_USER** — Assist the user (costs energy)
- **RECHARGE** — Go to charging station (takes time)
- **WAIT** — Do nothing (low cost, but urgency may increase)
- **CALL_FOR_HELP** — Request human assistance (gives up)

### Tradeoffs (The hard part!)
- Should it help when battery is low?
- When is it okay to make the user wait?
- Is efficiency more important than safety?

**Your choices define the AI's "personality".**

---

## Getting Started

### 1. Run the baseline simulation

```bash
python main.py
```

This runs with placeholder AI logic. The robot will make poor decisions!

### 2. Edit the implementation files

Open `implementation/scoring.py` and `implementation/decision.py`. Follow the TODO comments.

### 3. Test your AI

Run the simulation again and observe how behavior changes.

### 4. Try different scenarios

Edit the scenarios in `main.py` or create new ones.

---

## File Structure

```
decision-maker/
├── main.py              # Main simulation runner
├── README.md            # This file
│
├── implementation/      # AI implementation (edit these files)
│   ├── decision.py      # Decision-making logic
│   └── scoring.py       # Action evaluation & scoring
│
├── core/                # Simulation framework
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
├── docs/                # Documentation
│   ├── COMPARISON.md    # Comparative analysis
│   └── METRICS.md       # Metrics documentation
│
└── output/              # Generated files (auto-created)
    ├── my_metrics.json
    └── solution_metrics.json
```

**Edit files in `implementation/` to customize the AI behavior.**

**Note:** The `solutions/` folder contains an example implementation. Try your own approach first before looking at it!

---

## Discussion Questions

After implementing your AI:

1. What values did your robot prioritize?
2. When did your AI make surprising choices?
3. How would you design this for a **real** assistive robot?
4. What ethical concerns arise when AI makes decisions for vulnerable users?

---

## Success Criteria

There's no "correct" answer! Your AI is successful if:

- It completes scenarios without breaking constraints
- You can explain *why* it makes each decision
- It behaves differently from your classmates' AIs
- You can justify the tradeoffs you encoded

---

## Example Output

```
=== Scenario: Urgent User with Low Battery ===
Step 1: Battery=25, Urgency=HIGH → HELP_USER (risky but needed)
Step 2: Battery=10, Urgency=MEDIUM → RECHARGE (safety first)
Step 3: Battery=70, Urgency=MEDIUM → HELP_USER (safe to help now)
Result: User helped successfully!
```

### Performance Metrics

After running scenarios, you'll see quantitative metrics:

```
PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Metric                    Score    Grade
Success Rate              100.0%     A
Battery Efficiency         85.0%     B
Urgency Response           90.0%     A
Risk Management            95.0%     A
Overall Score              93.5%     A
```

See `METRICS.md` for detailed explanation of each metric.

---

## Comparing Solutions

After implementing your AI, compare quantitatively:

```bash
# Step 1: Run your implementation (saves metrics)
python main.py

# Step 2: Run solution (automatically compares)
python solutions/solution.py
```

You'll see:
- Side-by-side performance metrics
- Which approach excels at what
- Overall winner across 6 dimensions

See `COMPARISON.md` for behavioral analysis and `METRICS.md` for metrics explanation.

---

## Advanced Extensions (Optional)

- Add new actions (e.g., MOVE_CLOSER, REQUEST_PERMISSION)
- Introduce uncertainty (actions may fail)
- Create multi-robot scenarios (coordination)
- Build a GUI to visualize decisions
- Implement learning from past scenarios

---

## Credits

Designed for middle school AI workshop — decision-making without ML complexity.

