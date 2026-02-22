# Smadi, Fallyn — FE621 HW1 Grading

**Final Score: 48/100 + 0 bonus = 48**

---

## Part 1: Data Gathering (16/20)

### Q1 — Download Function (4/5)
- Python download function using yfinance
- Downloads equity and option data
- Third-Friday filtering present
- Functional implementation

### Q2 — Download Data (4/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- Data properly collected

### Q3 — Written Descriptions (3/5)
- Basic descriptions of symbols
- Adequate for SPY and VIX
- **Missing**: OCC option symbol format

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

---

## Part 2: Data Analysis (32/50)

### Q5 — Black-Scholes (6/7)
- BS formula implemented
- Handles calls and puts
- **Minor issue**: Interest rate used as `r2 = 0.00364` — appears to be **10x too small** (should be 0.0364). This is either a decimal conversion error or a typo that propagates through calculations

### Q6 — Bisection IV (5/7)
- Bisection implemented with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV reported
- Results may be affected by rate typo

### Q7 — Newton/Secant + Timing (4/7)
- Newton with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**
- Brief discussion

### Q8 — IV Tables + Commentary (4/7)
- IV tables present
- Average vols computed
- Commentary covers basic points
- Thin analysis

### Q9 — Put-Call Parity (4/6)
- Implementation present
- Comparison shown
- **Note**: Rate typo (0.00364 vs 0.0364) affects put-call parity calculations

### Q10 — Vol Smile Plots (3/6)
- 2D plots present
- **No 3D surface**
- Minimal plot analysis
- Limited visualization

### Q11 — Greeks (2/5)
- Analytical Greeks computed
- FD approximation attempted
- **CRITICAL BUG**: Step size `h = 100` for numerical Greeks — should be ~0.01 or 0.01*S. With h=100, the finite difference approximation is computed over an absurdly wide interval, making the numerical derivatives completely meaningless
- Student doesn't recognize the nonsensical FD results

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing attempted
- **Copy-paste bug** in code — uses DATA1 variables in DATA2 section
- Basic structure present but output compromised

---

## Part 3: AMM Fee Revenue (0/30)

### Q3a — Derive Swap Amounts (0/10)
- **ENTIRELY MISSING** — no AMM content whatsoever

### Q3b — Expected Fee Revenue (0/10)
- **ENTIRELY MISSING**

### Q3c — Optimal Fee Rate (0/10)
- **ENTIRELY MISSING**

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- Part 1 data gathering is adequate — proper download and collection
- BS formula and bisection implemented
- Newton method with analytical vega
- Basic structure of Parts 1-2 is in place

## Weaknesses
- **Part 3 ENTIRELY MISSING** — 0/30 points. This alone drops the grade by 30 points
- **h = 100 for numerical Greeks** — absurdly large step size renders FD approximations meaningless. Should be ~0.01·S (roughly 4-7 for these stocks, not 100). This is a fundamental misunderstanding of finite differences
- **Interest rate typo**: `r2 = 0.00364` instead of 0.0364 — 10x error that propagates through all pricing
- **Copy-paste bug in DATA2 code** — references DATA1 variables
- No Secant/Muller method
- No 3D volatility surface
- No Part 4 bonus
- Thin commentary throughout
- Multiple bugs suggest insufficient testing/review of results

## AI Assessment: LOW
The h=100 bug, rate typo, and copy-paste errors are all genuine student mistakes that an AI would be extremely unlikely to make. The missing Part 3 entirely is consistent with a student who ran out of time. Authentic student work with significant gaps.
