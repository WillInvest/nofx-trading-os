# Chopra, Rohan — FE621 HW1 Grading

**Final Score: 83/100 + 5 bonus = 83(+5)**

---

## Part 1: Data Gathering (15/20)

### Q1 — Download Function (4/5)
- `download_daily_data(target_dates, day)` uses yfinance for equity and option chain download
- `^IRX` (13-week Treasury bill) used for risk-free rate — appropriate external source
- `get_mid_price(row)` helper: checks bid/ask > 0, falls back to `lastPrice` — good data cleaning
- Third-Friday expiration filtering present
- **Minor**: VIX options NOT downloaded — only VIX spot level collected

### Q2 — Download Data (3/5)
- Two consecutive trading days: Feb 12 and Feb 13, 2026 ✓
- TSLA and SPY with full option chains, ^VIX spot only
- Third-Friday filtering for 3 monthly maturities ✓
- **Missing**: No CSV/Excel export functionality visible
- **Missing**: No explanation of why many more maturities exist (weeklies, LEAPs, quarterlies)

### Q3 — Written Descriptions (3/5)
- Basic descriptions of SPY and TSLA provided
- VIX described as volatility index
- **Missing**: No OCC option symbol format discussion
- Descriptions are adequate but not thorough

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded at download time ✓
- Interest rate from `^IRX` ✓
- Time to maturity computed ✓

---

## Part 2: Data Analysis (44/50)

### Q5 — Black-Scholes (7/7)
- BS call and put formulas correctly implemented from scratch
- Uses `norm.cdf` from scipy — follows assignment guidelines
- Clean implementation with proper d1/d2 calculations

### Q6 — Bisection IV (6/7)
- `bisection_method(func, a, b, tol=1e-6, max_iter=100)` with bracket `[0.0001, 5.0]`
- Applied to both TSLA and SPY ✓
- ATM IV filtering: moneyness band `(S/K >= 0.95) & (S/K <= 1.05)`
- Average ATM IV by maturity: SPY 8d: 0.2001, 36d: 0.1971, 64d: 0.1973 — reasonable and consistent
- **Minor**: Some TSLA deep OTM IVs exceed 100% — not filtered or discussed

### Q7 — Newton/Secant + Timing (5/7)
- Newton method with analytical `vega()`, guard `v < 1e-7`, initial guess σ=0.5
- **Timing: Bisection 4.45s vs Newton 2.76s** — Newton ~1.6x faster
- **Good written explanation**: "Newton's method converges faster than bisection because it uses the derivative..." — one of the better written convergence discussions
- **No Secant/Muller method** — only bisection and Newton

### Q8 — IV Tables + Commentary (5/7)
- IV tables by maturity, type, and stock present
- Average near-ATM vols computed
- **Commentary present**: Discusses VIX being lower than SPY IV suggesting calm conditions, "range-bound" trading analysis
- Covers TSLA vs SPY differences and VIX comparison — adequate but could be more detailed

### Q9 — Put-Call Parity (5/6)
- Correctly implemented C - P = S - K·e^(-rT) with `Theory_Put` and `Theory_Call`
- `.between(bid, ask)` validity check — verifies theoretical prices fall within market spread
- Scatter plot showing deviations — nice visualization
- **Minor**: No discussion of American exercise premium effects

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D volatility smile with blue/red/green for 3 maturities per ticker ✓
- Multi-maturity overlay ✓
- **3D scatter plots** for TSLA and SPY with viridis colormap — earns bonus ✓
- Professional matplotlib plotting with proper labels

### Q11 — Greeks (5/5)
- `delta_analytical`, `gamma_analytical`, `vega_analytical` all correctly implemented
- Finite differences: `delta_numerical(h=0.01)`, `gamma_numerical(h=0.01)`, `vega_numerical(h=0.001)` — appropriate step sizes
- Full 616-row comparison table across all options
- Avg absolute diffs: Delta 1.8e-10, Gamma 5.5e-6, Vega 2.5e-6 — excellent agreement
- Example: Delta analytical 0.94399 vs numerical 0.94399 — match to 5+ decimal places

### Q12 — DATA2 Pricing (5/5)
- Merges DATA1 IVs with DATA2 by (strike, expiration, type)
- `reprice_option(row)` uses DATA2 spot + DATA1 IV + current rate
- BS prices computed and compared with DATA2 market prices
- Error analysis present with pricing error table

---

## Part 3: AMM Fee Revenue (24/30)

### Q3a — Derive Swap Amounts (8/10)
- `swap_amounts_part_a(S_next, x_t, y_t, gamma)` with both Case 1 and Case 2
- Swap amounts Δx and Δy derived from constant product constraint and boundary conditions
- Mathematical structure correct
- **Minor**: Final expressions could be more clearly stated

### Q3b — Expected Fee Revenue (8/10)
- `expected_fee_revenue(gamma, sigma, n_points=10000)` with trapezoidal rule
- Lognormal density correctly computed
- 10,000 grid points — good resolution
- Results computed for given parameters

### Q3c — Optimal Fee Rate (8/10)
- Coarse σ×γ table with standard grid
- **Extended search**: `linspace(0.1, 1.0, 50)` for σ, `linspace(0.0005, 0.015, 50)` for γ — goes beyond basic 3-value grid
- Optimal γ*(σ) identified for each volatility level
- Plot produced ✓
- **Missing**: Detailed written commentary on the observed pattern

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **Greeks section is outstanding** — 616-row comparison table with avg diffs at machine-epsilon level (Delta 1.8e-10, Vega 2.5e-6)
- **3D volatility scatter plots** with viridis colormap — earns full Q10 bonus
- **Good Newton convergence explanation** — one of the better written discussions of why Newton is faster
- Put-call parity `.between(bid, ask)` validation with scatter plot — clean approach
- Extended gamma grid analysis in Part 3 shows initiative (linspace with 50 points)
- Consistent ATM IV values across maturities (SPY ~0.197-0.200) suggest clean data pipeline
- Good `get_mid_price()` helper with fallback logic

## Weaknesses
- **No Secant/Muller method** — only bisection and Newton
- **VIX options not downloaded** — only VIX spot level
- No CSV export functionality visible
- Missing explanation of why many maturities exist
- No OCC option symbol format discussion
- Some deep OTM IVs > 100% not filtered or discussed
- Part 4 bonus not attempted
- Newton speedup is modest (1.6x) compared to class average (~3-5x)

## AI Assessment: LOW
Code style is consistent with typical student work. The specific timing numbers (4.45s vs 2.76s) and 616-row Greeks table suggest genuine hands-on computation. The good written Newton convergence explanation shows understanding rather than AI boilerplate. No obvious AI-generation markers. Authentic student work.
