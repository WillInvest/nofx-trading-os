# Garg, Achintya — FE621 HW1 Grading

**Final Score: 82/100 + 5 bonus = 82(+5)**

---

## Part 1: Data Gathering (16/20)

### Q1 — Download Function (4/5)
- Uses yfinance for data download — functional implementation
- Downloads equity and option chain data for TSLA, SPY, ^VIX
- Third-Friday expiration filtering present
- Code is functional but minimal comments

### Q2 — Download Data (4/5)
- Two consecutive trading days downloaded ✓
- TSLA, SPY, ^VIX all present ✓
- Third-Friday filtering for 3 monthly maturities ✓
- **Missing**: No explicit explanation of why many more maturities exist (weeklies, LEAPs, etc.)

### Q3 — Written Descriptions (3/5)
- Basic descriptions provided for each symbol
- **Missing**: OCC option symbol format not explicitly discussed
- Descriptions adequate but not thorough — code-heavy submission with minimal prose

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate from appropriate source ✓
- TTM correctly computed ✓

---

## Part 2: Data Analysis (42/50)

### Q5 — Black-Scholes (7/7)
- BS call and put formulas correctly implemented from scratch
- Uses norm.cdf from scipy ✓
- Clean implementation with proper d1/d2

### Q6 — Bisection IV (6/7)
- Bisection method implemented with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV and near-ATM averages reported
- **Minor**: No discussion of IV artifacts for extreme strikes

### Q7 — Newton/Secant + Timing (5/7)
- Newton method with analytical vega ✓
- Timing comparison: Newton ~5x faster than bisection
- **No Secant/Muller method**
- Timing numbers reported but minimal written analysis of convergence theory

### Q8 — IV Tables + Commentary (5/7)
- IV tables by maturity, type, and stock present
- Average vols computed
- Commentary covers basic required points (TSLA vs SPY, maturity effect)
- **Weakness**: Commentary is very minimal — mostly bullet points without numerical depth

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison with market values
- Brief analysis of deviations
- **Minor**: Could discuss American exercise premium

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D volatility smile for nearest maturity ✓
- Multi-maturity overlay with 3 colors ✓
- **3D volatility surface** implemented — earns bonus ✓
- Properly labeled axes

### Q11 — Greeks (5/5)
- Analytical Delta, Gamma, Vega correct
- Finite difference approximations computed
- Comparison table showing good agreement
- Applied to near-ATM options

### Q12 — DATA2 Pricing (3/5)
- DATA2 pricing with DATA1 IVs attempted
- BS prices computed
- **Weakness**: Comparison analysis is thin

---

## Part 3: AMM Fee Revenue (24/30)

### Q3a — Derive Swap Amounts (8/10)
- Both Case 1 and Case 2 derivations present
- Mathematical structure correct
- Swap amounts properly derived
- **Minor**: Could be more clearly presented

### Q3b — Expected Fee Revenue (8/10)
- Trapezoidal rule implemented ✓
- Lognormal density correctly handled
- Numerical results computed
- Adequate grid resolution

### Q3c — Optimal Fee Rate (8/10)
- σ×γ table computed ✓
- Optimal γ*(σ) found for each σ
- Plot produced ✓
- **Missing**: Written commentary on the observed pattern

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **3D volatility surface** is well-implemented — earns bonus
- Complete coverage of Parts 1-3 — all questions attempted
- Good Greeks comparison showing close analytical/FD agreement
- Newton timing comparison shows 5x speedup
- Code is functional throughout

## Weaknesses
- **Very minimal written analysis throughout** — submission is code-heavy with almost no prose
- **No Secant/Muller method** — only bisection and Newton
- No OCC option symbol discussion
- No explanation of many maturities
- Commentary in Q8 and Q3c is extremely thin
- Part 4 bonus not attempted
- Report format is code-centric — not a polished document

## AI Assessment: LOW
Code-heavy submission with minimal prose is consistent with a student who is comfortable coding but less inclined to write analysis. No obvious AI markers. The thin commentary throughout (which an AI would typically generate) and the missing Secant method suggest authentic student work.
