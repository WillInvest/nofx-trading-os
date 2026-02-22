# FE621 HW1 - Pre-Grading Dashboard

## Quick Reference: Score Ranges (sorted high to low)


| #   | Student               | Late | Lang | P1/20    | P2/50    | P3/30    | Bonus/10 | Est. Range           | Tier  |
| --- | --------------------- | ---- | ---- | -------- | -------- | -------- | -------- | -------------------- | ----- |
| 1   | Friedman, Samuel      | -    | Py   | 19-20    | 46-49    | 27-29    | 9-10     | **92-97+9**          | A+    |
| 2   | Tenreiro, James       | -    | R    | 17-19    | 42-46    | 28-30    | 7-8      | **88-93+8**          | A     |
| 3   | Ponce, Jorge          | -    | Py   | 18-20    | 42-46    | 27-30    | 8-10     | **87-94+9**          | A     |
| 4   | Marton, Bence         | -    | Py   | 18-20    | 42-46    | 27-30    | 0        | **87-93**            | A     |
| 5   | Novoa Molina, Daniela | -    | Py   | 14-16    | 44-48    | 27-30    | 0        | **85-94**            | A     |
| 6   | Hsieh, Tzuling        | -    | Py   | 17-19    | 40-44    | 27-30    | 8-10     | **82-90+9**          | A-    |
| 7   | Khaw, Steven          | -    | Py   | 15-17    | 42-46    | 26-28    | 8-10     | **83-91+9**          | A-    |
| 8   | Santos, Afonso        | -    | R    | 17-18    | 44-47    | 21-23    | 0        | **82-88**            | A-    |
| 9   | Vishwakarma, Amit     | -    | Py   | 18-20    | 40-44    | 24-27    | 7-10     | **82-91+8**          | A-    |
| 10  | Randhawa, Simrat      | -    | R+Py | 14-16    | 42-46    | 24-27    | 7-9      | **80-89+8**          | B+    |
| 11  | Chopra, Rohan         | -    | Py   | 14-16    | 42-46    | 24-27    | 0        | **80-87**            | B+    |
| 12  | Takeshita, Bryan      | -    | Py   | 17-19    | 38-42    | 26-28    | 0        | **81-89**            | B+    |
| 13  | Zachery, Justin       | LATE | R    | 16-17    | 41-44    | 24-26    | 0        | **80-87+late**       | B+    |
| 14  | Yao, Yuhang           | -    | Py   | 16-18    | 40-44    | 26-28    | 0        | **79-85**            | B+    |
| 15  | Garg, Achintya        | -    | Py   | 15-17    | 40-44    | 23-26    | 0        | **78-87**            | B+    |
| 16  | Khosla, Tasha         | -    | Py   | 16-18    | 35-40    | 27-30    | 0        | **78-88**            | B+    |
| 17  | Trivedi, Akarsh       | -    | Py   | 14-16    | 37-42    | 26-28    | 8-10     | **77-86+9**          | B     |
| 18  | Sealy, Andre          | -    | Py   | 18-20    | 34-40    | 26-30    | 0        | **72-82**            | B     |
| 19  | Gil, Joseph           | -    | Py   | 18-20    | 36-42    | 18-22    | 0        | **72-80**            | B     |
| 20  | Stiemer, Julius       | LATE | Py   | 16-18    | 38-42    | 10-14    | 2-3      | **64-74+late**       | B-/C+ |
| 21  | Choi, Sungwuk         | LATE | Py   | 15-17    | 35-40    | 18-22    | 0        | **62-72+late**       | C+    |
| 22  | Tartaglia, Austin     | -    | Py   | 12-14    | 32-36    | 15-18    | 2-3      | **62-70+3**          | C+    |
| 23  | Kelleher, Jackson     | -    | R    | 13-15    | 28-32    | 6-8      | 5-7      | **52-60+6**          | C     |
| 24  | Gahan, Cian           | LATE | Py   | 14-16    | 33-37    | 4-6      | 2-4      | **51-59+late**       | C/D   |
| 25  | Smadi, Fallyn         | -    | Py   | 16       | 32-36    | 0        | 0        | **45-53**            | D     |
| 26  | Fan, Kaiwen           | -    | Py   | ~partial | ~partial | ~partial | ~partial | ~~**25-35~~ 55-65*** | D/C   |


