# Novoa Molina, Daniela — FE621 HW1 Grading

**Final Score: 88/100 + 0 bonus = 88**

---

## Part 1: Data Gathering (15/20)

### Q1 — Download Function (4/5)
- Python download function using yfinance
- Downloads equity and option chains
- VIX options code present — attempts to download VIX option chains
- Third-Friday filtering implemented

### Q2 — Download Data (3/5)
- Two consecutive days of data
- TSLA, SPY downloaded ✓
- **Issue**: VIX options code present but **VIX option results not shown** in output
- Third-Friday filtering ✓
- **Missing**: Explanation of many maturities (weeklies, LEAPs)

### Q3 — Written Descriptions (3/5)
- Basic descriptions provided
- **Missing**: Detailed OCC symbol format discussion
- Descriptions adequate but not thorough

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

---

## Part 2: Data Analysis (46/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented from scratch
- Handles calls and puts
- Clean implementation

### Q6 — Bisection IV (7/7)
- Bisection with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV and near-ATM averages reported
- Well-implemented

### Q7 — Newton/Secant + Timing (7/7)
- **Newton AND Secant** both implemented — one of very few students with multiple methods
- Bisection also present (3 methods total)
- Timing comparison across all methods
- Well-documented convergence behavior

### Q8 — IV Tables + Commentary (6/7)
- Comprehensive IV tables
- Average vols by maturity/type/stock
- **Thorough commentary** — discusses TSLA vs SPY, VIX comparison, maturity effects
- Well-written analysis section

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison with market values
- Analysis present
- **Minor**: Could discuss American exercise effects more

### Q10 — Vol Smile Plots (6/6)
- 2D volatility smile ✓
- Multi-maturity overlay ✓
- **3D surfaces** present — well-implemented
- Properly labeled and formatted

### Q11 — Greeks (4/5)
- Analytical + FD Greeks computed
- Comparison showing agreement
- **Minor**: Could show more options across maturities

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs ✓
- BS prices vs market comparison
- Analysis present

---

## Part 3: AMM Fee Revenue (27/30)

### Q3a — Derive Swap Amounts (9/10)
- Handwritten but thorough derivation for both cases
- Clear mathematical structure
- Both Δx and Δy expressions derived

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal integration with **40,000 points** — good resolution
- Lognormal density correctly handled
- Numerical results computed

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table computed ✓
- Optimal γ*(σ) found
- Plot produced ✓
- Commentary present

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **All 3 root-finding methods** implemented (bisection + Newton + Secant) — rare in class
- **Strong Part 2** — one of the highest-scoring Part 2 sections
- **3D volatility surfaces** present
- **Thorough commentary** in Q8 — above average writing quality
- Part 3 complete with good numerical resolution (40K points)
- 3 methods with timing comparison is comprehensive

## Weaknesses
- **VIX options absent from results** — code is present but output not shown
- **Part 3 handwritten** vs Parts 1-2 typeset — inconsistent presentation
- No explanation of many maturities
- No OCC symbol format discussion
- Part 4 bonus not attempted
- Some sections could use more specific numerical references

## AI Assessment: LOW
The combination of thorough computational work with handwritten Part 3 is consistent with authentic student work. The implementation of all 3 root-finding methods shows genuine effort. No signs of AI generation.
