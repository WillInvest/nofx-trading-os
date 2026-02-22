# Trivedi, Akarsh — FE621 HW1 Grading

**Final Score: 79/100 + 9 bonus = 79(+9)**

---

## Part 1: Data Gathering (14/20)

### Q1 — Download Function (4/5)
- Python with yfinance
- Downloads equity and option data
- Third-Friday filtering present
- Functional implementation

### Q2 — Download Data (2/5)
- **CRITICAL ISSUE**: DATA1 and DATA2 collected on the **SAME DAY** — only 20 minutes apart, not two consecutive trading days as required
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- This violates the fundamental requirement of "two consecutive days" and cascades into Q12

### Q3 — Written Descriptions (3/5)
- Basic descriptions provided
- **Missing**: OCC option symbol format
- Adequate but not thorough

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓
- **Note**: DATA2 rate falls back to hardcoded 0.05 when FRED API fails — significantly different from actual rate

---

## Part 2: Data Analysis (39/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented
- Handles calls and puts
- Clean implementation

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV reported
- Near-ATM averages computed

### Q7 — Newton/Secant + Timing (4/7)
- Newton with analytical vega ✓
- **No Secant/Muller method**
- **No timing table** — assignment requires timing comparison
- Results present but not formally compared

### Q8 — IV Tables + Commentary (5/7)
- IV tables by maturity/type/stock
- Average vols computed
- Commentary covers basic points
- Adequate analysis

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison shown
- Analysis present

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D plots ✓
- Multi-maturity overlay ✓
- **3D surfaces** present — earns bonus ✓
- Well-visualized

### Q11 — Greeks (4/5)
- Analytical + FD Greeks computed
- Comparison showing agreement
- **Minor**: Limited options analyzed

### Q12 — DATA2 Pricing (2/5)
- Attempted but **fundamentally compromised** — DATA1 and DATA2 are from the same day (20 min apart)
- BS prices computed but the comparison is meaningless when there's no actual day-over-day movement
- Additionally, DATA2 uses hardcoded rate 0.05 instead of actual Fed funds rate

---

## Part 3: AMM Fee Revenue (26/30)

### Q3a — Derive Swap Amounts (8/10)
- Both cases addressed
- Derivation present
- Correct mathematical approach

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal rule with **40,000 grid points** — good resolution
- Lognormal density correctly handled
- Numerical results computed

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table computed ✓
- Good sigma-gamma analysis
- Plot produced ✓
- Commentary present

---

## Part 4: Bonus (9/10)

### Analytical Solutions (3/3)
- f1 = xy: 9/4 ✓
- f2 = e^(x+y): correct ✓

### Numerical Implementation (6/7)
- 4 grid pairs tested ✓
- f1 exact ✓
- f2 converges ✓
- Convergence shown
- **Minor**: Could discuss convergence rate

---

## Strengths
- **Part 3 complete** with 40K grid points and good analysis
- **Part 4 bonus complete** — both analytical and numerical
- 3D volatility surfaces — earns Q10 bonus
- Strong Part 3 and Part 4 sections
- Good overall computational coverage

## Weaknesses
- **SAME-DAY DATA** — DATA1 and DATA2 collected 20 minutes apart on the same day. This is the single biggest issue, violating the fundamental "two consecutive trading days" requirement and rendering Q12 meaningless
- **Hardcoded rate 0.05** for DATA2 — when FRED API fails, falls back to 0.05 instead of 0.0364. This 36% rate difference significantly affects all DATA2 pricing
- **No Secant/Muller method**
- **No timing table** — required by Q7
- No OCC option symbol format discussion
- Q12 results are unreliable due to same-day data + wrong rate

## AI Assessment: LOW
The same-day data issue and hardcoded rate fallback are genuine student mistakes. The hardcoded 0.05 (a round number clearly chosen as a placeholder) is a typical student shortcut. 3D surfaces and complete Part 3/4 show genuine computational ability. No signs of AI generation.
