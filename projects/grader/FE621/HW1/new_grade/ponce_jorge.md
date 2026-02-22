# Ponce, Jorge — FE621 HW1 Grading

**Final Score: 90/100 + 9 bonus = 90(+9)**

---

## Part 1: Data Gathering (19/20)

### Q1 — Download Function (5/5)
- Well-organized download function
- FRED for interest rate — proper H.15 sourcing
- Organized CSV output structure
- Multi-asset support

### Q2 — Download Data (5/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- CSV export present

### Q3 — Written Descriptions (4/5)
- Good descriptions of SPY (ETF), VIX (volatility index), TSLA
- Option symbol discussion present
- **Minor**: Could be more detailed on OCC format

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- FRED rate sourced ✓
- TTM correctly computed ✓

### Bonus (5/5)
- Multi-asset CSV download implemented ✓

---

## Part 2: Data Analysis (43/50)

### Q5 — Black-Scholes (7/7)
- BS formula correctly implemented
- Clean implementation with proper d1/d2
- Handles calls and puts

### Q6 — Bisection IV (7/7)
- Bisection with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV and averages reported
- Well-implemented

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**
- **Minor**: Placeholder timestamps in output not filled in

### Q8 — IV Tables + Commentary (6/7)
- IV tables by maturity/type/stock ✓
- Average vols computed
- Commentary covers required points
- **Minor**: Some unfilled placeholders

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison with market values
- Analysis present

### Q10 — Vol Smile Plots (4/6)
- 2D plots present ✓
- Multi-maturity overlay ✓
- **No 3D surface plot**

### Q11 — Greeks (5/5)
- Analytical + FD Greeks correctly computed
- Comparison showing agreement
- Well-presented

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs ✓
- BS prices vs market comparison
- Analysis present

---

## Part 3: AMM Fee Revenue (28/30)

### Q3a — Derive Swap Amounts (10/10)
- Complete derivations for both cases
- Clear mathematical presentation
- Well-organized

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal rule correctly implemented
- Numerical results computed
- Adequate resolution

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table computed ✓
- Optimal γ*(σ) identified
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
- Convergence analysis present
- **Minor**: Could include convergence rate discussion

---

## Strengths
- **Comprehensive submission** — all parts complete including Part 4 bonus
- Separate report + code PDFs — well-organized submission
- FRED integration for interest rate
- Part 3 fully complete with derivations and code
- Bonus Part 4 complete with convergence analysis
- Strong overall quality across all sections

## Weaknesses
- **No Secant/Muller method** — only bisection and Newton
- **No 3D volatility surface** — missed the Q10 bonus
- Placeholder timestamps unfilled in some output sections
- No specific timing numbers discussed in writing
- Some commentary could be more detailed

## AI Assessment: LOW
Well-organized submission with genuine computational work. The separate report + code format, FRED integration, and complete coverage all indicate a strong student. Placeholder artifacts suggest authentic development workflow. No signs of AI generation.
