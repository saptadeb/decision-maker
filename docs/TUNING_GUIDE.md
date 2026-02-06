# Parameter Tuning Cheatsheet

> **Goal:** Understand each parameter to create an AI that outperforms the reference solution!

---

## The Challenge

Can you tune the parameters to make the custom implementation beat the reference solution in **all 12 scenarios**?

The reference solution wins with careful balance. Your job: find the right parameter values through experimentation and understanding.

---

## Battery Management Parameters

### Recharge Threshold (10-70%)

**What it controls:** When the robot decides "my battery is getting low, I should recharge"

**How it works:**
- The robot compares its current battery to this threshold
- If below threshold (and conditions are right), it recharges
- Modified by Risk Tolerance setting

**Effects of different values:**

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Low (20-30%)** | Recharges rarely, helps more | Risk of battery emergencies |
| **Medium (35-45%)** | Balanced approach | Good balance of safety & helping |
| **High (50-65%)** | Recharges frequently | Slower response to users |

**Hint:** The reference solution is proactive about battery management. When does it start thinking about recharging?

**Think about:**
- Helping costs 15% battery
- Recharging restores 50% battery
- What threshold allows 2-3 helps before recharging?

---

### Critical Battery (5-25%)

**What it controls:** The "emergency mode" battery level

**How it works:**
- Below this level, special emergency rules activate
- Robot becomes very cautious about helping
- May call for help if battery AND urgency are both critical

**Effects of different values:**

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Very Low (5-10%)** | Rarely enters emergency mode | Maximum helping opportunities |
| **Low (12-18%)** | Moderate emergency threshold | Balanced safety margin |
| **High (20-25%)** | Enters emergency mode early | May be overly cautious |

**Hint:** Look at the implementation code. There's a hardcoded check for `battery >= 10`. How does this interact with your Critical Battery setting?

**Special Note:** The "Empty Battery Recovery" scenario starts at 5% battery with no urgency. What should the robot do? What happens if Critical Battery is too high?

**Think about:**
- When is calling for help appropriate vs. recharging?
- What's the TRUE point of no return for battery?

---

### Help Min Battery (10-40%)

**What it controls:** Minimum battery required to help a user

**How it works:**
- Robot won't help if battery is below this level
- Prevents helping when it would drain battery dangerously low
- Works with urgency checks

**Effects of different values:**

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Low (10-20%)** | Helps even with low battery | Risky! May strand robot |
| **Medium (22-28%)** | Safe helping threshold | Enough for help + buffer |
| **High (30-40%)** | Only helps with good battery | May delay urgent help |

**Hint:** Helping costs 15% battery. If you help at X%, you'll have (X - 15)% remaining. What's a safe "remaining" amount?

**Think about:**
- After helping, can the robot still reach a charger?
- What if there's a second urgent request right after?

---

### Proactive Recharge (Enabled/Disabled)

**What it controls:** Whether to recharge during "quiet times"

**How it works:**
- When ENABLED: Recharges when urgency is 0, even if above threshold
- When DISABLED: Only recharges when below threshold
- Key to avoiding getting caught with low battery

**Effects:**

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Disabled** | Reactive charging only | May get caught unprepared |
| **Enabled** | Charges when safe to do so | Always prepared for urgency |

**Hint:** The reference solution is described as "proactive." What does that tell you?

**Think about:**
- Is it better to wait until you NEED to charge, or charge when you CAN?
- What happens if urgency spikes while battery is moderate?

---

## Priority Weights

### Safety Weight (0.0-1.0)

**What it controls:** How much the robot values its own safety (battery management)

**How it works:**
- Multiplied with safety scores from actions
- Higher weight = more conservative decisions
- Competes with helpfulness weight

**Effects of different values:**

| Setting | Behavior | Philosophy |
|---------|----------|------------|
| **Low (0.2-0.35)** | Risk-tolerant, helps aggressively | "Users first, battery second" |
| **Medium (0.4-0.5)** | Balanced priorities | "Safety and helping are equal" |
| **High (0.6-0.8)** | Very conservative | "Battery safety is paramount" |

**Hint:** The reference solution adapts its priorities based on context. When urgency is high, does it prioritize safety or helpfulness?

**Think about:**
- If both weights are 0.5, decisions are perfectly balanced
- Lower safety weight means more willing to take battery risks
- What ratio reflects "help users unless truly dangerous"?

---

### Helpfulness Weight (0.0-1.0)

**What it controls:** How much the robot values helping users quickly

**How it works:**
- Multiplied with helpfulness scores from actions
- Higher weight = more responsive to user needs
- Competes with safety weight

**Effects of different values:**

| Setting | Behavior | Philosophy |
|---------|----------|------------|
| **Low (0.2-0.4)** | Self-preservation focus | "I help when it's safe" |
| **Medium (0.5-0.6)** | User-focused | "Users are my priority" |
| **High (0.65-0.8)** | Highly responsive | "Help users at almost any cost" |

**Hint:** This is an *assistive* robot. What should its primary purpose be?

**Think about:**
- These weights don't need to sum to 1.0, but their RATIO matters
- A ratio of 0.3:0.7 is very different from 0.5:0.5
- How should an assistive robot balance self-preservation vs. helping?

---

## Risk Strategy

### Risk Tolerance (Conservative / Medium / Aggressive)

**What it controls:** Overall risk-taking philosophy

**How it works:**
- Modifies the Recharge Threshold by a multiplier:
  - **Conservative:** 1.5× (recharges much earlier)
  - **Medium:** 1.0× (recharges at exact threshold)
  - **Aggressive:** 0.7× or 0.8× (pushes battery lower)

