# Grading Report: Anna Hauk

**Course**: FE620  
**Assignment**: Homework 1  
**Grader**: Automated (Image Analysis)

---

## Problem 1.1 (18/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| F* | $5,226.76 | $5,229.88 | ✓* |
| Part i profit | $26.75 | ~$29.88 | ✓* |
| Part ii profit | $73.25 | ~$70.12 | ✓* |

**Comments**: Used simple compounding (1+r) instead of continuous (e^r). Both arbitrage strategies correctly identified.

⚠️ **UNCERTAINTY**: Simple vs continuous compounding - verify course convention.

---

## Problem 1.2 (19/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Annual | 3.28% | 3.276% | ✓ |
| Quarterly | 3.24% | 3.237% | ✓ |
| Continuous | 3.22% | 3.224% | ✓ |

**Comments**: All correct with minor rounding.

---

## Problem 1.3 (17/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Balance | $10,141.93 | $10,130.95 | -3 |

**Comments**: Used simple APR/365 approach.

---

## Problem 1.4 (19/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| B1 Price | $102.83 | $102.83 | ✓ |
| B2 Price | $111.85 | $111.84 | ✓ |
| B1 YTM | 3.52% | 3.49% | ✓ |
| B2 YTM | 4.52% | 4.47% | -1 |

**Comments**: Bond prices correct. YTMs slightly off due to discrete compounding convention.

---

## Problem 1.5 (17/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Gain | $25,000 | $25,000 | ✓ |
| Rate differential | 9.09% | 8.89% | -3 |

**Comments**: Gain correct. Rate differential WRONG — student used simple interest formula instead of continuous compounding.

⚠️ **UNCERTAINTY**: Student's formula appears to be: (F-X0)/X0 / T = (1.15-1.1)/1.1/0.5 = 9.09%

Correct formula (covered interest parity, continuous): r = (1/T) × ln(F/X0) = 2 × ln(1.15/1.1) = 8.89%

This is a conceptual error, not just numerical.

---

## Final Grade: 90/100

**Confidence**: HIGH — Clear handwritten work with color highlighting.

**Uncertainty Summary**:
1. Problem 1.1: Simple vs continuous compounding
2. Problem 1.5ii: Used wrong formula for rate differential (conceptual error)
