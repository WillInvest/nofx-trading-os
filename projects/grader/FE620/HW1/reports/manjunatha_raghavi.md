# Grading Report: Raghavi Manjunatha

**Course**: FE620  
**Assignment**: Homework 1  
**Grader**: Automated (Text Extraction)

---

## Problem 1.1 (15/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| F* | $5,226.75 | $5,229.88 | ✓* |
| Part i | "Arbitrage exists" | Correct | ✓ |
| Part ii | "Arbitrage does not exist" | WRONG | -5 |

**Comments**: 
- Part i: Correctly identifies arbitrage when F=$5,200 < F*
- Part ii: **WRONG** — says "arbitrage does not exist" when F=$5,300 > F*=$5,226.75. Arbitrage DOES exist via cash-and-carry.

⚠️ **CRITICAL ERROR**: Same conceptual mistake as Freire — misunderstanding of when arbitrage exists.

---

## Problem 1.2 (18/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Annual | 3.2764% | 3.276% | ✓ |
| Quarterly | 3.28% | 3.237% | -2 |
| Continuous | 3.227% | 3.224% | ✓ |

**Comments**: Quarterly rate appears to use wrong formula (shows same as annual).

⚠️ **UNCERTAINTY**: Text shows "r = 3.28%" for quarterly which should be ~3.237%. Possible transcription error or wrong calculation.

---

## Problem 1.3 (17/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Balance | $10,141.00 | $10,130.95 | -3 |

**Comments**: Used simple APR/365 approach.

---

## Problem 1.4 (12/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| B1 Price | $100.71 | $102.83 | -3 |
| B2 Price | $108.90 | $111.84 | -3 |
| B1 YTM | 4.64% | 3.49% | -2 |
| B2 YTM | 4.47% | 4.47% | ✓ |

**Comments**: Bond prices significantly off. Used discrete discounting (1/(1+r)^t) instead of continuous (e^(-rt)).

⚠️ **CRITICAL ISSUE**: B1 price of $100.71 is way too low. B1 YTM of 4.64% is too high. These indicate systematic calculation errors.

---

## Problem 1.5 (15/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Gain | "Loss of $25,000" | Gain of $25,000 | -3 |
| Rate differential | 4.44% | 8.89% | -2 |

**Comments**: 
- Gain interpretation WRONG — called it a "loss" when it's actually a gain
- Rate differential used wrong formula: ln(1.15/1.10) = 4.44% (not annualized)

⚠️ **CRITICAL ERRORS**: Multiple conceptual issues in Problem 1.5.

---

## Final Grade: 77/100

**Confidence**: MEDIUM — Text extraction clear, but multiple calculation errors visible.

**Uncertainty Summary**:
1. **Problem 1.1ii**: Conceptual error (says no arbitrage when it exists)
2. **Problem 1.4**: Systematic discounting errors (discrete vs continuous)
3. **Problem 1.5**: Wrong interpretation of gain/loss AND rate differential formula

**Recommendation**: This student needs feedback on:
- When arbitrage exists (F < F* AND F > F* both create opportunities)
- Continuous vs discrete discounting for bond pricing
- Covered interest parity formula with proper annualization