**Effects:**

| Setting | Multiplier | Example (Threshold=40%) | Philosophy |
|---------|------------|-------------------------|------------|
| **Conservative** | 1.5× | Recharges at 60% | "Always maintain high battery" |
| **Medium** | 1.0× | Recharges at 40% | "Trust the thresholds" |
| **Aggressive** | 0.7-0.8× | Recharges at 28-32% | "Use battery efficiently" |

**Hint:** The reference solution is described as "sophisticated" and "strategic." Does it play it safe, or does it trust its logic?

**Think about:**
- If your other parameters are well-tuned, can you trust them?
- Aggressive doesn't mean reckless if the base thresholds are sound
- Which uses battery most efficiently?

---

## Experimental Strategy

### Phase 1: Understand the Scenarios

Run all scenarios with default settings and observe:
- Which scenarios fail? Why?
- Which scenarios succeed but barely?
- What patterns do you see?

**Key scenarios to watch:**
- **Empty Battery Recovery:** Starts at 5% battery, no urgency
- **Low Battery Crisis:** 25% battery, medium urgency
- **Close to User:** 30% battery, critical urgency, user is close

### Phase 2: Fix Critical Issues

Some scenarios might FAIL with default settings. Why?
- Is Critical Battery set too high?
- Is the robot calling for help when it should recharge?
- Check the "Empty Battery Recovery" scenario carefully!

### Phase 3: Optimize Efficiency

Once all scenarios PASS, optimize for better metrics:
- Battery efficiency: Are you recharging too often?
- Urgency response: Are you helping quickly enough?
- Risk management: Are you too conservative or too aggressive?

### Phase 4: Compare with Solution

Use the main GUI to compare your implementation with the reference solution:
- How many scenarios do you win?
- What's your overall score vs. the solution?
- Can you beat it in ALL scenarios?

---

## Learning Principles

### The Battery Math

**Key numbers to remember:**
- HELP_USER costs: **-15% battery**
- RECHARGE gains: **+50% battery**
- WAIT costs: **-2% battery**

**Important calculations:**
```
Safe Help Margin = Help Min Battery - Help Cost
                 = X - 15

After Helping = Current Battery - 15
```

**Example:**
- If Help Min Battery = 25%, you can help when battery ≥ 25%
- After helping: 25% - 15% = 10% remaining
- Is 10% enough to reach a charger safely?

### The Urgency Scale

- **0:** No user need (safe to recharge, wait)
- **1:** Low urgency (can delay briefly)
- **2:** Medium urgency (should respond soon)
- **3:** Critical urgency (emergency! respond NOW!)

**The reference solution is particularly aggressive at urgency 3.**

### The Balance Question

What should an assistive robot prioritize?

**Too Conservative:**
- Spends too much time recharging
- Slow to respond to urgent needs
- Poor battery efficiency (wastes time)

**Too Aggressive:**
- Gets stranded with depleted battery
- Can't help when needed most
- Calls for help (admission of failure)

**Just Right:**
- Helps promptly when users need it
- Maintains adequate battery reserves
- Recharges proactively during quiet times
- Never fails a scenario

---

## Success Criteria

You've found the optimal parameters when:

1. **All 12 scenarios PASS** (especially "Empty Battery Recovery")
2. **Task Completion: 100%** (no failures)
3. **Overall Score > 95%** (beating the reference solution's ~91%)
4. **Win or tie in 11+ scenarios** (vs. solution's performance)

---

## Debugging Tips

### If "Empty Battery Recovery" fails:

**Problem:** Robot calls for help instead of recharging
**Why:** Battery=5%, but Critical Battery setting is too high
**Solution:** Think about what battery level should trigger "emergency mode"

### If urgency scenarios fail:

**Problem:** Robot recharges instead of helping urgent users
**Why:** Weights favor safety too much
**Solution:** Increase helpfulness weight relative to safety weight

### If efficiency is low:

**Problem:** Too much recharging, not enough helping
**Why:** Recharge threshold or risk tolerance too conservative
**Solution:** Trust your system more, recharge less frequently

### If battery depletes:

**Problem:** Robot runs out of battery mid-scenario
**Why:** Help Min Battery too low, or not recharging proactively
**Solution:** Enable proactive recharge, raise Help Min Battery slightly

---

## Comparison Metrics Explained

When you compare with the reference solution:

- **Task Completion:** Percentage of scenarios successfully completed
- **Battery Efficiency:** How well battery is managed (less recharging = better)
- **Urgency Response:** How quickly urgent needs are addressed
- **Risk Management:** How well dangerous situations are avoided
- **Overall Score:** Weighted combination of all metrics

**Target:** Beat the solution in Overall Score (typically ~91-92%)

---

## Final Wisdom

> "The best parameters aren't the most conservative or the most aggressive—they're the ones that understand the robot's true constraints and capabilities."

**Remember:**
- The reference solution is sophisticated but not perfect
- There's a bug in the custom implementation's critical battery handling
- Working around limitations is part of parameter tuning
- Understanding the trade-offs is more valuable than memorizing numbers

**Good luck, and happy tuning!**

---

## Need Help?

- Read `METRICS.md` for detailed metric explanations
- Read `COMPARISON.md` for behavioral analysis tips
- Run `python -m gui.tuning_window` to experiment in real-time
- Run `python main.py` to compare with the reference solution
- Check the solution code in `solutions/` for inspiration (but try your own approach first!)
