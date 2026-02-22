# Tenreiro, James — FE621 HW1 Grading

**Final Score: 91/100 + 8 bonus = 91(+8)**

---

## Part 1: Data Gathering (18/20)

### Q1 — Download Function (5/5)
- R with `quantmod` + Yahoo JSON API — dual data source approach
- Clean, well-commented R code
- Handles equity and option chain downloads
- Organized output structure

### Q2 — Download Data (4/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- **Missing**: Explicit explanation of why many maturities exist

### Q3 — Written Descriptions (4/5)
- Good descriptions of SPY, TSLA, VIX
- Clean writing style
- **Minor**: OCC format could be more explicit

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- **FRED for rate** — proper H.15 sourcing ✓
- TTM correctly computed ✓

---

## Part 2: Data Analysis (44/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented in R
- Clean implementation with `pnorm()`
- Handles calls and puts

### Q6 — Bisection IV (7/7)
- Pure bisection with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV and near-ATM averages reported
- Well-implemented

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**
- Timing discussion present

### Q8 — IV Tables + Commentary (6/7)
- Good IV tables by maturity/type/stock
- Average vols computed
- Commentary covers TSLA vs SPY, VIX comparison, maturity effects
- Well-written analysis

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- **Quantile analysis** of deviations — goes beyond basic comparison
- Good statistical approach

### Q10 — Vol Smile Plots (5/6)
- 2D plots ✓
- Multi-maturity overlay ✓
- **No 3D surface**
- Well-formatted R plots

### Q11 — Greeks (5/5)
- Analytical + FD Greeks correctly computed
- Comparison showing agreement
- Well-implemented

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs ✓
- **Error plots** for comparison — nice visualization showing pricing errors across strikes
- Good analysis approach

---

## Part 3: AMM Fee Revenue (29/30)

### Q3a — Derive Swap Amounts (10/10)
- Complete derivations for both Case 1 and Case 2
- Clear mathematical presentation
- Well-organized

### Q3b — Expected Fee Revenue (10/10)
- Trapezoidal rule correctly implemented
- Numerical results computed
- **Convergence check included** — verifies integration accuracy
- Well-implemented

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table computed ✓
- Optimal γ*(σ) identified
- Plot produced ✓
- Commentary present
- **Minor**: Could expand discussion

---

## Part 4: Bonus (8/10)

### Analytical Solutions (3/3)
- f1 = xy: 9/4 ✓
- f2 = e^(x+y): correct ✓

### Numerical Implementation (5/7)
- 4 grid pairs tested ✓
- f1 exact ✓
- f2 converges ✓
- Convergence commentary present
- **Minor**: Could discuss convergence rate more formally

---

## Strengths
- **Consistently high quality across all parts** — no major weak spots
- **Part 3 with convergence check** — verifies trapezoidal integration accuracy, shows thoroughness
- **Put-call parity quantile analysis** — statistical approach goes beyond basic comparison
- **Q12 error plots** — nice visualization of pricing errors across strikes
- Clean R code throughout
- FRED integration for rate
- Part 4 bonus complete with convergence commentary

## Weaknesses
- **No Secant/Muller method** — only bisection and Newton
- **No 3D volatility surface** — missed Q10 bonus
- **Minimal inline code comments** — code is clean but sparsely commented
- Missing explanation of many maturities
- Commentary in some sections could include more specific numerical references

## AI Assessment: LOW
Clean R submission with consistent quality. The R language choice, FRED integration, quantile analysis approach, and convergence checking all indicate a strong student with genuine statistical/computational skills. The missing Secant method and 3D surface are typical student omissions. No signs of AI generation.
