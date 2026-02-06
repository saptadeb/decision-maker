# Parameter Cheatsheet

Quick reference for tuning parameters.

---

## Recharge Threshold (10-70%)

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Low (20-30%)** | Recharges rarely, helps more | Risk of battery emergencies |
| **Medium (35-45%)** | Balanced approach | Good balance of safety & helping |
| **High (50-65%)** | Recharges frequently | Slower response to users |

---

## Critical Battery (5-25%)

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Very Low (5-10%)** | Rarely enters emergency mode | Maximum helping opportunities |
| **Low (12-18%)** | Moderate emergency threshold | Balanced safety margin |
| **High (20-25%)** | Enters emergency mode early | May be overly cautious |

---

## Help Min Battery (10-40%)

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Low (10-20%)** | Helps even with low battery | Risky! May strand robot |
| **Medium (22-28%)** | Safe helping threshold | Enough for help + buffer |
| **High (30-40%)** | Only helps with good battery | May delay urgent help |

---

## Proactive Recharge (On/Off)

| Setting | Behavior | Trade-offs |
|---------|----------|-----------|
| **Disabled** | Reactive charging only | May get caught unprepared |
| **Enabled** | Charges when safe to do so | Always prepared for urgency |

---

## Safety Weight (0.0-1.0)

| Setting | Behavior | Philosophy |
|---------|----------|------------|
| **Low (0.2-0.35)** | Risk-tolerant, helps aggressively | Users first, battery second |
| **Medium (0.4-0.5)** | Balanced priorities | Safety and helping are equal |
| **High (0.6-0.8)** | Very conservative | Battery safety is paramount |

---

## Helpfulness Weight (0.0-1.0)

| Setting | Behavior | Philosophy |
|---------|----------|------------|
| **Low (0.2-0.4)** | Self-preservation focus | I help when it's safe |
| **Medium (0.5-0.6)** | User-focused | Users are my priority |
| **High (0.65-0.8)** | Highly responsive | Help users at almost any cost |

---

## Risk Tolerance (Conservative / Medium / Aggressive)

| Setting | Multiplier | Recharge Behavior | Philosophy |
|---------|------------|-------------------|------------|
| **Conservative** | 1.5× | Recharges much earlier | Always maintain high battery |
| **Medium** | 1.0× | Recharges at exact threshold | Trust the thresholds |
| **Aggressive** | 0.7-0.8× | Pushes battery lower | Use battery efficiently |

---

## Action Costs

| Action | Battery Impact |
|--------|---------------|
| HELP_USER | -15% |
| RECHARGE | +50% |
| WAIT | -2% |
| CALL_FOR_HELP | -5% |
