# Grading Report: Ishaan Siwach

**Course**: FE620  
**Assignment**: Homework 1  
**Grader**: Automated

---

## Problem 1.1 (18/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| F* | $5,229.88 | $5,229.88 | ✓ |
| Part i profit | $29.88 | ~$29.88 | ✓ |
| Part ii | "No arbitrage" | Arbitrage exists | -2 |

**Comments**: Part i correct. Part ii is WRONG — student says "No arbitrage opportunity exists" when F=$5,300 > F*=$5,229.88. This IS an arbitrage (cash-and-carry): borrow, buy gold at spot, short forward at $5,300, deliver at maturity for $70.12 profit.

---

## Problem 1.2 (19/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Annual | 3.28% | 3.276% | ✓* |
| Quarterly | 3.24% | 3.237% | ✓ |
| Continuous | 3.23% | 3.224% | ✓ |

**Comments**: Minor rounding on annual (3.28% vs 3.276%). Acceptable.

---

## Problem 1.3 (17/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Balance | $10,141.92 | $10,130.95 | -3 |

**Comments**: Used simple APR/365 daily rate. Common interpretation error.

---

## Problem 1.4 (19/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| B1 Price | $102.83 | $102.83 | ✓ |
| B2 Price | $111.84 | $111.84 | ✓ |
| B1 YTM | 3.534% | 3.49% | -1 |
| B2 YTM | 4.546% | 4.47% | ✓* |

**Comments**: Bond prices correct. YTMs slightly off — using discrete vs continuous compounding convention.

---

## Problem 1.5 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Gain | $25,000 | $25,000 | ✓ |
| Rate differential | 8.89% | 8.89% | ✓ |

**Comments**: Perfect.

---

## Final Grade: 93/100

**Confidence**: HIGH — Well-formatted with Excel screenshots.

**Notes**: Good overall. Critical error on 1.1ii — need to review arbitrage conditions. When market forward > theoretical forward, cash-and-carry arbitrage exists.
