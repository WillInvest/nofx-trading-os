# FE620 HW1 Answer Key & Grading Rules

## Correct Answers

### Problem 1.1 (10 pts)
- **F* = $5,229.88** (= 5050 × e^0.035)
- Part a: If F > F*, short forward + buy spot → arbitrage profit
- Part b: If F < F*, long forward + short spot → arbitrage profit

### Problem 1.2 (20 pts)
Given: r₂ = 3.25% (semi-annual compounding)
- **i) Annual: r₁ = 3.2764%** (= (1 + 0.0325/2)² - 1)
- **ii) Quarterly: r₄ = 3.2369%** (= 4×[(1.01625)^0.5 - 1])
- **iii) Continuous: rc = 3.2239%** (= 2×ln(1.01625))

### Problem 1.3 (20 pts)
Given: 17.15% APR annual compounding, $10,000 deposit, 30 days
**Correct approach:** Convert to daily rate first!
- r_daily = 365 × [(1 + 0.1715)^(1/365) - 1] ≈ 15.82%
- Balance = 10000 × (1 + r_daily/365)^30 = **$10,130.95**

**WRONG approach (deduct 5 pts):**
- Simply using 10000 × (1 + 0.1715/365)^30 = $10,140.46 ← INCORRECT
- This ignores the rate conversion requirement

### Problem 1.4 (20 pts)
Zero rates: 0-1yr: 3%, 1-2yr: 3.5%, 2-5yr: 4.25%, 5-10yr: 4.5%

**Bond 1 (5% coupon, 2yr):**
- Price: **$102.83**
- YTM: **3.491%** (continuous)

**Bond 2 (6% coupon, 10yr):**
- Price: **$111.84**
- YTM: **4.465%** (continuous)

### Problem 1.5 (10 pts)
- **i) Gain = $25,000** (= 1M × (1.175 - 1.150))
- **ii) r_USD - r_EUR = 8.89%** (= (1/0.5) × ln(1.15/1.10))

---

## Grading Rules

1. **Rounding tolerance:** If math/formula is correct but numerical result differs due to rounding, **NO DEDUCTION**
2. **Problem 1.3:** **-5 points** if they did NOT convert to daily rate (just used 17.15%/365)
3. **Extract their math:** Show what they wrote, compare with correct
4. **Confidence levels:** HIGH / MEDIUM / LOW based on image clarity
5. **Total: 80 points**