---

## Late Submissions (4 students)

1. **Choi, Sungwuk** - 62-72 pre-penalty
2. **Gahan, Cian** - 51-59 pre-penalty
3. **Stiemer, Julius** - 64-74 pre-penalty
4. **Zachery, Justin** - 80-87 pre-penalty

---

## Common Patterns & Class-Wide Observations

### Nearly Universal Issues

- **No Secant method**: ~23/26 students only implemented Newton (not Secant/Muller). Only Santos (R) implemented all three (bisection + Newton + Secant). Chopra's report header references it but unclear if fully separate.
- *Optimal gamma always at boundary: Nearly all students find gamma*=0.01 for all sigma values because the discrete grid {0.001, 0.003, 0.01} is too coarse. This is a design issue in the problem, not necessarily a student error.
- **VIX options not analyzed**: Most students only download VIX spot level, not VIX option chains. The assignment wording is somewhat ambiguous on this.

### Common Deductions

- Missing 3D volatility surface plot (~40% of class)
- Thin commentary / minimal written analysis (~30% of class)
- No explicit option symbol (OCC format) discussion (~50% of class)
- Code as screenshots rather than formatted code (~20% of class)

### Standout Submissions

- **Friedman**: Most complete, all parts + bonus, well-documented code
- **Tenreiro**: Clean R submission, professional LaTeX, bonus complete
- **Ponce**: Strong report + separate code, bonus complete
- **Santos**: Only student with all 3 root-finding methods (bisection + Newton + Secant)
- **Randhawa**: Only student using Bloomberg (R + Rblpapi)

### Major Red Flags

- **Fan**: PDF was prose-only executive summary, BUT companion Colab notebook found with working code for all parts (revised to 55-65; see detailed notes)
- **Smadi**: Entire Part 3 missing (0/30), h=100 in numerical Greeks
- **Gahan**: Used SPX instead of SPY, Q11 unexecuted, Part 3 almost entirely incomplete
- **Kelleher**: Q12 missing, Part 3 mostly missing, admitted late data download
- **Trivedi**: DATA1 and DATA2 from same day (20 min apart), not two consecutive trading days

### AI Usage Assessment (from Complement Code Review)

6 students had complement coding files reviewed. AI detection summary:


| Student        | AI Likelihood    | Key Evidence                                                                                                                                                                                                                     |
| -------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Choi, Sungwuk  | **LOW**          | Typo "Newton Methodi"; no docstrings; hardcoded API key; Korean placeholder text; casual style                                                                                                                                   |
| Gahan, Cian    | **LOW**          | Personal/conversational writing; inconsistent style; genuine TODO markers; real bugs persist; sections trail off mid-work                                                                                                        |
| Fan, Kaiwen    | **LOW-MODERATE** | Mostly human (typos, workflow notes, unfixed bugs), but AMM function is suspiciously polished vs. rest of code                                                                                                                   |
| Khosla, Tasha  | **LOW-MODERATE** | Notably polished style (type hints, pathlib, closures), but real bugs (missing `abs()`, wrong `Callable` annotation). Possibly Copilot-assisted                                                                                  |
| Hsieh, Tzuling | **LOW**          | Bilingual Chinese/English working notes in comments; ESL typos; messy iterative notebook development                                                                                                                             |
| Sealy, Andre   | **LOW-MODERATE** | **Confirmed AI assistance**: leftover ChatGPT instruction comment in `2.5_greeks.py` ("Replace your **main** block with this"). Rest of codebase is authentically student-written with typos, copy-paste patterns, missing files |


**No student appears to have wholesale AI-generated their submission.** Sealy has the only confirmed direct evidence of AI tool usage (a leftover instruction comment), but the assistance was targeted to one section (Greeks), not the full assignment.

---

## Per-Student Detailed Summaries

### 1. Choi, Sungwuk (LATE) - Est: 62-72

