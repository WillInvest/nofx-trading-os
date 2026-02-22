# FE621 HW1 Grading Rubric

## Part 1 (20 pts) - Data Gathering
- **Q1** (5 pts): Data download function/program. Code present, source identified (Yahoo/Google/Bloomberg)
- **Q2** (5 pts): Downloaded TSLA, SPY, ^VIX (options+equity), 2 consecutive days, 3 monthly maturities (3rd Friday). Explanation of many maturities (weeklys, LEAPs, etc.)
- **Q3** (5 pts): Written description of SPY (ETF), ^VIX (volatility index), option symbols, expiration dates
- **Q4** (5 pts): Recorded underlying price at download time, short-term interest rate (Fed funds or T-bill, converted from %), time to maturity
- **Bonus** (5 pts): Multi-asset download to CSV/Excel

## Part 2 (50 pts) - Data Analysis
- **Q5** (~7 pts): Black-Scholes formula implemented from scratch (no toolbox; norm.cdf allowed)
- **Q6** (~7 pts): Bisection method for implied vol, tolerance 1e-6, ATM vol reported, both TSLA and SPY, average near-ATM vols
- **Q7** (~7 pts): Newton/Secant/Muller method, vega formula derived, timing comparison with bisection
- **Q8** (~7 pts): Table of implied vols (maturity x type x stock), average vols, commentary on TSLA vs SPY, vs VIX, maturity effect, moneyness
- **Q9** (~6 pts): Put-Call parity to price opposite type, compare with market bid/ask
- **Q10** (~6 pts): 2D vol smile (IV vs K) for nearest maturity, multi-maturity overlay (3 colors). Bonus: 3D surface
- **Q11** (~5 pts): Greeks (Delta, Vega, Gamma) analytical + numerical approximation, comparison table
- **Q12** (~5 pts): Use DATA2 + DATA1 implied vols + current rate to price via BS

## Part 3 (30 pts) - AMM Arbitrage Fee Revenue
- **Q3a** (10 pts): Derive swap amounts Δx, Δy for Case 1 and Case 2
- **Q3b** (10 pts): Expected fee revenue via trapezoidal rule (with given parameters)
- **Q3c** (10 pts): σ×γ table, optimal γ*(σ), scatter/line plot, commentary

## Part 4 - Bonus (10 pts)
- Analytical solutions for ∫∫ xy and ∫∫ e^(x+y)
- Numerical trapezoidal rule for double integral, 4 (Δx,Δy) pairs, error analysis

## General Quality Checks
- Code comments (required, graded)
- Report format (LaTeX/Word - professional)
- Tables well-formatted
- Figures/plots present and labeled
- Writing quality and interpretation of results

## Late Submissions
- choisungwuk, gahancian, stiemerjulius, zacheryjustin
