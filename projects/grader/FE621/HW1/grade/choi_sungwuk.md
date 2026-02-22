# Choi, Sungwuk — FE621 HW1 Grading (LATE)

**Final Score: 66/100 + 0 bonus = 66**

---

## Part 1: Data Gathering (16/20)

### Q1 — Download Function (4/5)
- `download_equity(symbol)` uses `yf.Ticker` with `history(period="1d", interval="1m")` — functional 1-minute intraday download
- `get_monthly_expirations(ticker)` correctly filters third-Friday expirations via `weekday() == 4 and 15 <= day <= 21`
- `download_option_chain(symbol)` concatenates calls/puts with type labels, filters `volume > 0` and `bid > 0 & ask > 0` — good data cleaning
- FRED API key hardcoded directly in source (`FRED_API_KEY = "0fa4f50d7dcb..."`) — bad practice, should use environment variable
- Saves to CSV with metadata file containing download time, rate, and spot prices — well-organized

### Q2 — Download Data (3/5)
- Downloaded TSLA, SPY, ^VIX for 2 consecutive days (DATA1 and DATA2 CSVs present in complement)
- Third-Friday filtering correctly implemented
- **Missing**: No explanation of why many more maturities exist beyond traditional monthly (weeklies, LEAPs, quarterlies, end-of-month)
- Download timing not explicitly stated in report — complement metadata CSVs confirm the data exists

### Q3 — Written Descriptions (2/5)
- Report is extremely brief — Part 1 is a single paragraph covering all of Q1-Q4 together
- No dedicated description of SPY as an ETF, no definition of ETF
- No description of ^VIX as a volatility index
- No discussion of option symbol format (OCC convention)
- Korean placeholder text `[여기에 입력]` left in the document header — unprofessional

### Q4 — Record Prices, Rate, TTM (5/5)
- Fed funds rate from FRED API: `DFF` series, divided by 100 to convert from percent
- Spot prices recorded via metadata CSV
- TTM calculated as `max(delta.days/365, 1e-8)` — calendar-day approach with floor to avoid zero

### Bonus (2/5)
- Multi-asset download built into the function (`for sym in ["TSLA", "SPY"]`) with CSV export — partially satisfies bonus

---

## Part 2: Data Analysis (37/50)

### Q5 — Black-Scholes (6/7)
- `black_scholes(S, K, T, r, sigma, option_type)` correctly implements d1/d2 with `norm.cdf`
- Handles T ≤ 0 edge case: returns `max(S-K, 0)` for calls, `max(K-S, 0)` for puts — good intrinsic value fallback
- Uses numpy throughout — clean implementation

### Q6 — Bisection IV (5/7)
- `implied_vol_bisection(S, K, T, r, market_price, option_type)` — pure bisection with `lower=1e-6`, `upper=5.0`, `tol=1e-6`, `max_iter=100`
- Convergence via `abs(diff) < tol` ✓
- ATM average IV computed in 0.95-1.05 moneyness band
- TSLA ATM Avg IV: 0.4356, SPY ATM Avg IV: 0.4784 — reported
- **Problem**: Upper bound of 5.0 (500%) means deep OTM options with no valid IV return `mid` at 5.0, contaminating averages. SPY short-dated IVs reach >1.0 — student doesn't filter or acknowledge these artifacts

### Q7 — Newton/Secant + Timing (5/7)
- `implied_vol_newton` with analytical `vega(S, K, T, r, sigma)` = S·√T·φ(d1) ✓
- Sigma clamping: `if sigma <= 0: sigma = 1e-6` — prevents negative drift
- Vega guard: `if abs(v) < 1e-8: break` ✓
- Timing comparison present: Bisection IV: 0.4317, Newton IV: 0.4317; Bisection time: 0.0022s, Newton time: 0.0002s — Newton ~10x faster
- **No Secant/Muller method** — only bisection and Newton implemented
- No written discussion of *why* Newton is faster (quadratic convergence)

### Q8 — IV Tables + Commentary (4/7)
- Tables present: TSLA Maturity IV and SPY Maturity IV grouped by expiration
- Call vs Put IV tables for both tickers shown
- Commentary is **extremely thin** — only 3 sentences:
  - "volatility is not flat over time"
  - "Comparing with VIX level gives an idea how different the index volatility can be"
  - No specific numerical comparisons, no TSLA vs SPY discussion
- VIX level referenced but not meaningfully compared

### Q9 — Put-Call Parity (4/6)
- `check_put_call_parity(df, S, r, current_time)` correctly computes `lhs = C - P` vs `rhs = S - K·exp(-rT)`
- TSLA Parity Mean Diff: 1.633, SPY Parity Mean Diff: 1.067 — relatively large
- Brief commentary: "average difference are small but not exactly zero... likely comes from bid-ask spread and small market frictions" — reasonable but doesn't mention American exercise premium
- Only mean difference reported, no per-strike or per-maturity breakdown

