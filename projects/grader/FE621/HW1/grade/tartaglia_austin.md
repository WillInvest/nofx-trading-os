# Tartaglia, Austin — FE621 HW1 Grading

**Final Score: 90/100 + 2 bonus = 90(+2)**

*Grading updated after review of complement code (`complement/Tartaglia_Austin/hw1_submission/`).*

---

## Part 1: Data Gathering (18/20)

### Q1 — Download Function (4/5)
- **Code verified**: Full Python implementation using direct Yahoo Finance API (requests) — `YahooScraper` with `get_history`, `get_option_expiries`, `get_option_chain`
- Downloads equity OHLCV and option chains for TSLA, SPY; VIX spot via `download_vix()`
- **Third-Friday filtering**: `_select_monthly_expiries()` explicitly selects 3rd-Friday monthlies with fallback to next available expiries if fewer than n
- Saves to CSV in `config.OUTPUT_DIR`
- **Minor**: Uses direct API rather than yfinance; VIX options not downloaded (only spot level)

### Q2 — Download Data (4/5)
- Two consecutive trading days (5d history); TSLA, SPY, ^VIX
- Third-Friday maturities selected; option chains saved per ticker/expiry
- CSV/Excel export: equity history and options written to `output/`
- **Minor**: Fallback to weeklies when fewer than n monthly expiries — worth explaining in report

### Q3 — Written Descriptions (5/5)
- **Code verified**: `descriptions.py` — SPY, VIX, **OCC option symbol format** (ROOT+YYMMDD+C/P+STRIKE with example), and expiration rules (third Friday, holiday rule, weeklies/quarterlies)
- Thorough and assignment-compliant

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded at download; `config.RISK_FREE_RATE` (0.0364) and date noted
- TTM computed per expiry in chain processing (`(exp_dt - today).days / 365.0`)
- All required quantities present in pipeline and output

---

## Part 2: Data Analysis (45/50)

### Q5 — Black-Scholes (7/7)
- **Code verified**: `black_scholes.py` — from scratch using only `scipy.stats.norm`
- `bs_d1`, `bs_d2`, `bs_call_price`, `bs_put_price`, `bs_vega` correctly implemented; input validation
- Main.py includes sanity check vs textbook values ✓

### Q6 — Bisection IV (6/7)
- Bisection in `root_finding.py` (tol=1e-6, max_iter=1000); `implied_vol.py` uses `config.TOLERANCE`
- ATM IV and near-ATM band summary in `atm_summary()`; applied to TSLA and SPY
- **Minor**: Extreme IVs could be filtered or discussed

### Q7 — Newton/Secant + Timing (7/7)
- **All three methods**: `bisection`, `newton`, `secant` in `root_finding.py`; Newton uses analytical vega
- `compute_iv_bisection`, `compute_iv_newton`, `compute_iv_secant` in `implied_vol.py`; `compute_all_ivs` runs all three and records iters/time
- `convergence_summary()` prints avg iterations and avg time (ms) per method with brief commentary ✓

### Q8 — IV Tables + Commentary (5/7)
- IV tables by ticker/expiry/type; ATM and VIX comparison in `vix_comparison()`; TSLA vs SPY average IV and commentary in code
- Adequate; could add more numerical detail in report

### Q9 — Put-Call Parity (5/6)
- **Code verified**: `put_call_parity.py` — correct C − P = S − K·e^(-rT); `verify_parity()` merges calls/puts by strike, computes parity put/call and error
- Mean/max |parity error| reported. Report "N/A" may have been from an older run or empty merge; implementation is correct ✓

### Q10 — Vol Smile Plots (6/6)
- **Code verified**: `vol_surface.py` — 2D IV vs strike (nearest expiry), 2D all expiries overlay, **and 3D surface** (`plot_3d_surface`: scatter + interpolated surface via griddata)
- Saves per-ticker PNGs to output ✓

### Q11 — Greeks (5/5)
- **Code verified**: `greeks.py` — analytical delta (call/put), gamma, vega; numerical with **correct step sizes**: `h = 0.01*S` for delta/gamma, `h = 0.001` for vega
- Comparison table for ~ATM options; output to CSV ✓

### Q12 — DATA2 Pricing (4/5)
- **Code verified**: `data2_pricing.py` — reprice with IV from DATA1, T_new = T_orig − 1/252
- **Note**: Code uses single `spots` dict (S_data1 = S_data2 = spots[ticker]); for true DATA2 (second day) a second spot snapshot would be needed. Logic for T and IV is correct ✓

---

## Part 3: AMM Fee Revenue (20/30)

### Q3a — Derive Swap Amounts (4/10)
- **Code verified**: `amm_fee_revenue.py` implements CPMM no-arb band and fee revenue: Case 1 (S_next > upper): x_new, y_new, δy; Case 2 (S_next < lower): x_new, δx; formulas consistent with CPMM
- **Gap**: No mathematical derivation of Δx, Δy (or x_new, y_new) shown in report or in code comments — derivation still missing for full credit

### Q3b — Expected Fee Revenue (8/10)
- Trapezoidal integration over lognormal density (`lognormal_pdf`, `expected_fee_revenue`); vectorized `fee_revenue_vectorized` for grid
- Numerical result for sigma=0.2, gamma=0.003 reported ✓

### Q3c — Optimal Fee Rate (8/10)
- σ×γ table via `compute_fee_table`; `optimal_gamma()` finds γ*(σ); plot saved (`amm_optimal_gamma.png`) with commentary ✓

---

## Part 4: Bonus (7/10)

### Analytical Solutions (2/3)
- **Code verified**: `bonus_integration.py` — exact values stated for f1(x,y)=xy and f2(x,y)=e^(x+y) (Rouah reference)
- **Minor**: No analytical derivation (integration steps) shown in report

### Numerical Implementation (5/7)
- Composite double trapezoidal rule (Rouah formula); four (dx, dy) grid pairs; error comparison table for both functions
- Convergence with finer grid shown ✓

---

## Strengths
- **Full, modular codebase** — data_gathering, black_scholes, root_finding, implied_vol, put_call_parity, greeks, vol_surface, data2_pricing, amm_fee_revenue, bonus_integration, all with clear structure and comments
- **All three root-finding methods** (bisection, Newton, Secant) implemented and compared
- **3D volatility surface** in addition to 2D plots
- **Correct Greeks** with appropriate finite-difference step sizes
- **OCC option format and expiration rules** in Q3; thorough Part 3 implementation and Part 4 bonus
- **Third-Friday monthly selection** with explicit calendar logic

## Weaknesses
- **Q3a**: Mathematical derivation of swap amounts (Δx, Δy) still not shown — only implementation
- **Report/PDF**: Original submission had no code in the PDF; grading was revised after reviewing complement code. For future assignments, including key code snippets or referencing the submitted files explicitly in the report would avoid ambiguity
- **DATA2**: Single spot snapshot in code — if assignment required two different trading days, a second spot load would be needed
- **Part 4**: Analytical derivation of exact integrals could be written out in the report

## AI Assessment: LOW
Code structure, variable names, and the mix of correct implementations with specific bugs/omissions (e.g., missing derivation, single-spot DATA2) are consistent with authentic student work. No signs of wholesale AI generation.
