# Fan, Kaiwen — FE621 HW1 Grading

**Final Score: 58/100 + 6 bonus = 58(+6)**

---

## Part 1: Data Gathering (12/20)

### Q1 — Download Function (3/5)
- **PDF submission**: Only prose description of download process — no actual code shown in the submitted PDF
- **Companion Colab notebook** (found separately): yfinance download for TSLA, SPY, ^VIX is functional with `files.upload()`/`files.download()` Colab workflow
- Third-Friday filtering present in notebook but not demonstrated in PDF deliverable
- Code exists but was not part of the formal submission

### Q2 — Download Data (3/5)
- PDF mentions data was downloaded on 2/11/26 (DATA1) — within deadline
- 5 expirations downloaded (more than required 3)
- **PDF deliverable**: No data tables, no screenshots of downloaded data, no evidence of DATA2
- Companion notebook shows execution artifacts confirming real data download

### Q3 — Written Descriptions (3/5)
- PDF contains prose descriptions of TSLA, SPY, and VIX
- SPY described as ETF tracking S&P 500
- VIX described as volatility index
- Descriptions are adequate in the PDF portion
- **Missing**: OCC option symbol format

### Q4 — Record Prices, Rate, TTM (3/5)
- PDF references prices and rate but **no specific numerical values shown**
- Companion notebook has rate and spot prices embedded in code
- TTM computation present in notebook code
- **Penalty**: PDF deliverable doesn't show the actual recorded values

---

## Part 2: Data Analysis (28/50)

### Q5 — Black-Scholes (5/7)
- **PDF**: Prose description only — "BS pricing formula was coded using the standard expressions for d1 and d2"
- **Notebook**: `black_scholes_price()` correctly implemented with `norm.cdf`
- Handles calls and puts
- **Penalty**: Code not shown in submitted PDF; grading based on companion notebook with penalty

### Q6 — Bisection IV (4/7)
- **PDF**: No code, no tables, no results
- **Notebook**: Bisection implemented, applied to options
- ATM IV computed
- **CRITICAL BUG**: IV averaging produces **-14,720,758** — the `analyze_row` function stores raw Newton output including diverged negative values, completely poisoning all downstream averages. Student clearly never reviewed their own output
- Penalty for missing from PDF + critical bug

### Q7 — Newton/Secant + Timing (3/7)
- **PDF**: No code or timing results shown
- **Notebook**: Newton method implemented
- **No Secant/Muller method**
- Timing comparison not clearly presented
- No written discussion of convergence differences

### Q8 — IV Tables + Commentary (2/7)
- **PDF**: No IV tables
- **Notebook**: Summary tables generated but with corrupted averages (from the -14.7M bug)
- **No written commentary** on TSLA vs SPY, VIX comparison, maturity effects
- This is the weakest section — assignment says "you will be judged by the quality of the writing"

### Q9 — Put-Call Parity (3/6)
- **PDF**: Mentioned briefly
- **Notebook**: Put-call parity computation present
- Comparison with market values attempted
- Results exist in notebook but not shown in PDF

### Q10 — Vol Smile Plots (4/6)
- **PDF**: No plots shown
- **Notebook**: 2D vol smile plots generated
- **3D surface plot** present in notebook — would earn bonus if it were in the PDF
- Multi-maturity overlay present in notebook
- Graded with partial credit for notebook content, penalty for PDF absence

### Q11 — Greeks (4/5)
- **Notebook**: Analytical + FD Greeks implemented
- Delta, Gamma, Vega computed
- Comparison present
- **Note**: `gamma_num` in notebook uses wrong center value in FD — minor bug

### Q12 — DATA2 Pricing (3/5)
- **Notebook**: DATA2 pricing attempted with DATA1 IVs
- **Problem**: With corrupted IVs from Q6, downstream pricing is unreliable
- Basic structure is correct even if results are contaminated

---

## Part 3: AMM Fee Revenue (12/30)

### Q3a — Derive Swap Amounts (5/10)
- **PDF**: Prose description of approach
- **Notebook**: Function for AMM fee revenue present
- Derivation not shown in detail in either document
- Code structure suggests understanding of Case 1 and Case 2

### Q3b — Expected Fee Revenue (4/10)
- **Notebook**: `expected_revenue` function present — notably the most polished function in the codebase (only one with a docstring)
- Trapezoidal integration attempted
- Numerical results computed
- **Missing from PDF**: No code, no results shown

### Q3c — Optimal Fee Rate (3/10)
- **Notebook**: σ×γ table and optimal gamma plot generated
- Grid search present
- **Missing from PDF**: No table, no plot, no commentary
- No written analysis of the pattern

---

## Part 4: Bonus (6/10)

### Analytical Solutions (3/3)
- **Notebook**: Both integrals computed correctly
- f1 = xy: ∫₀¹∫₀³ xy dy dx = 9/4 ✓
- f2 = e^(x+y): correct ✓

### Numerical Implementation (3/7)
- **Notebook**: 4 grid pairs tested
- f1 gives machine-epsilon error ✓
- f2 converges cleanly ✓
- **Missing**: Written commentary on convergence behavior, why f1 is exact
- **Missing from PDF**: No code or results shown

---

## Strengths
- Companion Colab notebook demonstrates that the student **did complete the computational work** for all parts including bonus
- Analytical solutions for bonus integrals are correct
- Code structure in notebook is generally reasonable
- Data download with real dates (2/11/26) and Colab execution artifacts confirm genuine work
- 3D volatility surface plot present in notebook

## Weaknesses
- **PDF deliverable is fatally incomplete** — contains only prose descriptions with NO code, NO plots, NO tables, NO numerical results. The assignment explicitly requires "a PDF containing the report" with "nicely formatted tables and figures"
- **Critical IV averaging bug** (-14,720,758) — student clearly never reviewed their own output. This contaminates all downstream analysis (Q8 averages, Q12 pricing)
- **No Secant/Muller method**
- **No written commentary/analysis** for Q8 (the assignment emphasizes "quality of writing and interpretation")
- Key collision risk in `iv_map` (strike, type without symbol/expiry) could cause incorrect IV lookups
- Notebook has duplicated function definitions across cells — messy development workflow
- Score reflects a middle ground: substantial work was done (Colab confirms this) but the submitted deliverable was far below the assignment requirements

## AI Assessment: LOW-MODERATE
Mostly human-authored. Indicators: typo `"# PArt 1 data downloading"`, personal workflow notes (`"I downloaded Day 1 on 2/11/26"`), sloppy short variable names, real unfixed bugs (-14.7M average never noticed), duplicated function definitions across cells, Colab upload/download workflow. One possible AI-assisted section: the `expected_revenue` AMM function is the only function with a docstring and the most polished code — the unfamiliar DeFi topic is exactly where a student would consult an LLM. Not wholesale AI-generated.
