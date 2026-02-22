# Hsieh, Tzuling — FE621 HW1 Grading

**Final Score: 85/100 + 9 bonus = 85(+9)**

---

## Part 1: Data Gathering (18/20)

### Q1 — Download Function (5/5)
- Python download function using yfinance — functional and well-structured
- Downloads equity and option chains for TSLA, SPY, ^VIX
- Third-Friday expiration filtering correctly implemented
- CSV output for equity and option data

### Q2 — Download Data (4/5)
- DATA1 clearly present with proper data
- Third-Friday filtering for 3 monthly maturities ✓
- **Issue**: Only 1 day of data clearly demonstrated in report; DATA2 exists in complement CSVs
- **Missing**: No explicit explanation of why many more maturities exist

### Q3 — Written Descriptions (5/5)
- Good descriptions of all symbols
- **Option symbol format explained** — one of few students to discuss OCC convention
- SPY as ETF, VIX as volatility index properly described
- Expiration mechanics discussed

### Q4 — Record Prices, Rate, TTM (4/5)
- Spot prices recorded ✓
- Interest rate from Fed funds ✓
- TTM correctly computed ✓
- **Minor typo**: "Queation" instead of "Question"

---

## Part 2: Data Analysis (41/50)

### Q5 — Black-Scholes (7/7)
- BS call and put correctly implemented
- Uses norm.cdf from scipy ✓
- Handles calls and puts with correct formulas
- Clean implementation

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV and near-ATM averages reported
- **Minor**: Some options return NaN due to data issues

### Q7 — Newton/Secant + Timing (5/7)
- Newton method implemented with analytical vega
- **Problem**: Newton has **131 "vega is zero" failures** for OTM options — root cause is missing sigma clamping after update step. When Newton overshoots to negative sigma, the guard `if sigma <= 0: return 0.0` in vega triggers, causing cascading failures
- Timing comparison present
- **No Secant/Muller method**
- Student doesn't diagnose or acknowledge the extensive Newton failures

### Q8 — IV Tables + Commentary (5/7)
- IV tables by maturity, type, and stock present
- Average vols computed
- Commentary covers required points (TSLA vs SPY, VIX comparison, maturity effect)
- Analysis is adequate but could include more specific numbers

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison with market values
- Analysis present
- **Minor**: Discussion could be more thorough

### Q10 — Vol Smile Plots (5/6)
- 2D volatility smile present ✓
- Multi-maturity overlay with different colors ✓
- No 3D surface (bonus not attempted here)
- Written observation of smile shapes present

### Q11 — Greeks (4/5)
- Analytical + FD Greeks computed
- Comparison table present
- Differences show 0.0 (rounding to display precision) — confirms agreement
- **Minor**: Showing 0.0 differences instead of actual small values hides the true FD error magnitude

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs implemented
- BS prices computed and compared
- Some options affected by Newton failures from Q7
- Basic comparison analysis present

---

## Part 3: AMM Fee Revenue (28/30)

### Q3a — Derive Swap Amounts (9/10)
- Thorough derivations for both Case 1 and Case 2
- Clear mathematical presentation
- Final expressions stated
- Well-organized

### Q3b — Expected Fee Revenue (10/10)
- Trapezoidal rule correctly implemented
- Lognormal density properly handled
- Numerical results computed with adequate grid resolution
- Well-presented results

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table computed ✓
- Optimal γ*(σ) found for each σ
- Plot produced ✓
- **Good commentary** on the observed pattern — better than most students
- **Minor**: Could explore extended gamma range

---

## Part 4: Bonus (9/10)

### Analytical Solutions (3/3)
- f1 = xy: 9/4 ✓
- f2 = e^(x+y): correctly evaluated ✓

### Numerical Implementation (6/7)
- 4 grid sizes tested ✓
- f1 gives exact results — **student explains why** (composite formula is exact for bilinear functions) ✓
- f2 shows clean convergence ✓
- Commentary on convergence behavior present — one of few students to explain the f1 exactness
- **Minor**: Could include error plot

---

## Strengths
- **Part 3 is one of the strongest in the class** — thorough derivations, correct implementation, good commentary
- **Part 4 bonus includes explanation of why f1 is exact** — shows deeper mathematical understanding
- **Option symbol format explained** in Q3 — rare among students
- Well-organized report with clear structure
- Strong overall score across all parts

## Weaknesses
- **131 Newton "vega is zero" failures** — trivially fixable with sigma clamping (`sigma = max(0.001, sigma)`) but student never diagnosed the issue
- **No Secant/Muller method**
- Greeks comparison shows "0.0" differences — hides actual FD error magnitudes
- Only 1 day of data clearly shown in report (DATA2 in complement only)
- Some Newton-affected IVs contaminate downstream results (Q8, Q12)
- Typo "Queation" in headers
- Missing appendix with full code as mentioned in report

## AI Assessment: LOW
Strong human indicators: **bilingual Chinese/English comments** (`總寬度`, `轉成微秒`, `若未收斂`) scattered through complement code — clearly a native Chinese speaker's working notes. ESL typos ("bond" for "bound", "Calsculate"), unresolved Newton bug output left in notebook, messy iterative Jupyter development pattern. Not AI-generated.