- **P1 (15-17)**: yfinance, FRED for rate; missing SPY/VIX descriptions; weak maturity explanation
- **P2 (35-40)**: Good BS/bisection/Newton; no Secant; thin commentary; suspicious high IVs (>1.0); large put-call parity diffs
- **P3 (18-22)**: Handwritten derivation OK; trapezoidal works; gamma* always 0.01 (unresolved)
- **Bonus**: 0 (not attempted)
- **Flags**: Placeholder Korean text "[여기에 입력]" in header; unprofessional formatting
- **Complement Code Review** (3 .py files + data):
  - Code is functional and correct in structure. BS, bisection (upper=5.0, tol=1e-6), Newton (analytical vega), put-call parity — all standard implementations
  - **Suspicious high IVs explained**: bisection upper bound is 5.0 (500%) and returns `mid` even when not fully converged; deep OTM options with wide spreads hit this ceiling. Data filtered for `volume>0` and `bid/ask>0` but no moneyness filter, so extreme OTM strikes inflate averages
  - **Put-call parity code is correct**: `C - P` vs `S - K*exp(-rT)` — differences likely arise from American exercise premia and wide bid-ask spreads, not code bugs
  - Part 3 uses `scipy.integrate.trapezoid` correctly; only searches over {0.001, 0.003, 0.01} — coarse grid explains gamma*=0.01 always
  - **AI assessment: LOW**. Typo `"Newton Methodi"` in comment; minimal/no docstrings; no type hints; FRED API key hardcoded; Korean text in report; casual coding style throughout. This is authentic student work

### 2. Chopra, Rohan - Est: 80-87

- **P1 (14-16)**: yfinance; VIX options NOT downloaded; no CSV export
- **P2 (42-46)**: Strong BS/bisection/Newton; 3D vol surface (bonus); good put-call parity with scatter plot; Greeks match well
- **P3 (24-27)**: All sub-parts addressed; extended gamma grid analysis
- **Bonus**: 0
- **Flags**: No Secant; some TSLA IVs >100% (deep OTM)

### 3. Fan, Kaiwen - Est: ~~25-35~~ → **REVISED: 55-65** (with companion notebook)

- **ALL PARTS (PDF)**: Prose descriptions only -- NO code, NO plots, NO tables, NO numerical results
- **Companion Notebook Found** (`HW_FE_621.ipynb` in Google Colab):
  - **Contains working code for ALL parts including bonus.** Every cell executed with outputs.
  - **P1**: yfinance download for TSLA, SPY, ^VIX with 5 expirations — functional
  - **P2**: BS, bisection, Newton all implemented; put-call parity computed; 2D vol smile + 3D surface plots generated. **CRITICAL BUG: IV averaging produces -14,720,758** — the `analyze_row` function computes a fallback IV but stores raw Newton output (including diverged negative values), poisoning all downstream averages. Student clearly never reviewed their own output
  - **P3**: AMM expected fee revenue function + sigma×gamma table + optimal gamma plot present
  - **P4 (Bonus)**: Both integrals with 4 grid pairs; f1=xy gives machine-epsilon error; f2 converges cleanly
  - **Missing from notebook**: Q8 IV tables with commentary, Secant/Muller method, any written analysis
  - **Score revision rationale**: Student clearly did the computational work (Colab execution artifacts confirm genuine runtime, real dates, `files.upload()`/`files.download()` pattern), but the PDF deliverable was fatally incomplete with no code/plots/tables. Recommend **55-65** as middle ground: acknowledge work done but penalize heavily for incomplete deliverable
  - **AI assessment: LOW-TO-MODERATE**. Mostly human: typo `"# PArt 1 data downloading"`, personal workflow notes (`"I downloaded Day 1 on 2/11/26"`), sloppy short variable names, real unfixed bugs (-14.7M average never noticed), duplicated function definitions across cells, Colab upload/download workflow. One possible AI-assisted section: the `expected_revenue` AMM function (only function with a docstring, most polished code — the unfamiliar DeFi topic is exactly where a student would consult an LLM). **Not wholesale AI-generated**
- **Flags**: PDF was indeed a summary of Colab work; critical IV bug unnoticed; `iv_map` has key collision risk (strike,type without symbol/expiry); gamma_num uses wrong center value in FD

### 4. Friedman, Samuel - Est: 92-97 + 9-10 bonus

