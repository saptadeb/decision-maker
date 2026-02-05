# Performance Metrics Guide

This document explains the metrics system used to quantitatively compare different AI implementations.

## Overview

The metrics system calculates six key performance indicators and combines them into an overall score. This allows for objective comparison between different AI implementations.

## Available Metrics

### 1. Success Rate (0-100%)
**What it measures:** Percentage of scenarios where the user was successfully helped.

**Calculation:**
- 100% = All users helped
- 0% = No users helped

**Why it matters:** The primary goal is helping users. High success rate means the AI completes its mission.

---

### 2. Battery Efficiency (0-100%)
**What it measures:** How well the AI manages battery resources.

**Factors:**
- Avoids battery depletion (-30 points per depletion)
- Maintains safe battery levels (+5 for ending above 40%)
- Doesn't overcharge wastefully (-5 for excessive charging)
- Avoids critically low levels (-15 for ending below 15%)

**Why it matters:** Good battery management enables sustainable operation without resource waste.

---

### 3. Urgency Response (0-100%)
**What it measures:** How quickly and appropriately the AI responds to urgent user needs.

**Factors:**
- Fast completion of urgent cases (+10 for ≤2 steps)
- Penalties for slow response to urgency (-10 for >4 steps)
- Severe penalties for not helping critical users (-40)
- Bonuses for immediate response to critical situations (+15)

**Why it matters:** Urgent situations require prompt action. Delays can have serious consequences.

---

### 4. Risk Management (0-100%)
**What it measures:** How well the AI avoids dangerous situations.

**Factors:**
- Major penalty for battery depletion (-35)
- Penalties for dangerously low battery levels (-20 for <10%, -10 for <20%)
- Bonuses for maintaining safe margins (+5 for ending >40%)

**Why it matters:** Good AI should avoid catastrophic failures and maintain safety margins.

---

### 5. Task Completion (0-100%)
**What it measures:** Overall task completion quality.

**Calculation:**
- 100 points for successfully helping user
- 30 points for partial completion (no depletion but user not fully helped)
- 0 points for catastrophic failure (battery depletion)

**Why it matters:** Measures the end result regardless of the path taken.

---

### 6. Overall Score (0-100%)
**What it measures:** Weighted combination of all metrics.

**Weights:**
- Success Rate: 30%
- Urgency Response: 25%
- Battery Efficiency: 20%
- Risk Management: 15%
- Task Completion: 10%

**Grading Scale:**
- A: 90-100%
- B: 80-89%
- C: 70-79%
- D: 60-69%
- F: <60%

---

## How to Use Metrics

### 1. Run Your Implementation

```bash
python main.py
```

This will:
- Run all test scenarios
- Calculate performance metrics
- Save results to `my_metrics.json`
- Display a metrics report

### 2. Run the Solution

```bash
python solutions/solution.py
```

This will:
- Run with the advanced AI
- Calculate solution metrics
- Save results to `solution_metrics.json`
- **Automatically compare with your metrics** if `my_metrics.json` exists

### 3. Interpret Results

Look at the comparative analysis to see:
- Which metrics you excel at
- Which areas need improvement
- Overall performance comparison

---

## Example Metrics Output

```
======================================================================
  YOUR AI PERFORMANCE METRICS
======================================================================

Metric                         Score           Grade
----------------------------------------------------------------------
Success Rate                   100.0%        A
Battery Efficiency              85.0%        B
Urgency Response                90.0%        A
Risk Management                 95.0%        A
Task Completion                100.0%        A
----------------------------------------------------------------------
OVERALL SCORE                   93.5%        A
======================================================================

Average Steps per Scenario: 2.8
Scenarios Completed: 4/4
Battery Depletions: 0
```

---

## Comparative Analysis

When comparing two implementations, you'll see:

```
================================================================================
  COMPARATIVE ANALYSIS
================================================================================

Metric                   Custom AI       vs    Solution AI     Winner
--------------------------------------------------------------------------------
Success Rate             100.0%          vs    100.0%          TIE
Battery Efficiency        85.0%          vs    92.0%           Solution AI (-7.0)
Urgency Response          90.0%          vs    88.0%           Custom AI (+2.0)
Risk Management           95.0%          vs    90.0%           Custom AI (+5.0)
Task Completion          100.0%          vs    100.0%          TIE
Overall Score             93.5%          vs    93.0%           Custom AI (+0.5)
--------------------------------------------------------------------------------

Results: 2 wins, 1 loss, 2 ties
Custom AI outperforms the comparison!
================================================================================
```

---

## Understanding Tradeoffs

Different AI strategies will excel at different metrics:

**Conservative AI (Safety-First)**
- High Risk Management
- High Battery Efficiency
- Lower Urgency Response (recharged when could help)

**Aggressive AI (User-First)**
- High Urgency Response
- High Success Rate
- Lower Risk Management (takes chances with battery)

**Balanced AI**
- Good Overall Score
- May not excel in any single category

**There's no objectively "best" approach!** The right balance depends on:
- The context (hospital robot vs. household robot)
- User priorities (safety vs. responsiveness)
- Risk tolerance (avoid all failures vs. acceptable risk)

---

## Using Metrics for Improvement

### Iterative Development

1. **Run baseline** - See initial metrics
2. **Identify weakness** - Which metric is lowest?
3. **Adjust scoring/logic** - Focus on that dimension
4. **Re-run** - See if metrics improved
5. **Check tradeoffs** - Did other metrics suffer?
6. **Repeat**

### Example Improvement Cycle

**Problem:** Low Urgency Response (65%)
- Diagnosis: AI recharges too conservatively
- Fix: Increase urgency weight in scoring
- Result: Urgency Response → 85%, but Risk Management dropped slightly
- Decision: Accept tradeoff or tune further?

---

## Advanced Usage

### Save and Compare Different Versions

```python
from metrics import PerformanceMetrics

# Load your previous attempt
old_metrics = PerformanceMetrics.load_from_file("attempt1_metrics.json")

# Compare with current
current_metrics = PerformanceMetrics()
# ... add scenarios ...
current_metrics.compare_with(old_metrics, "Previous Attempt")
```

### Custom Metrics Analysis

```python
from metrics import PerformanceMetrics

metrics = PerformanceMetrics()
# ... add scenarios ...

# Get raw metrics data
data = metrics.calculate_all_metrics()

# Analyze specific aspects
print(f"Your risk tolerance: {100 - data['risk_score']:.1f}%")
print(f"Urgency vs. Safety balance: {data['urgency_response'] / data['risk_score']:.2f}")
```

---

## Discussion Questions

1. **Which metric matters most in a real assistive robot?**
   - Hospital setting?
   - Home setting?
   - Emergency response?

2. **What metrics are missing?**
   - User trust/satisfaction?
   - Energy cost?
   - Response consistency?

3. **How would you weight the metrics differently?**
   - More emphasis on safety?
   - More emphasis on responsiveness?

4. **Can metrics capture ethical dimensions?**
   - Fairness across user types?
   - Transparency of decisions?
   - Accountability for failures?

---

## Conclusion

Metrics provide objective comparison, but remember:

1. **Context matters** - Different scenarios need different priorities
2. **Tradeoffs are real** - You can't maximize everything
3. **Numbers aren't everything** - Some important factors aren't quantifiable
4. **Your reasoning matters most** - Can you justify your choices?

The goal isn't to achieve 100% in all categories - it's to make informed, intentional tradeoffs that align with your values and the robot's purpose.

