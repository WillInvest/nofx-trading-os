# Stiemer, Julius — FE621 HW1 Grading (LATE)

**Final Score: 68/100 + 2 bonus = 68(+2)**

---

## Part 1: Data Gathering (17/20)

### Q1 — Download Function (4/5)
- Python with yfinance for data download
- Handles equity and option chains
- Third-Friday filtering present
- Brief but functional

### Q2 — Download Data (4/5)
- Two consecutive days ✓
- TSLA, SPY, ^VIX ✓
- **3 short-dated maturities** — all near-term, which limits the maturity analysis
- **Missing**: Explanation of many maturities

### Q3 — Written Descriptions (4/5)
- Brief descriptions of symbols
- Adequate but minimal
- **Missing**: OCC symbol format

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

---

## Part 2: Data Analysis (39/50)

### Q5 — Black-Scholes (7/7)
- BS class implementation — well-structured OOP approach
- Handles calls and puts correctly
- Clean design

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV reported

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**
- Very sparse writing about results

### Q8 — IV Tables + Commentary (4/7)
- IV tables present
- Average vols computed
- **Very sparse writing** — mostly just tables with minimal analysis
- The assignment emphasizes "quality of writing and interpretation"

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison shown
- Brief analysis

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D plots ✓
- Multi-maturity overlay ✓
- **3D surfaces** present — earns bonus

### Q11 — Greeks (4/5)
- Analytical + FD computed
- Comparison present
- **Minor**: Limited analysis

### Q12 — DATA2 Pricing (2/5)
- Attempted but thin
- Limited comparison analysis

---

## Part 3: AMM Fee Revenue (10/30)

### Q3a — Derive Swap Amounts (6/10)
- Handwritten derivation — looks rushed
- Both cases referenced
- Mathematical structure present but incomplete

### Q3b — Expected Fee Revenue (4/10)
- Partially set up — code structure present
- **Not fully implemented** — missing complete trapezoidal integration
- No clear numerical results

### Q3c — Optimal Fee Rate (0/10)
- **ENTIRELY MISSING** — no σ×γ table, no optimal γ*, no plot, no commentary

---

## Part 4: Bonus (2/10)

### Analytical Solutions (2/3)
- f1 and f2 analytical solutions attempted
- Results appear correct

### Numerical Implementation (0/7)
- **No numerical verification** — only analytical solutions, no trapezoidal approximation code
- No grid pairs, no error analysis

---

## Strengths
- 3D volatility surfaces are well-done — earns bonus
- BS class implementation is clean OOP design
- Parts 1-2 are reasonably complete
- Bisection and Newton both functional

## Weaknesses
- **Part 3c entirely missing** — 10 points lost
- **Part 3b partially incomplete** — another 6 points lost
- **Part 4 numerical section missing** — only analytical solutions provided
- Handwritten Part 3 pages look rushed — hard to follow
- **Very sparse writing throughout** — minimal prose, mostly code output
- No Secant/Muller method
- 3 short-dated maturities limit the maturity analysis

## AI Assessment: LOW
The rushed handwritten pages, incomplete sections, and very sparse writing are all consistent with a student who ran out of time (LATE submission confirms this). The BS class OOP design suggests genuine coding ability. No signs of AI generation.
