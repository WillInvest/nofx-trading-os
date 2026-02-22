# Gil, Joseph — FE621 HW1 Grading

**Final Score: 82/100 + 5 bonus = 82(+5)**

---

## Part 1: Data Gathering (20/20)

### Q1 — Download Function (5/5)
- `get_market_data(tickers, d1, d2)` uses yfinance for equity and option chain download
- Third-Friday filtering via `weekday()==4 and 15<=day<=21` — correct logic
- Downloads TSLA, SPY, ^VIX equity data and option chains
- Rate from FRED: `INT_Rate = 0.0364` — proper external source
- Code functional and well-organized

### Q2 — Download Data (5/5)
- Two consecutive trading days: DATA1 = 2026-02-12, DATA2 = 2026-02-13 ✓
- All three tickers: TSLA=417.07, SPY=681.27, VIX=20.82 ✓
- Third-Friday maturities filtered ✓
- Data structure properly organized

### Q3 — Written Descriptions (5/5)
- SPY, TSLA, VIX described with adequate detail
- **OCC option symbol format explicitly discussed**: "The expiration date is a set of 6 digits formatted as YYMMDD... The option type symbol is a 'C' for calls and a 'P' for puts... the strike price is represented by a set of 8 digits that tells the price in thousands"
- Good coverage of option expiration conventions

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded: TSLA=417.07, SPY=681.27, VIX=20.82 ✓
- Interest rate from FRED: 0.0364 ✓
- TTM correctly computed ✓

---

## Part 2: Data Analysis (41/50)

### Q5 — Black-Scholes (7/7)
- `bs_price(S0, K, T, r, sigma, opt_type='call')` correctly implements d1/d2
- Includes sigma/T guards for edge cases
- Uses `norm.cdf` from scipy ✓
- Clean implementation

### Q6 — Bisection IV (6/7)
- Bisection implemented with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV reported: TSLA Call 36.73% at K=417.5, SPY Call 16.66% at K=681.0
- Near-ATM averages computed in 0.95–1.05 moneyness band

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- Timing comparison: Bisection avg 0.00615s, Newton avg 0.00316s — **"Newton is 3.7x faster than Bisection"**
- **No Secant/Muller method** — only bisection and Newton
- Brief timing discussion present

### Q8 — IV Tables + Commentary (5/7)
- IV table: 12 rows by ticker/type/maturity with Newton IVs
- Commentary present: "TSLA has an increased implied volatility while SPY has a decreased implied volatility"
- VIX comparison: "The calculated VIX is pretty close to the SPY ATM IV"
- Commentary covers the key points but lacks deeper numerical analysis

### Q9 — Put-Call Parity (4/6)
- Put-call parity for SPY (Exp 2026-02-20) and TSLA with strike-by-strike table
- Comparison shown with market values
- Brief analysis present
- **Missing**: Discussion of American exercise premium effects

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D "Volatility Curve" with spot price dashed line, 3 expirations per ticker ✓
- Multi-maturity overlay ✓
- **3D trisurf plots** for both SPY and TSLA with viridis colormap — labeled "Extra Credit" section
- Professional matplotlib visualization — earns full bonus ✓

### Q11 — Greeks (4/5)
- `calc_greeks_approx(S0, K, T, r, sigma, dS=0.01, dVol=0.0001)` for FD approximations
- Analytical + FD comparison: SPY Delta 0.5242, Gamma 0.0237, Vega 40.163; TSLA Delta 0.5091, Gamma 0.0176, Vega 24.627
- Good agreement between methods
- **Minor**: Limited to a few representative options

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs: SPY K=681, Day2 spot 681.75, IV 16.66%, Calc price 6.90
- TSLA K=417.5, IV 36.73%, Calc price 8.58
- BS prices vs market comparison present
- Specific numerical examples provided

---

## Part 3: AMM Fee Revenue (21/30)

### Q3a — Derive Swap Amounts (7/10)
- Both Case 1 and Case 2 derivations present with algebraic work
- Swap amounts Δx and Δy derived from constant product constraint
- Mathematical approach correct
- Could be more clearly presented

### Q3b — Expected Fee Revenue (7/10)
- Trapezoidal rule implemented with numerical integration
- Expected fee = $0.00852204 for baseline σ=0.2, γ=0.003
- Lognormal density correctly handled
- Results computed for given parameters

### Q3c — Optimal Fee Rate (7/10)
- Coarse σ×γ table: σ ∈ {0.2, 0.6, 1.0}, γ ∈ {0.001, 0.003, 0.01} — all γ*=0.01 (class-wide pattern)
- **Extended search**: `linspace(0.1, 1.0, 50)` for σ, `linspace(0.0005, 0.015, 50)` for γ
- Optimal gamma plot produced ✓
- **Missing**: Detailed written commentary on the observed pattern

---

## Part 4: Bonus (0/10)

Not attempted.

---

## Strengths
- **OCC option symbol format** explicitly discussed — one of few students to include this
- **3D trisurf volatility surfaces** with viridis colormap — professional Extra Credit section earns bonus
- Strong Part 1 — all data gathering requirements met with specific values
- Timing comparison quantified: Newton 3.7x faster than bisection
- Extended gamma search in Q3c beyond the coarse 3-value grid
- Specific ATM IV values: TSLA 36.73%, SPY 16.66%

## Weaknesses
- **Code presented as images/screenshots** — harder to verify and not professional format
- **No Secant/Muller method** — only bisection and Newton
- **Sparse written commentary** throughout — Q8 analysis covers key points but lacks depth
- Put-call parity doesn't discuss American exercise premium
- Part 4 bonus not attempted
- Report format is not polished LaTeX/Word document

## AI Assessment: LOW
Code as screenshots, sparse comments, and minimal prose are all consistent with authentic student work. An AI would typically generate more polished prose and avoid screenshot-based code submission. The specific timing numbers (3.7x) and ATM IV values suggest hands-on computation. No signs of AI generation.
