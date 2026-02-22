# Gahan, Cian — FE621 HW1 Grading (LATE)

**Final Score: 53/100 + 3 bonus = 53(+3)**

---

## Part 1: Data Gathering (15/20)

### Q1 — Download Function (4/5)
- `BlackScholes` class in companion notebook is well-structured with `@staticmethod` methods
- Data download code references Bloomberg-like API externally
- Third-Friday filtering present
- **Issue**: Used **SPX instead of SPY** — student explicitly acknowledges this in a prominent red NOTE, arguing results should be "very similar." Technically SPX (European) is more appropriate for BS, but assignment specified SPY

### Q2 — Download Data (3/5)
- Two consecutive days of data collected
- SPX used instead of SPY (acknowledged error)
- Third-Friday expirations filtered
- **Missing**: Explanation of why many maturities exist

### Q3 — Written Descriptions (4/5)
- Descriptions present but in conversational/personal style
- SPY/SPX, VIX, TSLA described
- Missing OCC symbol format discussion
- Writing style is informal: "I misread the assignment instructions"

### Q4 — Record Prices, Rate, TTM (4/5)
- Spot prices recorded
- Interest rate sourced
- TTM computed
- **Minor**: `np.max(value, 0)` should be `np.maximum(value, 0)` — `np.max` treats second arg as `axis`

---

## Part 2: Data Analysis (34/50)

### Q5 — Black-Scholes (7/7)
- `BlackScholes` class with `_d1_d2` helper, `call_price()`, `put_price()` — well-organized
- Correct d1/d2 formulas
- Clean single-class design with shared helper methods

### Q6 — Bisection IV (6/7)
- Bisection IV solver implemented within `BlackScholes` class
- Tolerance 1e-6, applied to options ✓
- ATM IV reported
- Applied to both tickers ✓

### Q7 — Newton/Secant + Timing (5/7)
- Newton IV solver implemented with analytical vega ✓
- Timing comparison present
- **No Secant/Muller method**
- Newton has RuntimeWarning: divide-by-zero/overflow due to no sigma clamping when Newton overshoots to negative

### Q8 — IV Tables + Commentary (4/7)
- IV tables generated
- Commentary is conversational and thin
- Some analysis of TSLA vs SPX differences
- **Not comprehensive** — lacks specific numerical comparisons

### Q9 — Put-Call Parity (4/6)
- Implementation present
- Comparison with market values
- Brief commentary

### Q10 — Vol Smile Plots (4/6)
- 2D plots generated
- Multi-maturity overlay present
- No 3D surface (bonus not attempted)
- No written analysis of smile shapes

### Q11 — Greeks (0/5)
- **Code is fully implemented** in the `BlackScholes` class — both analytical (`delta()`, `gamma()`, `vega()`) and FD methods
- **BUT**: Application cell contains only `# TODO: choose options subset to calculate greeks on; compare results for each` — **NEVER EXECUTED**
- Cannot award points for unexecuted code with only a TODO placeholder

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing attempted with DATA1 IVs
- BS prices computed
- Comparison with market prices
- **Minor**: Results may be affected by SPX vs SPY mismatch

---

## Part 3: AMM Fee Revenue (4/30)

### Q3a — Derive Swap Amounts (4/10)
- Substantial handwritten derivations for Case 1 using quadratic formula approach
- Case 2 partially addressed
- Mathematical structure on the right track
- **Incomplete**: Derivation trails off mid-work; final clean expressions not stated

### Q3b — Expected Fee Revenue (0/10)
- **Entirely missing.** No code, no numerical results. Student writes "unable to finish"

### Q3c — Optimal Fee Rate (0/10)
- **Entirely missing.** No σ×γ table, no optimal γ*(σ), no plot, no commentary

---

## Part 4: Bonus (3/10)

### Analytical Solutions (3/3)
- f1 = xy: ∫₀¹∫₀³ xy dy dx = 9/4 ✓
- f2 = e^(x+y): correctly evaluated ✓

### Numerical Implementation (0/7)
- Code for `trapezoid_integrate` present but **has a critical bug**: uses numpy array variables `x`, `y` instead of loop scalars `xi`, `yi` in the `4*f(x+dx/2, y+dy/2)` midpoint term
- This causes the function to return arrays instead of scalar sums — completely incorrect output
- Student didn't catch the bug in their output

---

## Strengths
- `BlackScholes` class is well-structured with clean OOP design — `_d1_d2` helper, `@staticmethod` methods
- Analytical solutions for bonus integrals are correct
- Honest about mistakes — "I misread the assignment instructions" regarding SPX vs SPY
- Greeks code is fully implemented (just never applied)
- Bisection and Newton implementations are functional

## Weaknesses
- **Q11 Greeks UNEXECUTED** — 5-point loss from a TODO placeholder. The code exists in the class but was never applied
- **Part 3 almost entirely missing** — only partial Q3a derivation, Q3b and Q3c both "unable to finish." 20+ points lost
- **SPX instead of SPY** — acknowledged error but still a deviation from assignment spec
- **Part 4 numerical bug** — `trapezoid_integrate` uses wrong variables, producing garbage output
- `np.max(value, 0)` bug — should be `np.maximum(value, 0)`
- Newton RuntimeWarnings from no sigma clamping
- Sections trail off mid-work — submission feels rushed/incomplete
- Report has incomplete sections and conversational tone

## AI Assessment: LOW
Strong human indicators: personal/conversational writing style ("I misread the assignment instructions", "Was unable to finish"), inconsistent code style (f-strings mixed with string concatenation), sparse practical comments, genuine TODO markers with unfinished work, incomplete sections that trail off mid-work, real bugs persist in output (trapezoid arrays, np.max), MacOS file paths confirm personal machine. Not AI-generated.
