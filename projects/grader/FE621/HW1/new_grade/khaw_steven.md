# Khaw, Steven — FE621 HW1 Grading

**Final Score: 86/100 + 8 bonus = 86(+8)**

---

## Part 1: Data Gathering (15/20)

### Q1 — Download Function (5/5)
- `get_ohlcv()` — clean multi-ticker OHLCV download via `yf.download()`, saves to CSV with auto-generated timestamped filename. Handles both single string and list input.
- `get_options()` — downloads option chains for multiple tickers, filters for third-Friday expirations via `valid_friday()`, attaches spot price and timestamp to each row. Saves to CSV.
- Both functions support multi-asset in a single call, satisfying the **bonus** requirement. The code is well-commented and production-quality for a student.

### Q2 — Download Data (4/5)
- Two consecutive days: `saved_options_2026-02-04_1834.csv` (DATA1) and `saved_options_2026-02-05_1754.csv` (DATA2) — dates before Feb 14 ✓
- Downloaded TSLA, SPY, ^VIX ✓
- Third-Friday filtering correct via `valid_friday(ts)` checking `weekday() == 4` and `15 <= day <= 21` ✓
- **Issue**: Download times 18:34 and 17:54 are after trading hours (9:30am-4:00pm), so these aren't "during the trading day" as specified
- **Missing**: No explanation of why many maturities exist beyond traditional third-Fridays (weeklies, LEAPs, end-of-month, quarterlies, etc.)

### Q3 — Written Descriptions (1/5)
- **Mostly absent.** The submission is a Jupyter notebook export with code cells dominating. No dedicated markdown/text cells providing the required paragraph describing SPY (ETF definition), ^VIX (volatility index), option symbol format, or expiration mechanics.
- The only textual content comes from inline code comments, which are functional but not the written analysis the assignment requires ("Write this information and turn it in").

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices embedded in the options DataFrame via `S0` column with timestamp — elegant approach that ties each option to its exact download-time underlying price
- Fed funds rate = 0.0364 from H.15 ✓
- TTM via **business days / 252**: `np.busday_count(today, expire) / 252.0` — more accurate than calendar-day approaches used by most students. Good financial practice.

---

## Part 2: Data Analysis (45/50)

### Q5 — Black-Scholes (7/7)
- `bs_formula(cp, S0, vol, T, K, r)` handles both 'C' and 'P' with correct d1/d2 formulas
- Uses `norm.cdf()` from scipy.stats ✓
- Clean single-function design with string argument for option type
- Error handling for unknown `cp` value

### Q6 — Bisection IV (5/7)
- `bisection()` is a **pure bisection method** — correct `fa * fm < 0` / `fb * fm < 0` logic. 10,000 max iterations.
- Tolerance via interval width `abs(b-a) < tol` = 1e-6 ✓
- `calc_iv_bisection_atm()` — finds ATM by minimum `|strike - S0|`, filters zero bid/ask ✓
- `calc_iv_bisection_range()` — computes average IV for 0.9-1.1 moneyness band ✓
- Applied to both SPY and TSLA ✓
- **Limitation**: Only **call options** used for IV computation. Puts are never directly IV-solved. Since BS implies put and call IV should match at the same strike/maturity, this is theoretically fine but the assignment says "for each option."

### Q7 — Newton + Timing (6/7)
- `newton()` implemented with analytical vega via `bs_vega()` ✓
- Initial guess 0.3, max 10,000 iterations, convergence check `abs(fx) < tol` ✓
- Guards: `dfx == 0` check, `x_next <= 0` check with optional print warnings
- `%%time` Jupyter magic used for timing comparison ✓
- Difference check confirms bisection and Newton agree to effectively zero
- **No Secant/Muller** method implemented
- Copy-paste artifact: comment says "use bisection to find the root" in Newton code — harmless but shows code was cloned from the bisection section

### Q8 — IV Table + Commentary (5/7)
- `iv_newton` DataFrame with IV_ATM and IV_Avg by Ticker and Expiry — clean table ✓
- VIX comparison: `vix_vol = float(vix['Close'].iloc[-1]) / 100.0` — converts VIX to decimal volatility for direct comparison ✓
- Commentary is thin — the submission is extremely code-heavy with minimal prose. The assignment says "You will be judged by the quality of the writing and the interpretation of the results."

### Q9 — Put-Call Parity (6/6)
- `calc_put_parity(C, S0, K, r, T)` = C - S0 + K·e^(-rT) ✓
- `calc_call_parity(P, S0, K, r, T)` = P + S0 - K·e^(-rT) ✓
- Applied to contracts in 0.90-1.10 moneyness band for both TSLA and SPY
- Full DataFrames showing market_call, market_put, bs_call, bs_put, par_call, par_put — comprehensive output
- Trimmed to near-ATM for display: TSLA (0.95-1.05), SPY (0.99-1.01)

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- **2D plot**: TSLA and SPY IV vs Strike for nearest maturity, side by side ✓
- **Multi-maturity overlay**: 3 maturities per ticker with different colors, separate TSLA/SPY panels ✓
- **3D bonus plot**: Both TSLA and SPY implied vol surfaces plotted as 3D scatter with `projection='3d'`, proper axis labels (Strike, Maturity, IV), `view_init(elev=25, azim=135)` for good viewing angle ✓
- Professional matplotlib plotting with grid, legends, titles

### Q11 — Greeks (5/5)
- Analytical: `bs_delta()`, `bs_gamma()`, `bs_vega()` — all correct formulas for calls ✓
- Finite difference `fd_greeks()`:
  - `step = 1e-3 * S0` (0.1% of spot) — reasonable step size
  - Delta: central `(P_u - P_d) / (2*step)` ✓
  - Gamma: central `(P_u - 2*P_0 + P_d) / step^2` ✓
  - Vega: central `(P_uv - P_dv) / (2*percent)` with `percent=1e-3` ✓
