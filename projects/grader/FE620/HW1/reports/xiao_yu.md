# Grading Report: Yu Xiao

**Course**: FE620  
**Assignment**: Homework 1  
**Grader**: Automated

---

## Problem 1.1 (18/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| F* | $5,229 | $5,229.88 | ✓ |
| Part i profit | $29 | ~$29.88 | ✓ |
| Part ii profit | $71 | ~$70.12 | ✓ |

**Comments**: Correct approach. Part i strategy description is slightly confused — mentions "borrow $5050, buy gold, enter long forward at $5200" but arbitrage here should be reverse cash-and-carry (short gold, invest, long forward). Logic is inverted but numbers are approximately correct. Minor deduction for strategy description.

---

## Problem 1.2 (19/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Annual | 3.27% | 3.276% | ✓ |
| Quarterly | 3.23% | 3.237% | ✓ |
| Continuous | 3.22% | 3.224% | ✓ |

**Comments**: All correct, minor rounding.

---

## Problem 1.3 (17/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Balance | $10,141.96 | $10,130.95 | -3 |

**Comments**: Used continuous compounding A×e^(r×n) instead of discrete daily compounding. This gives slightly different result. The problem states daily compounding, not continuous.

---

## Problem 1.4 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| B1 Price | $102.83 | $102.83 | ✓ |
| B2 Price | $111.8428 | $111.84 | ✓ |
| B1 YTM | 3.49% | 3.49% | ✓ |
| B2 YTM | 4.47% | 4.47% | ✓ |

**Comments**: Perfect. All bond prices and yields correct.

---

## Problem 1.5 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Gain | $25,000 | $25,000 | ✓ |
| Rate differential | 8.89% | 8.89% | ✓ |

**Comments**: Perfect.

---

## Final Grade: 94/100

**Confidence**: HIGH — Clear typed submission.

**Notes**: Strong work. Be careful about compounding conventions — daily ≠ continuous.
