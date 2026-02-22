# Takeshita, Bryan — FE621 HW1 Grading

**Final Score: 83/100 + 0 bonus = 83**

---

## Part 1: Data Gathering (18/20)

### Q1 — Download Function (5/5)
- Python download function
- Handles equity and option data
- Well-organized

### Q2 — Download Data (4/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- **Notable**: TTM computed via **exact seconds** — more precise than most students

### Q3 — Written Descriptions (4/5)
- Descriptions of SPY, TSLA, VIX provided
- Good rate sourcing discussion
- **Minor**: OCC format not detailed

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate properly sourced ✓
- **TTM via exact seconds** — excellent precision, converts to years

---

## Part 2: Data Analysis (39/50)

### Q5 — Black-Scholes (7/7)
- BS formula correctly implemented
- Handles calls and puts
- Clean implementation

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV reported
- **Issue**: Some IV=0 artifacts present — not filtered or discussed

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**

### Q8 — IV Tables + Commentary (5/7)
- IV tables present
- Average vols computed
- Commentary covers required points
- IV=0 artifacts visible in tables but not addressed

### Q9 — Put-Call Parity (4/6)
- Correctly implemented
- Comparison shown
- Brief analysis

### Q10 — Vol Smile Plots (4/6)
- 2D plots ✓
- Multi-maturity overlay ✓
- **No 3D surface**

### Q11 — Greeks (3/5)
- Analytical + FD Greeks computed
- **CRITICAL ISSUE**: SPY Greeks table shows **Delta=1, Gamma=0, Vega=1e6** — student chose deep ITM strikes for the comparison, where Delta saturates at 1, Gamma is effectively 0, and Vega is meaningless
- Should have selected near-ATM options for Greeks comparison
- TSLA Greeks appear more reasonable

### Q12 — DATA2 Pricing (5/5)
- DATA2 pricing with DATA1 IVs ✓
- Comprehensive comparison
- BS prices vs market
- Well-presented

---

## Part 3: AMM Fee Revenue (26/30)

### Q3a — Derive Swap Amounts (8/10)
- Both cases addressed
- Derivation present
- Mathematical approach correct

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal rule correctly implemented
- Numerical results computed
- Adequate resolution

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table computed ✓
- **Optimal gamma search over wider range** — goes beyond the basic 3-value grid
- **Linear relationship found** between σ and γ* — good observation
- Plot produced ✓
- Commentary present

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **TTM via exact seconds** — most precise TTM calculation in the class
- **Extended gamma search** in Part 3 with linear relationship observation
- Strong Q12 implementation
- Part 3 fully complete with good numerical work
- Separate report + code PDFs

## Weaknesses
- **SPY Greeks table broken** — Deep ITM strikes chosen (Delta=1, Gamma=0, Vega=1e6). Should have selected near-ATM options
- **IV=0 artifacts** present but not filtered or discussed
- **No Secant/Muller method**
- No 3D volatility surface
- No Part 4 bonus
- Greeks issue suggests insufficient review of results

## AI Assessment: LOW
The deep-ITM Greeks bug and IV=0 artifacts are genuine student oversights. The exact-seconds TTM approach and extended gamma search show independent thinking. No signs of AI generation.
