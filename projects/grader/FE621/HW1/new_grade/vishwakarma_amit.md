# Vishwakarma, Amit Vijay — FE621 HW1 Grading

**Final Score: 85/100 + 10 bonus = 85(+10)**

---

## Part 1: Data Gathering (19/20)

### Q1 — Download Function (5/5)
- Well-structured download function
- Multi-asset support built in
- Clean organization

### Q2 — Download Data (5/5)
- Two consecutive trading days ✓
- TSLA, SPY, ^VIX ✓
- Third-Friday maturities ✓

### Q3 — Written Descriptions (4/5)
- Good descriptions of SPY (ETF), VIX, TSLA
- Written analysis present
- **Minor**: OCC format could be more detailed

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

### Bonus (5/5)
- **Multi-asset CSV** download implemented — earns P1 bonus ✓

---

## Part 2: Data Analysis (41/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented
- Handles calls and puts
- Clean code

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV and averages reported

### Q7 — Newton/Secant + Timing (5/7)
- Newton with analytical vega ✓
- **Newton returns NaN for deep ITM options** — not diagnosed
- Timing comparison present
- **No Secant/Muller method**

### Q8 — IV Tables + Commentary (5/7)
- IV tables present
- Average vols computed
- **Good commentary** — discusses TSLA vs SPY, VIX comparison, maturity effects
- Above-average analysis quality

### Q9 — Put-Call Parity (4/6)
- Implementation present
- **One-sided check methodology** — only checks one direction of parity
- Comparison with market values
- Could be more comprehensive

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D plots ✓
- Multi-maturity overlay ✓
- **3D trisurf plots** — well-implemented, professional appearance
- Earns Q10 bonus ✓

### Q11 — Greeks (4/5)
- Analytical + FD Greeks computed
- Comparison present
- **Minor**: Newton NaN issues may affect some Greek calculations

### Q12 — DATA2 Pricing (4/5)
- DATA2 pricing with DATA1 IVs ✓
- BS prices vs market comparison
- Analysis present

---

## Part 3: AMM Fee Revenue (25/30)

### Q3a — Derive Swap Amounts (8/10)
- Both cases addressed
- Derivation present
- Correct approach

### Q3b — Expected Fee Revenue (8/10)
- Trapezoidal rule implemented
- Numerical results computed

### Q3c — Optimal Fee Rate (9/10)
- **Extended gamma search** over [0.0005, 0.5] — much wider than the basic 3-value grid
- σ×γ analysis comprehensive
- Good plot ✓
- Commentary present

---

## Part 4: Bonus (10/10)

### P1 Bonus (5/5)
- Multi-asset CSV download ✓

### Q10 3D Bonus (5/5)
- 3D trisurf plots for both TSLA and SPY ✓

---

## Strengths
- **Highest bonus in the class** — earns both P1 multi-asset bonus AND Q10 3D bonus (10 total)
- **3D trisurf plots** are among the best visualizations in the class
- **Extended gamma search** [0.0005, 0.5] — most comprehensive gamma range explored
- Good Q8 commentary
- Well-structured download with multi-asset support
- Complete coverage of all parts

## Weaknesses
- **Newton NaN for deep ITM** — unresolved, affects downstream analysis
- **No Secant/Muller method**
- **Put-call parity one-sided** — should check both directions
- Newton failures not diagnosed or discussed
- Some commentary could be more detailed with specific numbers

## AI Assessment: LOW
The Newton NaN issue (left unresolved) and one-sided parity check are typical student oversights. The extended gamma search and 3D trisurf plots show genuine computational initiative. No signs of AI generation.
