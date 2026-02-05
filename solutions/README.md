# Solutions Folder

This folder contains an **example implementation** of the AI decision-making system. It demonstrates one approach to solving the decision-making challenges.

## Important Notes

**WARNING: These are NOT the only correct solutions!**

The AI decision-making problem has many valid approaches. This solution demonstrates:
- Multi-dimensional scoring (safety, helpfulness, efficiency)
- Strategic rules for critical situations
- Weighted combinations of different priorities

Your solution might look completely different and still be excellent!

## Running the Solution

```bash
python solutions/solution.py
```

This will run the same scenarios as `main.py` but using the advanced AI implementation.

## Comparing Results

Run both versions to see the difference:

```bash
# Custom AI implementation
python main.py

# Reference AI (example implementation)
python solutions/solution.py
```

Compare:
- Which decisions differ?
- Which approach uses fewer steps?
- Which manages battery better?
- Which prioritizes differently?

## Files

- `solution_scoring.py` - Advanced scoring implementation
  - Separate scoring for safety, helpfulness, and efficiency
  - Weighted combination of scores
  - Context-aware evaluation

- `solution_decision.py` - Advanced decision logic
  - Strategic rules for critical situations
  - Scoring-based fallback for normal situations
  - Explanation generation (bonus feature)

- `solution.py` - Main runner
  - Identical to main.py but imports solution modules
  - Shows side-by-side comparison potential

## Understanding This Solution

When reviewing this code, consider:

1. **What priorities does it encode?**
   - Look at the weights in `score_action()`
   - What values matter most?

2. **How does it handle tradeoffs?**
   - When does it sacrifice battery for urgency?
   - When does it delay helping to recharge?

3. **What assumptions does it make?**
   - Are these assumptions reasonable?
   - Would they work in all scenarios?

4. **How would you improve it?**
   - What edge cases might it miss?
   - What would you prioritize differently?

## Implementation Approach

To create a custom implementation:

1. Run the reference solution to see how it behaves
2. Understand WHY it makes each decision
3. Identify alternative approaches
4. Implement a different strategy in the implementation files

The goal is to explore different tradeoff strategies, not to find the "right answer."

## Discussion Questions

- Is this solution too conservative with battery?
- Does it respond quickly enough to urgent users?
- Would this work well for a real assistive robot?
- What ethical concerns does this implementation raise?

