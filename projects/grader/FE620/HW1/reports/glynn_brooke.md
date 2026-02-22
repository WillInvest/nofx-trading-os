# Grading Report: Brooke Glynn

**Course**: FE620  
**Assignment**: Homework 1  
**Grader**: Automated

---

## Problem 1.1 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| F* | $5,229.88 | $5,229.88 | ✓ |
| Part i profit | $29.88 | ~$29.88 | ✓ |
| Part ii profit | $70.12 | ~$70.12 | ✓ |

**Comments**: Correct formula and implementation in R. Arbitrage logic properly identified.

---

## Problem 1.2 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Annual | 3.2764% | 3.276% | ✓ |
| Quarterly | 3.2369% | 3.237% | ✓ |
| Continuous | 3.2239% | 3.224% | ✓ |

**Comments**: All conversions correct with proper precision.

---

## Problem 1.3 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Balance | $10,130.95 | $10,130.95 | ✓ |

**Comments**: Correctly converted APR to equivalent daily rate using (1+APR)^(1/365) - 1, then compounded. This is the proper interpretation of APR as annual compounding rate.

---

## Problem 1.4 (19/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| B1 Price | $102.831 | $102.83 | ✓ |
| B2 Price | $111.843 | $111.84 | ✓ |
| B1 YTM | 3.521% | 3.49% | -1 |
| B2 YTM | 4.516% | 4.47% | ✓* |

**Comments**: Bond prices correct. YTM for B1 slightly off (3.521% vs 3.49%) — appears to use discrete semi-annual compounding convention vs continuous. Minor methodology difference.

---

## Problem 1.5 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Gain | $25,000 | $25,000 | ✓ |
| Rate differential | 8.890% | 8.89% | ✓ |

**Comments**: Perfect. Correctly applied covered interest parity.

---

## Final Grade: 99/100

**Confidence**: HIGH — R code output cleanly extracted, all formulas visible.

**Notes**: Excellent submission with code. Only minor deduction for YTM convention difference.
