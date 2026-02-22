# Yao, Yuhang — FE621 HW1 Grading

**Final Score: 81/100 + 0 bonus = 81**

---

## Part 1: Data Gathering (16/20)

### Q1 — Download Function (4/5)
- Python with yfinance
- Downloads equity and option data
- Third-Friday filtering present

### Q2 — Download Data (3/5)
- **Lost VIX/SPY day-1 data** — accidentally deleted
- Only TSLA has complete 2-day data
- This cascades into Q12 (only TSLA can be compared)
- Third-Friday maturities ✓

### Q3 — Written Descriptions (4/5)
- Descriptions of SPY, TSLA, VIX
- Adequate
- **Minor**: "Bouns" typo

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

---

## Part 2: Data Analysis (41/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented
- Handles calls and puts
- Clean code

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV reported
- **Issue**: Some IV=0 artifacts present — not filtered

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**
- Divide-by-zero warnings present

### Q8 — IV Tables + Commentary (5/7)
- IV tables present
- Average vols computed
- Commentary covers basic points
- IV=0 artifacts visible but not addressed

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison shown
- Analysis present

### Q10 — Vol Smile Plots (6/6)
- 2D plots ✓
- Multi-maturity overlay ✓
- **3D scatter plots** present — partial bonus quality
- Properly visualized

### Q11 — Greeks (4/5)
- Analytical + FD Greeks computed
- Comparison present
- **Minor**: Divide-by-zero warnings in some calculations

### Q12 — DATA2 Pricing (3/5)
- **Only TSLA** can be priced (lost SPY/VIX day-1 data)
- TSLA comparison present and correct
- Significantly incomplete due to data loss

---

## Part 3: AMM Fee Revenue (27/30)

### Q3a — Derive Swap Amounts (9/10)
- Both cases addressed
- Derivation present
- Correct approach

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal rule implemented
- **Monte Carlo validation** — unique approach in the class, uses random sampling to verify trapezoidal result
- Good cross-validation methodology

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
- **Monte Carlo validation** for trapezoidal integration — unique in the class, shows statistical thinking
- 3D scatter plots present
- Part 3 fully complete with creative validation approach
- Good overall Part 2 coverage despite data loss
- Honest about data loss

## Weaknesses
- **Lost VIX/SPY day-1 data** — accidentally deleted, compromises Q2 and Q12
- **Q12 only has TSLA** — significant data loss impact
- **IV=0 artifacts** not filtered or discussed
- **Divide-by-zero warnings** in Newton and Greeks — not addressed
- **No Secant/Muller method**
- "Bouns" typo
- No Part 4 bonus
- Data management issue (deletion) suggests poor backup practices

## AI Assessment: LOW
The accidental data deletion, IV=0 artifacts, divide-by-zero warnings, and "Bouns" typo are all strongly human indicators. The Monte Carlo validation for trapezoidal integration shows genuine statistical creativity. No signs of AI generation.
