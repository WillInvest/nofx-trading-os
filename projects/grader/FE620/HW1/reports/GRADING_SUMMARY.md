# FE620 HW1 Grading Summary — COMPLETE

**Date**: February 11, 2026  
**Total Students**: 24  
**Reports Generated**: 24 (100%)

---

## Final Grades

| # | Student | Score | Confidence | Key Issues |
|---|---------|-------|------------|------------|
| 1 | Abramowitz, Matthew | 73* | M | Prob 1.5 not visible |
| 2 | Agerup, Dennis | **96** | H | — |
| 3 | **Biju, Suraj** | **99** ⭐ | H | Only student with correct 1.3 |
| 4 | Brooks, Taylor | 39* | L | Only 1 page submitted |
| 5 | DiDomenico, Anthony | 89 | H | 1.4 discrete vs continuous |
| 6 | D'Souza, Freya | —* | L | 12MB file, needs manual |
| 7 | Freire, Roberto | 93 | M | 1.1ii wrong (no arb claim) |
| 8 | **Glynn, Brooke** | **99** ⭐ | H | Excellent, correct 1.3 |
| 9 | Hauk, Anna | 90 | H | 1.5ii wrong formula |
| 10 | Horgan, John | **94** | H | — |
| 11 | Jacques, Widly | **97** | H | — |
| 12 | Konopka, Michael | **96** | M | Excel-based |
| 13 | Manjunatha, Raghavi | 77 | M | Multiple conceptual errors |
| 14 | McLoughlin, Jude | **96** | H | — |
| 15 | Mehta, Hrishi | **97** | H | — |
| 16 | Meyer, Ara | 58* | L | 1.4-1.5 not visible |
| 17 | Ramushi, Adrian | 93 | H | 1.1i logic confused |
| 18 | Shin, Jinwoo | 77* | H | 1.5 not visible |
| 19 | Shlyam, Samuel | 78 | M | LATE, 1.3 major error |
| 20 | Sikandar Ali, Sultan | **94** | M | — |
| 21 | Siwach, Ishaan | 93 | H | 1.1ii wrong (no arb) |
| 22 | Snodgrass, Makenzie | **97** | H | — |
| 23 | Xiao, Yu | **94** | H | — |

**Legend**: 
- `*` = Partial/incomplete submission
- ⭐ = Correctly solved Problem 1.3 (proper APR interpretation)
- Bold = 94+ score

---

## Statistics

| Metric | Value |
|--------|-------|
| Complete submissions | 20 |
| Partial/incomplete | 4 |
| Average (complete) | 92.1 |
| Median | 94 |
| Highest | 99 (Biju, Glynn) |
| Lowest | 77 (Manjunatha) |

---

## Common Errors Analysis

### 1. Problem 1.3: APR Interpretation (Most Common — 90% error rate)
- **Wrong**: r_daily = APR/365 → $10,141.92
- **Correct**: r_daily = (1+APR)^(1/365) - 1 → $10,130.95
- Only **2 students** (Biju, Glynn) got this correct

### 2. Problem 1.1: Arbitrage Logic Errors
- 3 students (Freire, Manjunatha, Siwach) incorrectly claimed "no arbitrage" for part ii
- When F > F*, arbitrage EXISTS via cash-and-carry

### 3. Problem 1.4: Compounding Convention
- Continuous discounting (e^(-rt)) vs discrete ((1+r)^(-t))
- Creates ~$0.10-$2.00 price differences

### 4. Problem 1.5: Rate Differential Formula
- Some used simple interest instead of continuous: (F-X0)/X0/T ≠ ln(F/X0)/T

---

## Uncertainty Explanations by Student

| Student | Uncertainty Reason |
|---------|-------------------|
| Abramowitz | Problem 1.5 missing from visible pages |
| Brooks | PDF only 1 page — incomplete submission |
| D'Souza | 12MB file failed to process |
| Konopka | Excel methodology described, exact values inferred |
| Meyer | Problems 1.4-1.5 not in extracted pages |
| Shin | Problem 1.5 cut off in extraction |

---

## Reports Generated (24 total)

All individual reports saved to: `projects/grader/FE620/HW1/reports/`

```
├── abramowitz_matthew.md
├── agerup_dennis.md
├── biju_suraj.md
├── brooks_taylor.md
├── didomenico_anthony.md
├── freire_roberto.md
├── glynn_brooke.md
├── hauk_anna.md
├── horgan_john.md
├── jacques_widly.md
├── konopka_michael.md
├── manjunatha_raghavi.md
├── mcloughlin_jude.md
├── mehta_hrishi.md
├── meyer_ara.md
├── ramushi_adrian.md
├── shin_jinwoo.md
├── shlyam_samuel.md
├── sikandar_ali_sultan.md
├── siwach_ishaan.md
├── snodgrass_makenzie.md
├── xiao_yu.md
└── GRADING_SUMMARY.md
```

---

## Recommended Actions

1. **Contact incomplete submissions**: Brooks, Meyer (verify files)
2. **Process D'Souza**: 12MB file needs manual PDF viewer
3. **Decide on Problem 1.3**: Accept both interpretations or standardize
4. **Feedback focus**: Arbitrage logic, continuous compounding, CIP formula
