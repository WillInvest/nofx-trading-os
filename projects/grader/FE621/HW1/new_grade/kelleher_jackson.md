# Kelleher, Jackson — FE621 HW1 Grading

**Final Score: 54/100 + 7 bonus = 54(+7)**

---

## Part 1: Data Gathering (13/20)

### Q1 — Download Function (4/5)
- `download_data()` function using `quantmod::getSymbols()` and `getOptionChain()` in R is functional
- Handles both equity and option data, writes to CSV
- VIX ticker symbol handling (`^VIX` → `VIX` for filenames) is a nice touch
- Minor: the function assigns to `.GlobalEnv` inside a function (bad practice) and does a redundant `getOptionChain` call (once for `chain`, once for `assign()`)
- The bonus multi-asset download is arguably built into this function already

### Q2 — Download Data (2/5)
- **Admitted downloading after the trading day on Feb 15**: "I apologize as I downloaded these after the trading day on the 15th, I did not see that part of the assignment until too late" — data was collected after market close on the due date itself, violating the "during the trading day" and "no later than February 14th" requirements
- Only **one day of data** visible (DATA1 only). **No DATA2** anywhere in the submission, which cascades into a missing Q12
- Third-Friday filtering for 3 monthly expirations is correctly implemented via `is_third_friday()`
- **Missing**: explanation of why many more maturities exist (weeklies, LEAPs, end-of-month, quarterly, etc.)

### Q3 — Written Descriptions (3/5)
- TSLA described as "common stock of Tesla" — adequate
- SPY as "SPDR S&P 500 ETF Trust" with ETF definition — good
- VIX described as "CBOE Volatility Index... measures the market's expectation of 30-day forward-looking volatility" — good
- Option contract identification listed (ticker, expiration, strike, type) — minimal
- **Missing**: OCC symbol format discussion, no specific option symbol examples from the data

### Q4 — Record Prices, Rate, TTM (4/5)
- Spot prices recorded: SPY=681.75, TSLA=417.44, VIX=20.60
- Fed funds effective rate r=0.0364 — sourced from H.15
- TTM calculated as `(exp_dates - today)/365` — standard calendar-day approach
- Minor: prices were recorded outside trading hours

---

## Part 2: Data Analysis (35/50)

### Q5 — Black-Scholes (6/7)
- `bs_call()` and `bs_put()` correctly implemented from scratch using `pnorm()`
- `bs_put()` has edge case handling for T≤0 or σ≤0 (returns intrinsic)
- Minor inconsistency: `bs_call()` computes d1/d2 inline while `bs_put()` calls `bs_d1()` helper — suggests the two functions were written at different times or `bs_call()` was written first and not refactored

### Q6 — Bisection IV (5/7)
- Implemented as **Regula Falsi** (false position), not pure bisection: `vi = vLow + (price - cLow)*(vHigh - vLow)/(cHigh - cLow)`. The assignment says "Bisection method" — this is a related but distinct algorithm. Still a valid root-finding method, but technically not what was asked
- Tolerance 1e-6 ✓, dynamic upper bound expansion ✓
- Applied to both SPY and TSLA ✓
- ATM IV reported, average in 0.95-1.05 band calculated ✓
- **Problem**: SPY short-dated (tau=0.014 years) IVs are absurdly high: Strike=335 → IV=1.92, Strike=365 → IV=4.04. These are deep ITM options with very short time to expiry — the student doesn't filter or address these
- Citation from StackExchange provided (honest attribution)

### Q7 — Newton/Secant + Timing (5/7)
- **Newton** `iv_newton()` is well-implemented: uses analytical vega, sigma clamping `min(max(sigma_new, 1e-6), 5)`, guards against near-zero vega. This is one of the better Newton implementations in the class
- **Secant** `iv_secant()` implemented — one of very few students to do this. However, **it returns NA for the vast majority of options** (all 20 rows in the first printout). Only works for near-ATM options (confirmed in the ATM report table where Secant matches bisection and Newton perfectly). The failure pattern suggests the initial guesses (0.10, 0.30) cause divergence for extreme strikes
- **Timing comparison present**: SPY: Bisect 0.39s, Newton 0.01s, Secant 0.06s → Newton is ~39x faster. TSLA: similar ratios
- No written discussion of *why* Newton is faster (quadratic vs linear convergence)

### Q8 — IV Tables + Commentary (4/7)
- Tables present showing IVs by maturity/type/stock
- Average IVs in ATM band reported for all methods
- Commentary covers required points but is **extremely thin** — just 4 sentences:
  - TSLA > SPY ✓
  - SPY ≈ VIX ✓
  - IV increases with maturity ✓
  - IV increases for ITM/OTM ✓
- No numerical references in the commentary, no specific comparison of values
- "Done above in previous R chunks, see tables above" — lazy signposting