- **P1 (19-20)**: Excellent download pipeline; organized CSV output; FRED for rate; bonus CSV export
- **P2 (46-49)**: All questions complete; bisection + Newton + Secant all coded; 3D vol surface; thorough Greeks
- **P3 (27-29)**: Complete trapezoidal integration; table + plot; thin commentary
- **P4 (9-10)**: Both integrals, 4 grid pairs, convergence analysis
- **Flags**: Minor: VIX European/American caveat missing; some typos in Q2 explanation

### 5. Gahan, Cian (LATE) - Est: 51-59 + 2-4 bonus

- **P1 (14-16)**: Used SPX instead of SPY (acknowledged); Bloomberg-like code referenced externally
- **P2 (33-37)**: Good BS/bisection/Newton; Q11 Greeks cell UNEXECUTED (TODO comment left in); no Secant
- **P3 (4-6)**: Only Case 1 algebraic derivation; Q3b and Q3c entirely missing ("unable to finish")
- **P4 (2-4)**: Analytical correct; numerical code buggy (dumps arrays instead of sum)
- **Flags**: SPX/SPY error; incomplete Part 3; unexecuted code cells
- **Complement Code Review** (`hw1.ipynb`):
  - `BlackScholes` class is well-structured with `@staticmethod` methods, `_d1_d2` helper, analytical + FD Greeks, bisection + Newton IV solvers
  - **SPX vs SPY**: Student explicitly acknowledges the error in a prominent red NOTE. Argues results should be "very similar" — partially correct for IV purposes, but exercise specified SPY. Interestingly, SPX (European) is more appropriate for BS analysis than SPY (American)
  - **Q11 Greeks**: Code is fully implemented in the `BlackScholes` class (both analytical and FD), but the application cell contains only `# TODO: choose options subset to calculate greeks on; compare results for each` — never executed
  - **Part 3**: Contains substantial handwritten quadratic-formula derivations for AMM delta-x/delta-y but no code; trails off mid-work
  - **Part 4 Bonus bug confirmed**: `trapezoid_integrate` uses `x` and `y` (full numpy arrays) instead of loop variables `xi` and `yi` in `4*f(x+dx/2, y+dy/2)` — causes function to return arrays instead of scalar sums
  - `**timeval` bug**: `np.max(value, 0)` should be `np.maximum(value, 0)` — `np.max` treats second arg as `axis`, not comparison value
  - Newton warnings: RuntimeWarning divide-by-zero/overflow due to no sigma clamping when Newton overshoots to negative — noisy but handled via NaN return
  - **AI assessment: LOW**. Strong human indicators: personal/conversational writing style ("I misread the assignment instructions", "Was unable to finish"), inconsistent code style (f-strings mixed with string concatenation), sparse practical comments, genuine TODO markers, incomplete sections trail off mid-work, real bugs persist in output, MacOS file paths confirm personal machine. **Not AI-generated**

### 6. Garg, Achintya - Est: 78-87

- **P1 (15-17)**: yfinance; adequate data; option symbols not explicitly discussed
- **P2 (40-44)**: Good implementations; 3D vol surface (bonus); Newton timing 5x faster; no Secant
- **P3 (23-26)**: All parts present; no written commentary on results
- **Bonus**: 0
- **Flags**: Very minimal written analysis throughout; code-heavy submission

### 7. Gil, Joseph - Est: 72-80

- **P1 (18-20)**: Solid data gathering with third-Friday logic
- **P2 (36-42)**: Good BS/Newton; timing comparison (3.7x); 3D scatter plots; no Secant
- **P3 (18-22)**: Q3a-b solid; Q3c has coarse gamma grid, all gamma*=0.01
- **Bonus**: 0
- **Flags**: Code as images; sparse comments; minimal writing

### 8. Hsieh, Tzuling - Est: 82-90 + 8-10 bonus

