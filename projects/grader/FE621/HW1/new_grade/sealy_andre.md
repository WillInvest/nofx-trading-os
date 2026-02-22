# Sealy, Andre — FE621 HW1 Grading

**Final Score: 76/100 + 0 bonus = 76**

---

## Part 1: Data Gathering (19/20)

### Q1 — Download Function (5/5)
- Well-organized project structure with separate .py files by question number (1.1, 1.2, 2.1-2.6, 3.2, 3.3)
- Uses yfinance for download
- Git repository maintained
- Shared `black_scholes.py` module — modular design

### Q2 — Download Data (5/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓
- `1.2_download_vix.py` downloads VIX data (copy-pasted 3-line pattern 6 times instead of loop — clearly human)

### Q3 — Written Descriptions (4/5)
- LaTeX report format — professional presentation
- SPY, TSLA, VIX described
- **Minor**: OCC format could be more detailed

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

---

## Part 2: Data Analysis (35/50)

### Q5 — Black-Scholes (7/7)
- `black_scholes.py` — shared module with correct BS formula
- Handles calls and puts
- Clean modular design

### Q6 — Bisection IV (5/7)
- Bisection implemented in `2.1_bisection_method.py`
- **Problem**: File imports `from bisection import implied_vol` but **no `bisection.py` exists** in submission — the driver script cannot actually run
- Suspicious unused import: `from pandas.core.base import SelectionMixin` — likely autocomplete pollution
- Tolerance 1e-6 ✓

### Q7 — Newton/Secant + Timing (3/7)
- `newton_raphson.py` is a **generic root-finder** using central finite differences `(f(x+dx) - f(x-dx)) / (2*dx)` with `dx=1e-5`
- **Does NOT use analytical vega** for IV solving, even though student knows the formula (appears in `2.5_greeks.py`)
- Using FD instead of analytical vega is a lazy but functional design choice
- **No Secant/Muller method**
- **No timing numbers** shown in the report — assignment requires timing comparison
- `x != x` NaN check idiom — unusual pattern

### Q8 — IV Tables + Commentary (4/7)
- IV tables present
- Average vols computed
- **Only 1 IV plot shown** — should have multiple maturity overlays
- Commentary thin

### Q9 — Put-Call Parity (4/6)
- Implementation in `2.3_call_put_parity.py`
- `.copy()` misplacement bug — doesn't affect correctness but shows sloppy code
- Comparison present
- Brief analysis

### Q10 — Vol Smile Plots (3/6)
- Only 1 IV plot shown
- **No multi-maturity overlay** (or not clearly shown)
- **No 3D surface**
- Incomplete sentence on p.10 of report

### Q11 — Greeks (5/5)
- **`2.5_greeks.py`** demonstrates analytical BS greeks + FD comparison
- Correct Delta, Gamma, Vega formulas
- FD with central differences
- **AI RED FLAG**: Line 246 contains `"--- Replace your __main__ block with this (computes BOTH analytic and FDM greeks for calls+puts) ---"` — this is an **AI assistant instruction** (ChatGPT/Copilot) the student forgot to remove
- Redundant re-imports inside `__main__` (numpy, pandas) confirm pasted block
- Despite the AI assistance, the Greeks section itself is correct

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing implemented in `2.6` file
- BS prices computed with DATA1 IVs
- Comparison present
- `price_dff_day2` typo in variable name

---

## Part 3: AMM Fee Revenue (27/30)

### Q3a — Derive Swap Amounts (9/10)
- Both cases addressed
- Derivation present
- Well-structured

### Q3b — Expected Fee Revenue (9/10)
- Trapezoidal implementation
- Numerical results computed
- Correct implementation

### Q3c — Optimal Fee Rate (9/10)
- σ×γ table ✓
- Good commentary on **volatility harvesting** — unique insight in the class
- Plot produced ✓
- Crude 3-point gamma optimization

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **Part 3 commentary on volatility harvesting** — unique insight, shows deeper DeFi understanding
- **Well-organized project structure** with separate files per question and shared modules
- **Git repository** maintained — professional development practice
- LaTeX report format
- Greeks computation is correct (despite AI assistance on that section)

## Weaknesses
- **Newton uses FD instead of analytical vega** — the student clearly knows the vega formula (in `2.5_greeks.py`) but chose to use a generic FD root-finder. Lazy design choice
- **Missing `bisection.py` dependency** — `2.1_bisection_method.py` cannot run as submitted
- **No timing comparison** shown in report
- **AI instruction left in code**: `"Replace your __main__ block with this"` in `2.5_greeks.py` — definitive proof of AI assistance on Greeks section
- **No Secant/Muller method**
- Only 1 IV plot shown — inadequate for Q10
- Incomplete sentence on p.10
- Copy-paste patterns: `select_option_type` copied across 5 files instead of shared module
- Typos: "seperated", "similiar", "price_dff_day2"
- No 3D surface, no Part 4 bonus

## AI Assessment: LOW-MODERATE (~30-35%)
Primarily student-written with **confirmed selective AI assistance**. The leftover ChatGPT instruction in `2.5_greeks.py` line 246 (`"Replace your __main__ block with this"`) is definitive proof of at least partial AI usage. Redundant re-imports inside `__main__` confirm the block was pasted from an AI conversation. The `x != x` NaN check idiom in `newton_raphson.py` is a pattern commonly seen in AI-generated code. However, pervasive typos ("seperated", "similiar"), copy-paste patterns (function duplicated across 5 files), missing `bisection.py` dependency, and real bugs are all consistent with authentic student work. The student likely wrote most code themselves and used ChatGPT to help with the Greeks computation. **Not wholesale AI-generated, but has confirmed evidence of targeted AI assistance.**
