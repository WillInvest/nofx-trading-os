# Chopra, Rohan — FE621 HW1 Grading

**Final Score: 83/100 + 5 bonus = 83(+5)**

---

## Part 1: Data Gathering (15/20)

### Q1 — Download Function (4/5)
- Uses yfinance for data download — functional implementation
- Downloads equity OHLCV and option chains for TSLA, SPY, ^VIX
- Third-Friday expiration filtering present
- **Minor**: VIX options NOT downloaded — only VIX spot level collected

### Q2 — Download Data (3/5)
- Two consecutive trading days with data for TSLA and SPY
- Third-Friday filtering for 3 monthly maturities ✓
- **Missing**: No CSV/Excel export functionality visible
- **Missing**: No explanation of why many more maturities exist (weeklies, LEAPs, quarterlies)

### Q3 — Written Descriptions (3/5)
- Basic descriptions of SPY and TSLA provided
- VIX described as volatility index
- **Missing**: No OCC option symbol format discussion
- Descriptions are adequate but not thorough

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded at download time ✓
- Interest rate sourced and recorded ✓
- Time to maturity computed ✓

---

## Part 2: Data Analysis (44/50)

### Q5 — Black-Scholes (7/7)
- BS call and put formulas correctly implemented from scratch
- Uses `norm.cdf` from scipy — follows assignment guidelines
- Clean implementation with proper d1/d2 calculations

### Q6 — Bisection IV (6/7)
- Pure bisection method implemented with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV and near-ATM averages reported
- **Minor**: Some TSLA deep OTM IVs exceed 100% — not filtered or discussed

### Q7 — Newton/Secant + Timing (5/7)
- Newton method implemented with analytical vega ✓
- Timing comparison with bisection present
- **No Secant/Muller method** — only bisection and Newton
- Written comparison of timing results present but brief

### Q8 — IV Tables + Commentary (5/7)
- IV tables by maturity, type, and stock present
- Average near-ATM vols computed
- Commentary covers TSLA vs SPY differences and VIX comparison
- Commentary is adequate but could be more detailed with specific numerical references

### Q9 — Put-Call Parity (5/6)
- Correctly implemented C - P = S - K·e^(-rT)
- Comparison with market bid/ask values
- Scatter plot showing deviations — nice visualization
- **Minor**: No discussion of American exercise premium effects

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D volatility smile for nearest maturity ✓
- Multi-maturity overlay with 3 colors ✓
- **3D volatility surface** implemented — earns bonus points ✓
- Professional matplotlib plotting

### Q11 — Greeks (5/5)
- Analytical Delta, Gamma, Vega correctly implemented
- Finite difference approximations computed
- Comparison table showing good agreement between analytical and FD values
- Applied to near-ATM options

### Q12 — DATA2 Pricing (5/5)
- Uses DATA1 implied vols + DATA2 spot prices + current rate
- BS prices computed and compared with DATA2 market prices
- Error analysis present

---

## Part 3: AMM Fee Revenue (24/30)

### Q3a — Derive Swap Amounts (8/10)
- Both Case 1 and Case 2 derivations present
- Swap amounts Δx and Δy derived from constant product constraint and boundary conditions
- Mathematical structure correct
- **Minor**: Final expressions could be more clearly stated

### Q3b — Expected Fee Revenue (8/10)
- Trapezoidal rule implementation for E[R(S_{t+1})]
- Lognormal density correctly computed
- Numerical approximation with adequate grid points
- Results computed for given parameters

### Q3c — Optimal Fee Rate (8/10)
- σ×γ table computed with extended gamma grid analysis
- Goes beyond the basic {0.001, 0.003, 0.01} — explores wider range
- Optimal γ*(σ) identified for each volatility level
- Plot produced
- **Missing**: Detailed written commentary on the observed pattern

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **3D volatility surface** is one of the better implementations — earns full bonus
- Strong Part 2 overall — all questions addressed with working code
- Put-call parity scatter plot is a nice visualization touch
- Extended gamma grid analysis in Part 3 shows initiative
- Greeks match well between analytical and FD methods
- Clean code organization

## Weaknesses
- **No Secant/Muller method** — only bisection and Newton
- **VIX options not downloaded** — only VIX spot level
- No CSV export functionality (Q1 bonus requirement)
- Missing explanation of why many maturities exist
- No OCC option symbol format discussion
- Some deep OTM IVs > 100% not filtered or discussed
- Part 4 bonus not attempted
- Commentary throughout is adequate but not thorough

## AI Assessment: LOW
Code style is consistent with typical student work. No obvious AI-generation markers. The submission shows genuine understanding with some gaps that an AI would typically fill (e.g., missing Secant method, missing symbol format discussion). Authentic student work.