### Q10 — Vol Smile Plots (4/6)
- 2D scatter plots: SPY IV Smile and TSLA IV Smile with 3 maturities in different colors ✓
- Multi-maturity overlay present ✓
- Commentary: "curved shape instead of flat line... consistent with what is usually observed" — minimal
- **No 3D surface plot** (bonus not attempted)
- IV scale goes up to 5.0 on y-axis — the contaminated high IVs are visible but not filtered or discussed

### Q11 — Greeks (5/5)
- `greeks_call(S, K, T, r, sigma)` returns analytical Delta (`norm.cdf(d1)`), Gamma (`norm.pdf(d1)/(S·σ·√T)`), Vega (`S·√T·norm.pdf(d1)`) — all correct
- Finite difference: `delta_fd_call` (central, h=1e-4), `gamma_fd_call` (central), `vega_fd_call` (central, h=1e-4) ✓
- Comparison table: Delta 0.5266/0.5266, Gamma 0.01499/0.01499, Vega 24.491/24.491 — excellent agreement
- Clean `compare_greeks_call` wrapper function

### Q12 — DATA2 Pricing (4/5)
- Merges DATA1 IVs with DATA2 by (strike, expiration, type)
- Computes BS theoretical prices using DATA2 spot, DATA1 IV, DATA2 rate
- Pricing error table shown with `theoretical_price`, `market_price`, `pricing_error` columns
- Brief commentary: "theoretical prices does not perfectly match the new market prices, which reflects market movement and model limitation"
- Output table only shows head() — not comprehensive

---

## Part 3: AMM Fee Revenue (20/30)

### Q3a — Derive Swap Amounts (7/10)
- Handwritten derivation in appendix covering both Case 1 and Case 2
- Case 1: boundary condition y_{t+1}/x_{t+1} = S_{t+1}(1-γ), solves for x_{t+1} = √(k/((1-γ)·S)) and Δx = x_t - x_{t+1}
- Case 2: similar structure with x_{t+1} = √(k·(1-γ)/S)
- Derivation is on the right track but **hard to follow** — handwriting is somewhat messy
- Final expressions not cleanly boxed/stated

### Q3b — Expected Fee Revenue (7/10)
- `expected_fee_trap(S0, x0, y0, gamma, sigma, dt, n)` implemented using `scipy.integrate.trapezoid`
- Lognormal density via standard normal transformation: `z = linspace(-4, 4, n)`, `S = S0·exp(m + sd·z)` with `m = -0.5·σ²·dt` ✓
- Integration over z-space rather than S-space — valid approach
- Expected fee = 0.01307 reported for baseline parameters
- Only computes one case (dx → R for Case 1) — should handle both cases but appears to work

### Q3c — Optimal Fee Rate (6/10)
- σ×γ table present: σ ∈ {0.2, 0.6, 1.0}, γ ∈ {0.001, 0.003, 0.01}
- All σ values give `best gamma = 0.01` — this is the class-wide pattern from the coarse grid
- Extended grid search: `sigma_grid = linspace(0.1, 1.0, 20)`, optimal gamma selected via `argmax`
- Plot of σ vs γ* produced ✓
- Brief commentary: "numerical results select the highest candidate γ in the tested set for all volatility levels, which may reflect the simplified integration approach" — acknowledges the issue
- **No detailed written analysis** of the pattern

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- Complete coverage of Parts 1-3 — all questions attempted with working code
- Greeks section shows excellent analytical/FD agreement (6 decimal places matching)
- FRED API integration for interest rate is well-implemented
- Part 3 trapezoidal integration uses standard normal transformation — shows mathematical understanding
- Code is functional and clearly structured across 3 separate .py files
- Metadata CSV approach is well-organized for data management

## Weaknesses
- **Korean placeholder text `[여기에 입력]`** left in document header — unprofessional
- **Written analysis is extremely thin throughout** — most questions have 1-3 sentences of commentary
- **No Secant/Muller method** implemented
- **Bisection upper bound of 5.0** causes IV contamination for deep OTM options — IVs > 1.0 visible in plots but never addressed
- No explanation of why many maturities exist (weeklies, LEAPs)
- No SPY/VIX/option symbol descriptions (Q3 largely missing)
- Put-call parity differences (>1.0) not adequately explained (American exercise premium)
- No 3D volatility surface (bonus not attempted)
- Report format is minimal — screenshots of terminal output, not a polished LaTeX/Word document
- No Part 4 bonus attempted

## AI Assessment: LOW
Strong human indicators: typo `"Newton Methodi"` in code comment; FRED API key hardcoded directly in source; Korean placeholder text `[여기에 입력]`; no docstrings; casual coding style with minimal comments; code separated into 3 simple .py files without abstraction. Authentic student work.