### Q9 — Put-Call Parity (5/6)
- Correct implementation: `Put_Implied = Mid_Call - S0 + Strike * exp(-r * Tau)`
- Comparison table shows differences ~-1.5 for SPY near ATM
- Good observation: "Since we are using American options not European, BS formulas do not hold up. Also, TSLA has dividends." — valid and shows understanding
- Only shows 10 rows near ATM for one maturity; could be more comprehensive

### Q10 — Vol Smile Plots (5/6)
- 2D volatility smile by type/expiration using `ggplot2` with `facet_wrap` — professional looking
- Multi-maturity overlay with different colors present
- Warnings about removed rows (NA values) — not cleaned up
- **No 3D surface plot** (bonus not attempted)
- No written description of what is observed in the smile shapes

### Q11 — Greeks (5/5)
- **Best section of the submission.** Analytical Delta, Gamma, Vega all correct for calls
- Finite difference: central differences for Delta and Gamma (using `hS = 0.01*S0`), central for Vega (`hV=1e-4`)
- Comprehensive comparison table with differences — all differences are tiny (Delta_Diff ~1e-4, Gamma_Diff ~1e-5, Vega_Diff ~1e-7), confirming convergence
- Applied across all maturities and near-ATM options — 30 rows shown
- Well-organized output with `mapply()` — clean R coding

### Q12 — DATA2 Pricing (0/5)
- **Entirely missing.** No DATA2 was downloaded, so this question could not be attempted. Direct consequence of the late/single-day data download issue.

---

## Part 3: AMM Fee Revenue (6/30)

### Q3a — Derive Swap Amounts (6/10)
- Handwritten derivation on pages 9-10
- Shows understanding of the setup: variables defined (BTC reserves, USDC reserves, trade mechanics, constant product constraint)
- Both Case 1 and Case 2 boundary conditions referenced
- Derivation attempts to solve for Δx and Δy
- **Hard to follow** — OCR of handwriting is garbled, but the mathematical structure appears on the right track
- **Incomplete**: the final clean expressions for Δx(S_{t+1}) and Δy(S_{t+1}) are not clearly boxed/stated

### Q3b — Expected Fee Revenue (0/10)
- **No code implementation.** The expected fee revenue integral is referenced in the handwritten work, but there is **no R code computing the trapezoidal approximation** of E[R(S_{t+1})]. No numerical results at all.

### Q3c — Optimal Fee Rate (0/10)
- **Entirely missing.** No sigma×gamma table, no optimal γ*(σ) computation, no scatter/line plot, no commentary.

---

## Part 4: Bonus (7/10)

### Analytical Solutions (3/3)
- f1: ∫₀¹∫₀³ xy dy dx = 9/4 ✓
- f2: ∫₀¹∫₀³ e^(x+y) dy dx = e⁴ - e³ - e¹ + 1 ≈ 32.794 ✓

### Numerical Implementation (4/7)
- 4 grid pairs: (0.1, 0.2), (0.04, 0.04), (0.01, 0.005), (0.001, 0.0001)
- f1 gives machine-epsilon error for all grids — correct, since the composite formula is exact for bilinear f(x,y)=xy
- f2 converges cleanly: 3.4e-2 → 2.2e-3 → 8.5e-5 → 6.9e-7
- Code correctly implements the hint formula with corner terms + edge midpoints + center midpoint
- Error plot included (log scale vs step size)
- **Missing**: commentary on why f1 is exact, convergence rate analysis for f2

---

## Strengths
- One of few students to implement all 3 root-finding methods (bisection, Newton, Secant)
- Newton implementation is excellent with proper sigma clamping and vega guards
- Greeks section is the strongest part — comprehensive analytical + FD comparison with tiny errors confirming convergence
- Bonus double integral is correct with clean convergence demonstration
- Honest about mistakes (late data download admission)
- R code is generally clean with `ggplot2` for professional plots

## Weaknesses
- **Q12 entirely missing** due to no DATA2 — 5-point loss cascading from data gathering failure
- **Part 3 almost entirely missing** — only partial handwritten derivation for Q3a, no code for Q3b, nothing for Q3c. 20-24 points lost
- Secant method returns NA for most options — should have debugged or acknowledged
- Q6 uses Regula Falsi (false position) not strict bisection
- SPY short-dated IVs (>1.0, up to 4.0) are clearly artifacts but never addressed or filtered
- Commentary throughout is extremely thin — mostly 1-2 sentences per topic
- No explanation of why many option maturities exist (weeklies, LEAPs)
- Report format is raw R Markdown/console output — not a polished Word/LaTeX report

## AI Assessment: LOW
The R code has genuine character — honest StackExchange citation, admitted mistakes, broken Secant method left in, raw console output presentation, and incomplete sections are all strongly indicative of authentic student work. No signs of AI generation.
