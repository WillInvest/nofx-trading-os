# Garg, Achintya — FE621 HW1 Grading

**Final Score: 85/100 + 5 bonus = 85(+5)**

---

## Part 1: Data Gathering (17/20)

### Q1 — Download Function (4/5)
- `fetch_option_snapshot(expiry_list, valuation_date)` uses yfinance for option chain download
- `^IRX` (13-week Treasury bill) used for risk-free rate — appropriate source
- Symbols: `['TSLA','SPY']` with ^VIX for spot only
- Downloads equity and option data with volume/bid/ask filtering
- Code functional but minimal inline comments

### Q2 — Download Data (4/5)
- Two consecutive trading days: DATA1 = 2026-02-12, DATA2 = 2026-02-13 ✓
- TSLA, SPY, ^VIX all present ✓
- Third-Friday filtering for 3 monthly maturities ✓
- **Missing**: No explicit explanation of why many more maturities exist (weeklies, LEAPs, etc.)

### Q3 — Written Descriptions (4/5)
- **"Symbols Downloaded" section** with structured bullet descriptions:
  - TSLA: individual equity
  - SPY: ETF tracking S&P 500 index
  - VIX: CBOE 30-day implied volatility index
- **"Option Structure" section** listing underlying, expiration, strike, contract type
- Adequate coverage — slightly below full marks for lack of OCC symbol format detail

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded at download time ✓
- Interest rate from `^IRX` ✓
- TTM correctly computed ✓

---

## Part 2: Data Analysis (43/50)

### Q5 — Black-Scholes (7/7)
- BS call and put formulas correctly implemented from scratch
- Uses `norm.cdf` from scipy ✓
- Clean implementation with proper d1/d2 calculations
- numpy throughout

### Q6 — Bisection IV (6/7)
- `bisection(func, a, b, tol=1e-6, max_iter=100)` with dual convergence: `abs(f_mid) < tol or (b-a)/2 < tol`
- Bracket `[0.0001, 5.0]`
- ATM IV: TSLA 8d: 0.3674, 36d: 0.4310, 64d: 0.4453; SPY 8d: 0.1667, 36d: 0.1696, 64d: 0.1631
- Near-ATM averages in 0.95–1.05 moneyness band
- **Minor**: No discussion of IV artifacts for extreme strikes

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical `vega()` = S·√T·φ(d1), guard `v < 1e-7`
- **Timing: Bisection 15.95s vs Newton 3.02s** — Newton 5.3x faster
- **No Secant/Muller method** — only bisection and Newton
- Timing numbers reported but minimal written analysis of convergence theory

### Q8 — IV Tables + Commentary (5/7)
- IV table: 12 rows by Symbol/Type/Days showing Newton IVs
- Average vols computed by maturity and type
- Commentary covers basic required points (TSLA vs SPY, maturity effect)
- **Weakness**: Commentary is thin — mostly bullet points without deep numerical analysis

### Q9 — Put-Call Parity (5/6)
- `put_call_parity_analysis(df)` computes `Theory_Put` and `Theory_Call`
- `.between(bid, ask)` validity check — clean approach
- Fractions within bid-ask: SPY Call 0.41, TSLA Call 0.33
- **Minor**: Could discuss American exercise premium explicitly

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D smile: per ticker with 3 maturity colors + spot price dashed vertical line ✓
- Multi-maturity overlay ✓
- **3D scatter plots** (axes: TTM, Strike, IV) for TSLA and SPY
- **Bonus 3D trisurf**: labeled "TSLA Implied Volatility Surface" and "SPY Implied Volatility Surface" — earns full bonus ✓

### Q11 — Greeks (5/5)
- `bs_greeks_call()` analytical: Delta, Gamma, Vega all correct
- `numerical_greeks(h=1e-4)` central finite differences
- Comparison: Delta 0.94399/0.94399, Gamma 0.003118/0.003121, Vega 6.968/6.968
- Full 616-row comparison table, avg absolute diffs: Delta 1.8e-10, Gamma 5.5e-6, Vega 2.5e-6 — excellent agreement

### Q12 — DATA2 Pricing (4/5)
- Merge DATA1 IVs with DATA2 by (strike, expiration, type)
- `reprice_option` with DATA2 spot and DATA1 IV
- BS prices vs market comparison present
- Basic analysis of pricing errors

---

## Part 3: AMM Fee Revenue (25/30)

### Q3a — Derive Swap Amounts (8/10)
- Both Case 1 and Case 2 derivations present
- Swap amounts properly derived from constant product constraint
- Mathematical structure correct
- **Minor**: Could be more clearly presented

### Q3b — Expected Fee Revenue (8/10)
- `expected_fee_revenue(gamma, sigma, n_points=10000)` with trapezoidal rule
- Lognormal density correctly handled
- Numerical results computed for baseline parameters
- 10,000 grid points — good resolution

### Q3c — Optimal Fee Rate (9/10)
- Coarse σ×γ table: σ ∈ {0.2, 0.6, 1.0}, γ ∈ {0.001, 0.003, 0.01}
- **Extended search**: `linspace(0.0005, 0.015, 50)` for γ — goes well beyond the 3 specified values
- Optimal γ*(σ) found for each volatility level
- Plot produced ✓
- **Minor**: Written commentary on the observed pattern is thin

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **3D trisurf volatility surfaces** for both tickers — earns full Q10 bonus
- **Greeks section is excellent** — 616-row comparison with avg diffs at machine-epsilon level (Delta 1.8e-10)
- **Extended gamma search** in Q3c with 50-point linspace — shows initiative
- Newton 5.3x speedup clearly demonstrated with specific timing
- Dual convergence criterion in bisection (`abs(f_mid) < tol or (b-a)/2 < tol`) — robust design
- Structured "Symbols Downloaded" and "Option Structure" sections in Part 1
- Put-call parity `.between(bid, ask)` validation is a clean approach
- Complete coverage of Parts 1-3

## Weaknesses
- **Written analysis is thin throughout** — submission is code-heavy with minimal prose
- **No Secant/Muller method** — only bisection and Newton
- No full OCC symbol format discussion
- No explanation of why many maturities exist
- Commentary in Q8 lacks deep numerical comparisons
- Part 4 bonus not attempted
- Report format is code-centric Jupyter notebook — not a polished document

## AI Assessment: LOW
Code-heavy submission with minimal prose is consistent with a student who is comfortable coding but less inclined to write analysis. The thin commentary throughout (which an AI would typically generate) and the missing Secant method suggest authentic student work. The excellent Greeks comparison (616 rows) shows genuine computational effort. No signs of AI generation.