- **P1 (17-19)**: Good descriptions; option symbol format explained; only 1 day clearly shown
- **P2 (40-44)**: All parts done; Newton has many "vega is zero" failures; Greeks diffs show 0.0 (rounding)
- **P3 (27-30)**: Thorough derivations; well-presented; good commentary
- **P4 (8-10)**: f1 exact, f2 converges; 4 grid sizes; commentary on why f1 is exact
- **Flags**: Extensive Newton failures for OTM options; missing appendix with full code; typo "Queation"
- **Complement Code Review** (3 notebooks: `11.ipynb`, `3.ipynb`, `4.ipynb` + data CSVs):
  - **Newton failure root cause identified**: Missing sigma clamping after Newton update step. When Newton overshoots to negative sigma, the guard clause `if sigma <= 0: return 0.0` in `bs_vega` triggers, causing 131 cascading "vega is zero" failures. Trivially fixable with `sigma = max(0.001, sigma)` — a well-known pitfall the student didn't catch
  - Notebook `11.ipynb` covers Parts 1-2 with full execution; `3.ipynb` handles AMM (Part 3); `4.ipynb` handles bonus integration
  - Code is functional with messy Jupyter exploration workflow and some duplicate function definitions across cells
  - **AI assessment: LOW** (80-85% human-authored). Strongest evidence: **bilingual Chinese/English comments** (`總寬度`, `轉成微秒`, `若未收斂`) scattered through the code — clearly a native Chinese speaker's working notes. Also: consistent ESL typos ("bond" for "bound", "Calsculate"), unresolved bug output left in notebook, messy iterative development pattern. **Not AI-generated**

### 9. Kelleher, Jackson - Est: 52-60 + 5-7 bonus

- **P1 (13-15)**: R with quantmod; admits downloading data after deadline on Feb 15
- **P2 (28-32)**: BS/bisection/Newton/Secant all coded; Secant returns NA for most options; Q12 MISSING
- **P3 (6-8)**: Q3a handwritten derivation only; Q3b formula but no code; Q3c entirely missing
- **P4 (5-7)**: Analytical correct; numerical with 4 pairs and error plot
- **Flags**: Late data download; broken Secant method; Part 3 mostly incomplete; raw R console output

### 10. Khaw, Steven - Est: 83-91 + 8-10 bonus

- **P1 (15-17)**: Good data; missing maturity explanation; TTM via business days/252
- **P2 (42-46)**: Complete all questions; 3D plots; good commentary on TSLA vs SPY
- **P3 (26-28)**: Handwritten derivation + code; all sub-parts
- **P4 (8-10)**: 6 grid pairs (exceeds requirement); both functions
- **Flags**: Informal tone ("im too lazy"); only calls used for IV; Jupyter format not LaTeX/Word

### 11. Khosla, Tasha - Est: 78-88

- **P1 (16-18)**: LaTeX report; code in separate file (not in PDF)
- **P2 (35-40)**: Newton IV for TSLA ATM = 0.2 vs bisection 0.42 (major discrepancy); many IVs hit bound of 5.0
- **P3 (27-30)**: Thorough derivations; boxed results; good presentation
- **Bonus**: 0
- **Flags**: Newton convergence bug; IV boundary contamination; code not verifiable from PDF alone
- **Complement Code Review** (3 .py files: `part1.py`, `part2.py`, `part3.py`):
  - **Newton convergence bug root cause found**: In `newtons_method`, convergence check uses `if numerator < tolerance` instead of `if abs(numerator) < tolerance` — missing `abs()`. For puts where BS price > market price, the numerator is negative and never satisfies `< tolerance`, so Newton iterates to max_iterations and returns a poorly converged value. This directly explains the TSLA ATM discrepancy (0.2 vs 0.42) and the IVs hitting bound of 5.0
  - `part1.py`: Well-structured download script using `pathlib.Path`, `os.makedirs(exist_ok=True)`, `fast_info` fallback chain, third-Friday filtering. Notably polished
  - `part2.py`: Clean functional design. `get_bs_call_or_put_fn` returns closures — somewhat sophisticated pattern. Uses `math` module (not numpy) for scalar ops. `Callable[float]` type hint is incorrect (should be `Callable[[float], float]`) — genuine mistake
  - `part3.py`: AMM implementation with trapezoidal rule, 1M grid points, proper lognormal density. Uses underscored numeric literals (`1_000_000`). Well-structured with correct math (separate integrals for Case 1/Case 2 with proper bounds)
  - **AI assessment: LOW-TO-MODERATE**. Code is notably more polished than average student: consistent Python 3.10+ type hints (`tuple[str, str]`, `float | None`), clean `pathlib` usage, closure-based design patterns. However, the missing `abs()` bug and incorrect `Callable[float]` annotation are genuine mistakes. No docstrings, sparse comments. The polished style could indicate Copilot-assisted editing rather than wholesale generation. **Likely student-written with possible IDE-level AI assistance (Copilot autocomplete)**

