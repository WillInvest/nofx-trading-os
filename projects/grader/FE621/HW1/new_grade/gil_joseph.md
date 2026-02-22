# Gil, Joseph — FE621 HW1 Grading

**Final Score: 75/100 + 0 bonus = 75**

---

## Part 1: Data Gathering (19/20)

### Q1 — Download Function (5/5)
- Solid download function using yfinance
- Handles TSLA, SPY, ^VIX equity and option data
- Third-Friday logic correctly implemented
- Code functional and well-organized

### Q2 — Download Data (5/5)
- Two consecutive trading days ✓
- All three tickers downloaded ✓
- Third-Friday maturities filtered ✓
- Data structure properly organized

### Q3 — Written Descriptions (4/5)
- SPY, TSLA, VIX described
- Basic option expiration discussion
- **Missing**: OCC option symbol format not discussed in detail

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM correctly computed ✓

---

## Part 2: Data Analysis (38/50)

### Q5 — Black-Scholes (7/7)
- BS call and put formulas correctly implemented
- Clean implementation with proper d1/d2
- Uses norm.cdf ✓

### Q6 — Bisection IV (6/7)
- Bisection implemented with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV reported
- Near-ATM averages computed

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison: Newton ~3.7x faster than bisection
- **No Secant/Muller method**
- Brief timing discussion

### Q8 — IV Tables + Commentary (4/7)
- IV tables present
- Average vols by maturity/type
- Commentary is sparse — minimal writing
- **Missing**: Detailed numerical comparisons

### Q9 — Put-Call Parity (4/6)
- Correctly implemented
- Comparison shown
- Brief analysis
- **Missing**: Discussion of American exercise effects

### Q10 — Vol Smile Plots (5/6)
- 2D plots present ✓
- Multi-maturity overlay ✓
- 3D scatter plots present — partial bonus quality
- **Note**: Plots may be as screenshots/images rather than inline

### Q11 — Greeks (4/5)
- Analytical + FD Greeks computed
- Comparison showing agreement
- **Minor**: Limited to a few options

### Q12 — DATA2 Pricing (3/5)
- DATA2 pricing attempted
- BS prices vs market comparison
- **Weakness**: Analysis is thin

---

## Part 3: AMM Fee Revenue (18/30)

### Q3a — Derive Swap Amounts (7/10)
- Both cases addressed
- Derivation present
- Mathematical approach correct
- Could be cleaner

### Q3b — Expected Fee Revenue (6/10)
- Trapezoidal rule implemented
- Numerical results computed
- Adequate implementation

### Q3c — Optimal Fee Rate (5/10)
- σ×γ table computed with coarse grid
- All γ* = 0.01 — the standard class pattern from limited {0.001, 0.003, 0.01} grid
- Plot produced
- **Missing**: Written commentary
- No extended grid search beyond the 3 specified γ values

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- Strong Part 1 — solid data gathering with all requirements met
- Timing comparison shows clear Newton advantage (3.7x)
- All parts of the assignment attempted
- 3D scatter plots for vol surface

## Weaknesses
- **Code presented as images/screenshots** in some sections — harder to verify and not professional
- **Sparse comments** throughout code
- **Minimal writing** — the assignment emphasizes "quality of writing and interpretation"
- No Secant/Muller method
- Part 3 Q3c uses only the coarse gamma grid — no extended analysis
- No Part 4 bonus
- Report format is not polished LaTeX/Word

## AI Assessment: LOW
Code as images, sparse comments, and minimal writing are all consistent with authentic student work. An AI would typically generate more prose and avoid screenshot-based code. No signs of AI generation.
