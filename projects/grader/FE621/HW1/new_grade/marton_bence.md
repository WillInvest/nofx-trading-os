# Marton, Bence — FE621 HW1 Grading

**Final Score: 90/100 + 0 bonus = 90**

---

## Part 1: Data Gathering (19/20)

### Q1 — Download Function (5/5)
- Well-structured download function using yfinance
- Handles multiple tickers with option chain downloads
- Third-Friday filtering correctly implemented
- Clean code organization

### Q2 — Download Data (5/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- **4 expirations** downloaded (exceeds required 3)
- Proper data structure

### Q3 — Written Descriptions (4/5)
- Good descriptions of SPY as ETF, VIX as volatility index
- TSLA described
- **Missing**: OCC option symbol format not discussed in detail

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate: **^IRX** (13-week T-bill rate) — valid alternative to Fed funds, shows independent thinking ✓
- TTM correctly computed ✓

---

## Part 2: Data Analysis (44/50)

### Q5 — Black-Scholes (7/7)
- BS formula correctly implemented from scratch
- Handles calls and puts with correct d1/d2
- Clean code

### Q6 — Bisection IV (6/7)
- Pure bisection with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV and near-ATM averages reported
- **Flag**: Bisection IV for short-dated options shows 0.514 — differs from Newton (0.288)

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**
- **Note**: Short-dated IV discrepancy (bisection 0.514 vs Newton 0.288) suggests one method has convergence issues for near-expiry options — student doesn't investigate

### Q8 — IV Tables + Commentary (6/7)
- Good IV tables by maturity, type, and stock
- Average vols in near-ATM band computed
- Put-call parity with **bid-ask check** — goes beyond basic comparison
- Commentary is adequate
- **Minor**: Could be more detailed in numerical comparisons

### Q9 — Put-Call Parity (6/6)
- Correctly implemented
- Comparison with market bid/ask values
- Bid-ask spread check included — nice touch
- Good analysis of deviations

### Q10 — Vol Smile Plots (5/6)
- 2D volatility smile present ✓
- Multi-maturity overlay ✓
- **No 3D surface plot**
- Properly labeled

### Q11 — Greeks (5/5)
- Analytical + FD Greeks correctly computed
- Comparison showing excellent agreement
- Applied to appropriate options

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs ✓
- BS prices vs market comparison
- Analysis present
- **Minor**: Some affected by bisection/Newton discrepancy for short-dated options

---

## Part 3: AMM Fee Revenue (27/30)

### Q3a — Derive Swap Amounts (9/10)
- Complete derivations for both Case 1 and Case 2
- Clear mathematical presentation
- Final expressions properly stated

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal rule correctly implemented
- Numerical results computed
- Adequate grid resolution
- Well-presented

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table with all required combinations ✓
- Optimal γ*(σ) identified
- Plot produced ✓
- **Commentary present** — discusses the observed pattern
- One of the more complete Q3c implementations

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **Strong across all parts** — consistent quality from Part 1 through Part 3
- **^IRX for interest rate** — uses 13-week T-bill rate instead of Fed funds; valid and shows independent thinking
- **Put-call parity with bid-ask check** — goes beyond basic implementation
- **Part 3 fully complete with commentary** — derivation, code, table, plot, AND written analysis
- 4 expirations (exceeds 3 required)
- Good overall balance between code and writing

## Weaknesses
- **Bisection vs Newton IV discrepancy** for short-dated options (0.514 vs 0.288) — not investigated
- **No Secant/Muller method**
- **No 3D volatility surface** (bonus not attempted)
- Part 4 bonus not attempted
- OCC option symbol format not discussed
- Some commentary could be more detailed with specific numerical references

## AI Assessment: LOW
Submission shows consistent quality with genuine analytical work. The IV discrepancy (left uninvestigated) and missing Secant method are typical student omissions. The use of ^IRX for the rate shows independent decision-making. No signs of AI generation.