### 12. Marton, Bence - Est: 87-93

- **P1 (18-20)**: Well-structured download; ^IRX for rate; 4 expirations
- **P2 (42-46)**: All parts; good IV tables; put-call parity with bid-ask check; no 3D plot
- **P3 (27-30)**: Complete with derivation, trapezoidal, table, plot, commentary
- **Bonus**: 0
- **Flags**: Bisection vs Newton IV discrepancy for short-dated options (0.514 vs 0.288)

### 13. Novoa Molina, Daniela - Est: 85-94

- **P1 (14-16)**: VIX options code present but VIX option results not shown
- **P2 (44-48)**: Strong -- Newton + Secant + bisection all implemented; 3D surfaces; thorough commentary
- **P3 (27-30)**: Handwritten but thorough derivation; trapezoidal with 40K points; table + plot
- **Bonus**: 0
- **Flags**: VIX options absent from results; Part 3 handwritten vs Parts 1-2 typeset

### 14. Ponce, Jorge - Est: 87-94 + 8-10 bonus

- **P1 (18-20)**: FRED for rate; organized CSV structure; good descriptions
- **P2 (42-46)**: All parts; no Secant; no 3D surface; placeholder timestamps unfilled
- **P3 (27-30)**: Complete with derivation + code + table + plot
- **P4 (8-10)**: Both integrals; 4 grid pairs; convergence analysis
- **Flags**: No Secant method; placeholder timestamps; no 3D vol surface

### 15. Randhawa, Simrat - Est: 80-89 + 7-9 bonus

- **P1 (14-16)**: Bloomberg via Rblpapi (unique in class); R for data + Python for analysis
- **P2 (42-46)**: Good implementations; 8+ plots including 3D; no Secant; no timing comparison
- **P3 (24-27)**: All parts; gamma* flat at 0.01; thin commentary
- **P4 (7-9)**: Analytical correct; 4 grid sizes; f1 exact; f2 converges
- **Flags**: Brief 1-page report; no Secant/timing; VIX options absent

### 16. Santos, Afonso - Est: 82-88

- **P1 (17-18)**: R with quantmod; data from local CSVs not API; good descriptions
- **P2 (44-47)**: ONLY STUDENT WITH ALL 3 METHODS (bisection + Newton + Secant); 3D plotly surfaces; SPY ATM IV anomaly (0.72%)
- **P3 (21-23)**: Handwritten derivation OK; trapezoidal works; Q3c commentary thin
- **Bonus**: 0
- **Flags**: SPY ATM IV suspiciously low; DATA2 collected 9:50am (no active quotes, Mid=0)

### 17. Sealy, Andre - Est: 72-82

