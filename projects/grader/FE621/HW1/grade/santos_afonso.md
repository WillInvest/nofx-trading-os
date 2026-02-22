# Santos, Afonso — FE621 HW1 Grading

**Final Score: 84/100 + 0 bonus = 84**

---

## Part 1: Data Gathering (17/20)

### Q1 — Download Function (4/5)
- R with `quantmod` for data download
- Loads data from local CSVs rather than live API in the report — data was previously downloaded
- Handles equity and option data
- Third-Friday filtering present

### Q2 — Download Data (4/5)
- Two consecutive days (DATA1 and DATA2) ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- **Issue**: DATA2 collected at **9:50am** — very early in trading session, possibly before active quoting (Mid=0 for many options)

### Q3 — Written Descriptions (4/5)
- Good descriptions of SPY, TSLA, VIX
- Written analysis of option mechanics
- **Minor**: OCC symbol format could be more detailed

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

---

## Part 2: Data Analysis (45/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented in R
- `bs_call()` and `bs_put()` with `pnorm()`
- Clean R implementation

### Q6 — Bisection IV (7/7)
- Pure bisection with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV reported
- Near-ATM averages computed
- **Note**: SPY ATM IV anomaly — suspiciously low at 0.72%, likely from the early-morning DATA2 issue

### Q7 — Newton/Secant + Timing (7/7)
- **ALL 3 METHODS implemented**: bisection + Newton + Secant — **ONLY STUDENT in the class with all three**
- Newton with analytical vega ✓
- Secant method properly implemented
- Timing comparison across all three methods
- Excellent coverage

### Q8 — IV Tables + Commentary (5/7)
- IV tables present
- Average vols by maturity/type/stock
- Commentary addresses basic required points
- **Weakness**: SPY ATM IV of 0.72% should have been flagged as suspicious

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison with market values
- Analysis present

### Q10 — Vol Smile Plots (6/6)
- 2D volatility smile ✓
- Multi-maturity overlay ✓
- **3D plotly surfaces** — interactive plots using plotly library
- Professional visualization

### Q11 — Greeks (5/5)
- Analytical + FD Greeks correctly computed
- Comparison showing agreement
- Well-implemented in R

### Q12 — DATA2 Pricing (3/5)
- DATA2 pricing attempted
- **Problem**: DATA2 collected at 9:50am with many Mid=0 values → unreliable pricing comparison
- Basic structure correct but output quality compromised by early-morning data

---

## Part 3: AMM Fee Revenue (22/30)

### Q3a — Derive Swap Amounts (8/10)
- Handwritten derivation — both cases addressed
- Mathematical approach correct
- Could be cleaner in presentation

### Q3b — Expected Fee Revenue (7/10)
- Trapezoidal rule implemented in R
- Numerical results computed
- Works correctly

### Q3c — Optimal Fee Rate (7/10)
- σ×γ table computed ✓
- Optimal γ*(σ) found
- Plot produced ✓
- **Commentary thin** — lacks detailed analysis of the pattern

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **ONLY student with ALL 3 root-finding methods** (bisection + Newton + Secant) — standout achievement
- **3D plotly surfaces** — interactive, professional visualizations
- Strong Part 2 — one of the highest-scoring sections
- R implementation throughout — consistent language choice
- Timing comparison across all 3 methods

## Weaknesses
- **DATA2 collected at 9:50am** — before active quoting, many Mid=0 values. Compromises Q12
- **SPY ATM IV = 0.72%** — suspiciously low, should have been investigated and flagged
- Part 3 commentary thin
- No Part 4 bonus
- Handwritten Part 3 derivation could be cleaner
- Data loaded from local CSVs rather than demonstrating live API call

## AI Assessment: LOW
R code with `quantmod`, all 3 root-finding methods, and plotly 3D surfaces show a strong and independently-minded student. The early-morning data issue and undiagnosed SPY IV anomaly are genuine student oversights. No signs of AI generation.