- Applied to TSLA (0.95-1.05) and SPY (0.99-1.01) ATM bands
- Full comparison tables with bs and fd columns

### Q12 — DATA2 Pricing (5/5)
- Uses `calc_ivs_newton(data1)` to compute all day-1 IVs indexed by `(expiry, K)`
- Iterates over DATA2, matches by `(exp, K)` key to look up day-1 IV
- Computes BS call and put prices using day-2 S0, day-1 IV, same rate
- **Excellent 12-panel visualization** (3 exps × 4 panels: TSLA call/put × SPY call/put) comparing market scatter vs BS scatter — one of the best Q12 presentations in the class
- Honest comment: "PS, i know i am calculating bs prices twice, once for calls then again for puts.... im too lazy to optimize sorry"

---

## Part 3: AMM Fee Revenue (26/30)

### Q3a — Derive Swap Amounts (9/10)
- **Handwritten derivations** on pages 36-37 for both Case 1 and Case 2
- **Code implementation** matches:
  - Case 1: `dx = x - (k / ((1-gamma)*s))^0.5`, `dy = ((k*(1-gamma)*s)^0.5 - y) / (1-gamma)`
  - Case 2: `dx = ((k*(1-gamma)/s)^0.5 - x) / (1-gamma)`, `dy = y - (k*s/(1-gamma))^0.5`
- `R_func(s, x, y, gamma)` correctly checks `s > P/(1-gamma)` for Case 1 and `s < P*(1-gamma)` for Case 2, returns `gamma*dy` or `gamma*dx*s` respectively, 0 otherwise ✓

### Q3b — Expected Fee Revenue (9/10)
- `log_density_func()` — correct lognormal density with `mu = -0.5*sigma^2*dt` ✓
- `trapz_func()` — clean trapezoidal rule: `0.5*(f(left) + f(right))*h` ✓
- `expected_revenue()` integrates `R * f_S` over [0.1, 2.0] with n=10,000 points
- **Concern**: Integration bounds [0.1, 2.0] may be too narrow for high-vol cases (σ=1.0 has significant mass beyond s=2.0). The upper bound should ideally be ~5.0 or higher.

### Q3c — Optimal Fee Rate (8/10)
- σ×γ table with pivot and `idxmax` ✓
- Grid search over σ ∈ [0.1, 1.0] with 0.01 step ✓
- `gamma_star` and `E[R]_max` DataFrame ✓
- **Plot** of σ vs γ*(σ) — clean line plot with grid ✓
- **Missing**: Written commentary on the observed pattern

---

## Part 4: Bonus (8/10)

### Analytical Solutions (3/3)
- f1 = xy: ∫₀¹∫₀³ xy dy dx = 9/4 ✓ (handwritten on page 37)
- f2 = e^(x+y): ∫₀¹∫₀³ e^(x+y) dy dx = e⁴ - e³ - e + 1 ✓

### Numerical Implementation (5/7)
- `comp_trapz_func(f, dx, dy)` correctly implements the hint formula with corner terms + edge midpoints + center midpoint, multiplied by `dx*dy/16` ✓
- **6 grid pairs** (exceeds the 4 required): (0.1,0.1), (1.0,1.0), (0.5,1.5), (0.5,0.5), (1.5,0.5), (0.5,5.0)
- **Bug**: The pair (0.5, 5.0) has `dy=5.0 > y_range=3.0`, so `m = int(3.0/5.0) = 0` — the inner loop never executes and the result is 0. Silent failure the student should have caught.
- f1 gives exact results for valid pairs (correct — the composite formula is exact for bilinear functions) ✓
- f2 shows convergence for valid pairs ✓
- **Missing**: Written commentary on convergence behavior and why f1 is exact

---

## Strengths
- **Strongest Q12 in the class** — the 12-panel market-vs-BS visualization (3 expirations × TSLA call/put × SPY call/put) is exceptional
- **TTM via business days/252** — more financially accurate than the calendar-day/365 approach most students used
- **3D implied vol surfaces** for both TSLA and SPY with good perspective angles
- **Part 3 fully implemented** — derivation, trapezoidal code, σ×γ table, optimal gamma plot. One of few students with complete Part 3
- **6 grid pairs for Part 4** — exceeds the 4 required
- Code is clean, well-organized with parallel function structures (bisection_atm/range, newton_atm/range, etc.)

## Weaknesses
- **Missing Q3 written descriptions entirely** — no paragraph on SPY (ETF), VIX (volatility index), option symbols, or expiration mechanics. This is a requirement
- **Only call options used for IV** — puts are never IV-solved directly
- **Commentary/analysis is extremely thin** — the submission is almost entirely code with minimal prose. Sections like Q8, Q3c, and Part 4 all lack written analysis
- **No Secant/Muller method** — only bisection and Newton implemented
- **Integration bounds [0.1, 2.0] for AMM** may underestimate E[R] at high volatility
- **One invalid grid pair** in Part 4: (0.5, 5.0) has dy > y-range, producing a degenerate 0 result
- **Report format**: Raw Jupyter notebook export, not a polished LaTeX/Word document as requested
- Copy-paste artifact: "use bisection to find the root" appears as a comment in the Newton code

## AI Assessment: LOW
Strong human indicators throughout: "im too lazy to optimize sorry" comment, copy-paste comment artifacts (bisection label in Newton code), only calls used for IV (a shortcut an AI would be unlikely to suggest), missing written analysis (an AI would typically generate analysis text), one invalid (dx,dy) pair not caught. Authentic student work.
