# Khosla, Tasha — FE621 HW1 Grading

**Final Score: 80/100 + 0 bonus = 80**

---

## Part 1: Data Gathering (17/20)

### Q1 — Download Function (4/5)
- Well-structured download script using `pathlib.Path`, `os.makedirs(exist_ok=True)` — notably polished
- Uses yfinance with `fast_info` fallback chain for spot prices
- Third-Friday filtering implemented
- Code in separate `part1.py` file, not shown in LaTeX report PDF
- **Minor**: Code not verifiable from PDF alone

### Q2 — Download Data (4/5)
- Two consecutive trading days downloaded ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- **Missing**: No explanation of why many more maturities exist

### Q3 — Written Descriptions (4/5)
- LaTeX report with proper formatting
- Descriptions of SPY, TSLA, VIX provided
- **Missing**: OCC option symbol format not discussed

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Fed funds rate ✓
- TTM correctly computed ✓
- Well-presented in LaTeX format

---

## Part 2: Data Analysis (36/50)

### Q5 — Black-Scholes (7/7)
- BS formula correctly implemented in `part2.py`
- `get_bs_call_or_put_fn` returns closures — somewhat sophisticated pattern
- Uses `math` module for scalar operations (not numpy) — valid choice
- **Minor**: `Callable[float]` type hint is incorrect (should be `Callable[[float], float]`) — genuine mistake

### Q6 — Bisection IV (6/7)
- Bisection implemented with tolerance 1e-6 ✓
- Applied to TSLA and SPY ✓
- ATM IV reported: TSLA bisection ATM ≈ 0.42
- **Problem**: Many IVs hit upper bound of 5.0 — contaminated results for deep OTM options

### Q7 — Newton/Secant + Timing (4/7)
- Newton implemented
- **CRITICAL BUG**: Missing `abs()` in convergence check — `if numerator < tolerance` instead of `if abs(numerator) < tolerance`. For puts where BS price > market price, the numerator is negative and never satisfies `< tolerance`, so Newton iterates to max_iterations and returns poorly converged values
- This directly explains the **TSLA ATM discrepancy**: Newton IV = 0.2 vs bisection IV = 0.42
- **No Secant/Muller method**
- Timing comparison present but Newton results are unreliable due to bug

### Q8 — IV Tables + Commentary (4/7)
- IV tables present
- Average vols reported
- Commentary addresses required points but affected by Newton bug contamination
- The Newton/bisection discrepancy is visible but not diagnosed

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison with market values
- Analysis present

### Q10 — Vol Smile Plots (4/6)
- 2D plots present ✓
- Multi-maturity overlay ✓
- No 3D surface
- Plots may show contaminated IVs (5.0 boundary hits)

### Q11 — Greeks (4/5)
- Analytical + FD Greeks computed
- Comparison showing agreement
- Applied to near-ATM options
- **Minor**: Results may be affected by incorrect IV inputs

### Q12 — DATA2 Pricing (2/5)
- Attempted but results compromised by Newton convergence bug
- IVs used for pricing include incorrectly converged values
- Basic structure correct but output unreliable

---

## Part 3: AMM Fee Revenue (27/30)

### Q3a — Derive Swap Amounts (9/10)
- Thorough derivations for both Case 1 and Case 2
- **Boxed results** — professional LaTeX presentation
- Mathematical structure correct and clearly stated

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal rule with **1 million grid points** — more than sufficient for accuracy
- Lognormal density correctly handled
- Proper bounds for Case 1 and Case 2 integrals separately
- Correct math with separate integrals for each case

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table computed ✓
- Extended search present
- Plot produced ✓
- Good presentation
- **Minor**: Commentary could be more detailed

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **Part 3 is excellent** — thorough derivations with boxed results, 1M grid points for trapezoidal, professional LaTeX presentation
- **LaTeX report format** — one of the more professionally presented submissions
- Clean functional code design with closure-based patterns in `part2.py`
- Python 3.10+ type hints (`tuple[str, str]`, `float | None`) throughout
- Clean `pathlib` usage in data handling

## Weaknesses
- **Newton convergence bug** — missing `abs()` causes TSLA ATM IV = 0.2 vs correct 0.42. This cascades into unreliable Q8 averages and Q12 pricing
- **Many IVs hit 5.0 boundary** — from both the Newton bug and bisection upper bound
- **No Secant/Muller method**
- **Code not shown in PDF** — separate .py files referenced but not included in the report
- No 3D volatility surface
- No explanation of many maturities
- Part 4 bonus not attempted
- The Newton bug is the single largest issue — a trivial fix (`abs()`) would have substantially improved the score

## AI Assessment: LOW-MODERATE
Code is notably more polished than average student: consistent Python 3.10+ type hints, clean `pathlib` usage, closure-based design patterns in `get_bs_call_or_put_fn`. However, the missing `abs()` bug and incorrect `Callable[float]` annotation are genuine mistakes an AI would be unlikely to make. No docstrings, sparse comments. The polished style could indicate Copilot-assisted editing rather than wholesale generation. Likely student-written with possible IDE-level AI assistance (Copilot autocomplete).