- **P1 (18-20)**: Good data gathering; LaTeX format
- **P2 (34-40)**: No 3D; Newton uses FD for derivative (not analytical vega); no Secant; no timing numbers
- **P3 (26-30)**: Q3a-c all addressed; good commentary on volatility harvesting
- **Bonus**: 0
- **Flags**: Incomplete sentence on p.10; analytical vega not used in Newton; only 1 IV plot shown
- **Complement Code Review** (12 .py files in organized `FE621/` project directory with git repo):
  - **Newton FD confirmed**: `newton_raphson.py` is a generic root-finder using central finite differences `(f(x+dx) - f(x-dx)) / (2*dx)` with `dx=1e-5`. Never uses analytical vega for IV, even though `2.5_greeks.py` demonstrates the student knows the vega formula. Lazy but functional design choice
  - **Missing dependency**: `2.1_bisection_method.py` imports `from bisection import implied_vol` but no `bisection.py` exists in the submission — the bisection driver script cannot run
  - **Suspicious import**: `from pandas.core.base import SelectionMixin` in `2.1_bisection_method.py` — unused internal pandas import, likely autocomplete pollution or AI artifact
  - Code organization: Well-separated files by question number (1.1, 1.2, 2.1-2.6, 3.2, 3.3). Uses git. Modular design with shared `black_scholes.py` and `newton_raphson.py`
  - Human indicators: Typos (`"seperated"`, `"similiar"`, `"price_dff_day2"`); commented-out debug prints; unused `monthrange` import; copy-pasted `select_option_type` function across 5 files instead of shared module; `.copy()` misplacement bug in `2.3_call_put_parity.py`; crude 3-point gamma optimization
  - `1.2_download_vix.py` is the most obviously human-written: copy-pasted the same 3-line pattern 6 times instead of using a loop
  - **AI RED FLAG in `2.5_greeks.py` line 246**: Comment reads `"--- Replace your __main__ block with this (computes BOTH analytic and FDM greeks for calls+puts) ---"` — this is an **AI assistant instruction** the student forgot to remove. It's the voice of ChatGPT/Copilot directing the student, not a developer comment. Also: redundant re-imports inside `__main_`_ (numpy, pandas) suggest the block was pasted from an AI conversation
  - `x != x` NaN check idiom in `newton_raphson.py` — pattern commonly seen in AI-generated code (most students use `math.isnan()`)
  - **AI assessment: LOW-TO-MODERATE (~30-35%)**. Primarily student-written with **selective AI assistance on specific sections**. The leftover AI instruction in `2.5_greeks.py` is definitive proof of at least partial AI usage. However, the pervasive typos, copy-paste patterns, missing files, and real bugs across the codebase are consistent with authentic student work. The student likely wrote most code themselves and used ChatGPT to help with the Greeks computation. **Not wholesale AI-generated, but has confirmed evidence of targeted AI assistance (Greeks section)**

### 18. Smadi, Fallyn - Est: 45-53

- **P1 (16)**: Adequate data collection
- **P2 (32-36)**: h=100 for numerical Greeks (should be ~0.01); no Secant; no 3D; r2=0.00364 typo (10x off)
- **P3 (0)**: ENTIRELY MISSING -- no AMM content at all
- **Bonus**: 0
- **Flags**: Part 3 = 0/30; h=100 Greeks bug; interest rate typo; copy-paste bug in DATA2 code

### 19. Stiemer, Julius (LATE) - Est: 64-74 pre-penalty

- **P1 (16-18)**: yfinance; brief descriptions; 3 short-dated maturities
- **P2 (38-42)**: Good BS class; bisection + Newton; 3D surfaces (bonus); very sparse writing
- **P3 (10-14)**: Q3a handwritten; Q3b partially set up; Q3c MISSING
- **P4 (2-3)**: 2 analytical solutions only; no numerical verification
- **Flags**: Part 3c missing; minimal prose; handwritten pages look rushed

### 20. Takeshita, Bryan - Est: 81-89

- **P1 (17-19)**: TTM via exact seconds (precise); good rate sourcing
- **P2 (38-42)**: SPY Greeks table broken (deep ITM strikes chosen); IV=0 artifacts; no 3D
- **P3 (26-28)**: Complete; optimal gamma search over wider range; linear relationship found
- **Bonus**: 0
- **Flags**: SPY Greeks with Delta=1, Gamma=0, Vega=1e6; no Secant

### 21. Tartaglia, Austin - Est: 62-70 + 2-3 bonus

- **P1 (12-14)**: NO code in report; references external .py files; maturity inconsistency (uses weeklies in plots)
- **P2 (32-36)**: Has all 3 methods (bisection + Newton + Secant) in Q7; but no code shown; put-call parity avg = "N/A"
- **P3 (15-18)**: Q3a derivation MISSING; Q3b method unclear; Q3c table + plot + commentary present
- **P4 (2-3)**: Partial -- 2 functions, no analytical derivation shown
- **Flags**: Zero code in PDF; maturity data mismatch; Q3a missing

### 22. Tenreiro, James - Est: 88-93 + 7-8 bonus

- **P1 (17-19)**: R with quantmod + Yahoo JSON API; FRED for rate; clean code
- **P2 (42-46)**: Strong throughout; put-call parity with quantile analysis; error plots for Q12
- **P3 (28-30)**: Complete and well-implemented; convergence check included
- **P4 (7-8)**: Both integrals; 4 pairs; convergence commentary
- **Flags**: No Secant; no 3D surface; minimal inline code comments

