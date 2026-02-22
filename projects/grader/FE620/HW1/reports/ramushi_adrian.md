# Grading Report: Adrian Ramushi

**Course**: FE620  
**Assignment**: Homework 1  
**Grader**: Automated

---

## Problem 1.1 (15/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| F* | $5,229.88 | $5,229.88 | ✓ |
| Part i | "No arbitrage" | Arbitrage exists | -5 |
| Part ii | "No arbitrage" | Arbitrage exists | ✓* |

**Comments**: Part i is WRONG — student says "no arbitrage" but arbitrage exists when market forward ($5,200) < theoretical forward ($5,229.88). The reverse cash-and-carry is profitable. Part ii correctly identifies no arbitrage exists when F=$5,300 > F*... wait, actually both parts have arbitrage opportunities in the problem. Student's reasoning is confused.

**Revised**: Student says i) no arbitrage because $5200 < $5229.88 (wrong interpretation — this IS arbitrage opportunity). Says ii) there IS arbitrage when $5300 > $5229.88 (correct). Deduct 5 for part i logic error.

---

## Problem 1.2 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Annual | 3.276% | 3.276% | ✓ |
| Quarterly | 3.24% | 3.237% | ✓* |
| Continuous | 3.23% | 3.224% | ✓* |

**Comments**: Minor rounding but acceptable.

---

## Problem 1.3 (18/20)

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Balance | $10,141.92 | $10,130.95 | -2 |

**Comments**: Used simple APR/365 instead of proper daily rate conversion. Common error.

---

## Problem 1.4 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| B1 Price | $102.8314 | $102.83 | ✓ |
| B2 Price | $111.8428 | $111.84 | ✓ |
| B1 YTM | 3.5214% | 3.49% | ✓* |
| B2 YTM | 4.5152% | 4.47% | ✓* |

**Comments**: Bond prices perfect. YTMs use discrete compounding convention — acceptable variation.

---

## Problem 1.5 (20/20) ✓

| Item | Student Answer | Correct Answer | Status |
|------|----------------|----------------|--------|
| Gain | $25,000 | $25,000 | ✓ |
| Rate differential | 8.8904% | 8.89% | ✓ |

**Comments**: Perfect.

---

## Final Grade: 93/100

**Confidence**: HIGH — Excel screenshots with clear values.

**Notes**: Strong quantitative work but confused arbitrage logic in 1.1i. Need to review when market price below theoretical = arbitrage opportunity (reverse cash-and-carry).
