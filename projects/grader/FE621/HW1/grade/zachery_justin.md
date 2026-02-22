# Zachery, Justin — FE621 HW1 Grading (LATE)

**Final Score: 82/100 + 5 bonus = 82(+5)**

---

## Part 1: Data Gathering (16/20)

### Q1 — Download Function (4/5)
- R with `quantmod` for data download
- Clean implementation
- Handles equity and option data

### Q2 — Download Data (4/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- **VIX variance formula included** — shows understanding of VIX construction

### Q3 — Written Descriptions (3/5)
- Basic descriptions provided
- **Missing**: No explicit option symbol (OCC format) discussion
- Adequate but not thorough

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓
- Clean LaTeX presentation

---

## Part 2: Data Analysis (42/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented in R
- Clean implementation with `pnorm()`
- Handles calls and puts

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV reported
- **Issue**: Some SPY IVs > 5.0 for high strikes — artifacts not filtered

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- **Microbenchmark timing** — more precise timing methodology than most students
- **No Secant/Muller method**

### Q8 — IV Tables + Commentary (5/7)
- IV tables present
- Average vols computed
- Commentary covers basic points
- **SPY IV artifacts (>5.0)** visible but not discussed

### Q9 — Put-Call Parity (4/6)
- Correctly implemented
- Comparison shown
- **Weak analysis** — brief and lacks depth

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D plots ✓
- Multi-maturity overlay ✓
- **3D plots** present — earns bonus ✓
- Clean LaTeX formatting

### Q11 — Greeks (5/5)
- Analytical + FD Greeks correctly computed
- Comparison showing agreement
- Well-implemented in R

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs ✓
- BS prices vs market comparison
- Analysis present

---

## Part 3: AMM Fee Revenue (24/30)

### Q3a — Derive Swap Amounts (8/10)
- Both cases addressed
- Derivation present
- Correct approach

### Q3b — Expected Fee Revenue (8/10)
- Trapezoidal rule implemented ✓
- Numerical results computed

### Q3c — Optimal Fee Rate (8/10)
- σ×γ table computed ✓
- **Step function** pattern for γ* — matches class-wide observation
- Plot produced ✓
- **Missing**: Detailed written commentary on the pattern

---

## Part 4: Bonus (0/10)

Not attempted. (However, Q10 3D plots earn bonus within Part 2.)

---

## Strengths
- **Clean LaTeX presentation** — one of the more professionally formatted submissions
- **3D plots** earn bonus in Q10
- **Microbenchmark timing** — precise methodology
- **VIX variance formula** — shows understanding of VIX construction beyond just recording the value
- R code throughout — consistent language choice
- Good overall coverage of Parts 1-3

## Weaknesses
- **No Secant/Muller method**
- **No option symbol (OCC) discussion**
- **SPY IV artifacts > 5.0** — not filtered or discussed
- **Weak put-call parity analysis**
- Part 3 commentary thin — missing detailed analysis of gamma pattern
- Part 4 not attempted
- LATE submission

## AI Assessment: LOW
Clean LaTeX with R code is consistent with a well-prepared student. The VIX variance formula inclusion shows genuine interest in the material. SPY IV artifacts and weak parity analysis are typical student oversights. No signs of AI generation.