### 23. Trivedi, Akarsh - Est: 77-86 + 8-10 bonus

- **P1 (14-16)**: DATA1 and DATA2 from SAME DAY (20 min apart) -- not two consecutive trading days
- **P2 (37-42)**: Good implementations; 3D surfaces; no Secant; no timing table
- **P3 (26-28)**: Complete; 40K grid points; good sigma-gamma analysis
- **P4 (8-10)**: Both integrals; 4 grid pairs; convergence shown
- **Flags**: Same-day data is major issue for Q2/Q12; DATA2 rate falls back to hardcoded 0.05

### 24. Vishwakarma, Amit - Est: 82-91 + 7-10 bonus

- **P1 (18-20)**: Well-structured download; multi-asset CSV (bonus); good descriptions
- **P2 (40-44)**: Newton NaN for deep ITM; 3D trisurf plots; good commentary; no Secant
- **P3 (24-27)**: Complete; extended gamma search [0.0005, 0.5]; good plot
- **Bonus (7-10)**: P1 bonus + Q10 3D bonus
- **Flags**: Newton NaN unresolved; put-call parity methodology (one-sided check)

### 25. Yao, Yuhang - Est: 79-85

- **P1 (16-18)**: Lost VIX/SPY day-1 data (accidentally deleted)
- **P2 (40-44)**: Good; 3D scatter plots; IV=0 artifacts; Q12 only TSLA (lost data)
- **P3 (26-28)**: Trapezoidal + Monte Carlo validation (unique approach)
- **Bonus**: 0
- **Flags**: Lost data; IV=0 artifacts; divide-by-zero warnings; "Bouns" typo

### 26. Zachery, Justin (LATE) - Est: 80-87 pre-penalty

- **P1 (16-17)**: R with quantmod; clean LaTeX; VIX variance formula included
- **P2 (41-44)**: Good; microbenchmark timing; 3D plots (bonus); weak put-call parity analysis
- **P3 (24-26)**: Complete; step function for gamma* matches class pattern
- **Bonus**: 0 (Part 4 not attempted; but Q10 3D = +bonus within P2)
- **Flags**: No Secant; no option symbols; SPY IV artifacts (>5.0 for high strikes)

---

### Bug Root Causes Identified via Complement Code Review


| Student | Dashboard Flag                                          | Root Cause Found in Code                                                                                                                                            |
| ------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Choi    | Suspicious high IVs (>1.0), large put-call parity diffs | Bisection upper bound 5.0 with no moneyness filter; deep OTM options with wide spreads inflate results. Parity code is correct; diffs from American exercise premia |
| Hsieh   | 131 Newton "vega is zero" failures                      | Missing sigma clamping after update step; negative sigma triggers `return 0.0` in vega guard clause                                                                 |
| Khosla  | Newton IV = 0.2 vs bisection 0.42 (ATM discrepancy)     | Missing `abs()` in convergence check: `if numerator < tolerance` instead of `if abs(numerator) < tolerance`; negative errors never satisfy condition                |
| Fan     | No code in PDF (25-35 est.)                             | Code exists in companion Colab notebook; critical IV averaging bug (-14.7M) shows student never reviewed outputs                                                    |
| Gahan   | Part 4 dumps arrays instead of sum                      | `trapezoid_integrate` uses numpy array variables `x`,`y` instead of loop scalars `xi`,`yi` in midpoint term                                                         |
| Sealy   | Newton uses FD not analytical vega                      | Generic `newton_raphson.py` uses central FD with dx=1e-5; student knows analytical vega (in `2.5_greeks.py`) but chose lazy generic solver                          |


---

## Language Distribution

- **Python**: 21 students (81%)
- **R**: 4 students (Kelleher, Santos, Tenreiro, Zachery) (15%)
- **R+Python**: 1 student (Randhawa) (4%)

## Bonus Attempts (Part 4 Double Integral)

Attempted: Friedman, Hsieh, Kelleher, Khaw, Ponce, Randhawa, Tenreiro, Trivedi (8/26 = 31%)

## Grade Distribution Summary

- A range (85+): ~8 students
- B range (70-84): ~10 students
- C range (55-69): ~6 students (Fan revised up from F)
- D/F range (<55): ~2 students (Smadi, partial)

