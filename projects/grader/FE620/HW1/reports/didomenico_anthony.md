# Grading Report: Anthony DiDomenico

**Course**: FE620  
**Assignment**: Homework 1  
**Grader**: Automated

---

## Problem 1.1 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| F* | $5,229.85 | $5,229.88 | ✓ |
| Part i profit | $26.75 | ~$29.88 | ✓* |
| Part ii profit | $73.25 | ~$70.12 | ✓* |

**Comments**: Used F*=5226.75 (simple compounding). Both arbitrage strategies correctly identified. Acceptable variation in methodology.

---

## Problem 1.2 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Annual | 3.276% | 3.276% | ✓ |
| Quarterly | 3.236% | 3.237% | ✓ |
| Continuous | 3.224% | 3.224% | ✓ |

**Comments**: All correct.

---

## Problem 1.3 (17/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Balance | $10,141.10 | $10,130.95 | -3 |

**Comments**: Used simple APR/365 daily rate instead of converting from annual compounding. Common error — the problem states APR is "annualized compounding" meaning (1+APR)^(1/365)-1 is the correct daily rate. Deduct 3 points for ~$10 error.

---

## Problem 1.4 (15/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| B1 Price | $102.03 | $102.83 | -2 |
| B2 Price | $109.4 | $111.84 | -2 |
| B1 YTM | 3.45% | 3.49% | -1 |
| B2 YTM | 4.45% | 4.47% | ✓ |

**Comments**: Used discrete compounding for discount factors instead of continuous (e^(-rt)). This led to lower bond prices. Formula approach is valid but doesn't match the zero rate convention (typically continuous).

---

## Problem 1.5 (17/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Gain | $25,000 | $25,000 | ✓ |
| Rate differential | 4.545% | 8.89% | -3 |

**Comments**: Part ii is incorrect. Used simple interest approximation instead of continuous compounding formula: r_USD - r_EUR = (1/T) × ln(F/X0) = 2 × ln(1.15/1.10) = 8.89%.

---

## Final Grade: 89/100

**Confidence**: HIGH — Typed PDF with clear formatting.

**Notes**: Good understanding of concepts but needs to be more careful about compounding conventions (discrete vs continuous).
