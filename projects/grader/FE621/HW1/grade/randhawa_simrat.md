# Randhawa, Simrat Kaur — FE621 HW1 Grading

**Final Score: 83/100 + 8 bonus = 83(+8)**

---

## Part 1: Data Gathering (15/20)

### Q1 — Download Function (5/5)
- **Bloomberg via Rblpapi** — unique in class, shows access to institutional data
- R for data download, Python for analysis — dual-language approach
- Handles equity and option chain downloads
- Well-organized across 4 separate PDF submissions

### Q2 — Download Data (3/5)
- Two consecutive days of data ✓
- TSLA, SPY downloaded ✓
- **Issue**: VIX options absent — only VIX spot level
- **Missing**: Explanation of many maturities

### Q3 — Written Descriptions (2/5)
- **Brief 1-page report** — minimal prose
- Basic descriptions only
- **Missing**: Detailed SPY/ETF definition, VIX explanation, OCC format
- Report is far too brief for Q3 requirements

### Q4 — Record Prices, Rate, TTM (5/5)
- Spot prices recorded ✓
- Interest rate sourced ✓
- TTM computed ✓

---

## Part 2: Data Analysis (44/50)

### Q5 — Black-Scholes (7/7)
- BS correctly implemented
- Handles calls and puts
- Clean Python implementation

### Q6 — Bisection IV (6/7)
- Bisection with tolerance 1e-6 ✓
- Applied to both TSLA and SPY ✓
- ATM IV and averages reported

### Q7 — Newton/Secant + Timing (4/7)
- Newton with analytical vega ✓
- **No Secant/Muller method**
- **No timing comparison** — assignment requires comparing time to find root
- Missing discussion of convergence speed

### Q8 — IV Tables + Commentary (5/7)
- IV tables present
- Average vols computed
- Commentary covers basic required points
- **Thin writing** — minimal prose

### Q9 — Put-Call Parity (5/6)
- Correctly implemented
- Comparison with market values
- Brief analysis

### Q10 — Vol Smile Plots (6/6 + 5 bonus)
- 2D plots present ✓
- Multi-maturity overlay ✓
- **3D plots present** — 8+ plots including 3D surface
- Professional visualization with multiple plot types

### Q11 — Greeks (5/5)
- Analytical + FD Greeks computed
- Comparison showing agreement
- Well-implemented

### Q12 — DATA2 Pricing (5/5)
- DATA2 pricing with DATA1 IVs ✓
- Comprehensive comparison
- Well-presented

---

## Part 3: AMM Fee Revenue (24/30)

### Q3a — Derive Swap Amounts (8/10)
- Both cases addressed
- Derivation present
- Mathematical approach correct

### Q3b — Expected Fee Revenue (8/10)
- Trapezoidal rule implemented ✓
- Numerical results computed
- Adequate resolution

### Q3c — Optimal Fee Rate (8/10)
- σ×γ table computed ✓
- γ* flat at 0.01 — standard class pattern from coarse grid
- Plot produced ✓
- **Thin commentary**

---

## Part 4: Bonus (8/10)

### Analytical Solutions (3/3)
- f1 = xy: 9/4 ✓
- f2 = e^(x+y): correct ✓

### Numerical Implementation (5/7)
- 4 grid sizes tested ✓
- f1 gives exact results ✓
- f2 shows convergence ✓
- **Missing**: Written commentary on convergence behavior

---

## Strengths
- **Bloomberg via Rblpapi** — unique data source in the class, demonstrates institutional access
- **8+ plots including 3D** — strong visualization
- **Dual-language approach** (R + Python) shows versatility
- Part 4 bonus complete
- Good overall coverage of all parts

## Weaknesses
- **Brief 1-page report** — far too short for Q3 requirements
- **No Secant/Muller method**
- **No timing comparison** — required by Q7
- VIX options not downloaded
- Written analysis is extremely thin throughout
- 4 separate PDFs is somewhat disorganized
- γ* flat at 0.01 with no investigation

## AI Assessment: LOW
Bloomberg/Rblpapi usage is a strong indicator of authentic student work — this requires physical lab access. The dual R+Python approach and brief report style are consistent with a student more comfortable with code than writing. No signs of AI generation.
