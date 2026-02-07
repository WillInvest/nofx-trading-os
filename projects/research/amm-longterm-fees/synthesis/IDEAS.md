# Ideas — Estimating Long-Term LP Fee Revenue

## The Core Question
**If I provide liquidity for 1 year, what's my expected return?**

---

## Key Formula: Fee APY

```
Fee APY = (Trading Volume × Fee Rate) / TVL × 365
```

Or using the **V/R Ratio** (Volume-to-Reserve):
```
Daily V/R = Daily Volume / Pool Reserve
Fee APY ≈ Daily V/R × Fee Rate × 365
```

**Example** (from DeFi Prime research):
- V/R ratio of 1.0 with 0.3% fee = **~109% APY** from fees alone
- V/R ratio of 0.5 with 0.3% fee = **~55% APY**
- V/R ratio of 0.1 with 0.3% fee = **~11% APY**

---

## The Reality Check: Net Returns

### Formula for Net LP Returns:
```
Net Return = Fee Revenue - Impermanent Loss - Gas Costs
```

### Empirical Data (Uniswap v3, 2021):
| Metric | Value |
|--------|-------|
| Total Fees Earned | $199.3M |
| Total IL Incurred | $260.1M |
| Net Loss | -$60.8M |
| % LPs Profitable | 49.5% |

**Key insight**: On average, LPs **LOSE money** because IL > Fees.

---

## Estimating Your 1-Year Return

### Step 1: Estimate Fee Revenue
```
Fee Revenue = Your Liquidity × (Pool Volume / Pool TVL) × Fee Rate × 365
```

**Where to find data**:
- Pool volume: Dune Analytics, DeFi Llama
- Pool TVL: Uniswap Info, DeFi Llama
- Fee rate: 0.05% (stable), 0.3% (standard), 1% (volatile)

### Step 2: Estimate Impermanent Loss
```
IL = 2 × sqrt(price_ratio) / (1 + price_ratio) - 1
```

| Price Change | IL |
|--------------|-----|
| ±10% | -0.11% |
| ±25% | -0.6% |
| ±50% | -2.0% |
| ±75% | -3.8% |
| 2x (100%) | -5.7% |
| 3x (200%) | -13.4% |
| 5x (400%) | -25.5% |

**Key insight**: In volatile markets, IL can easily exceed fee income.

### Step 3: Calculate Net Return
```
Net Return = Fee Revenue - IL - Gas Costs
```

---

## Realistic Expectations by Pool Type

### Stablecoin Pairs (USDC/USDT)
- **Fee tier**: 0.01-0.05%
- **Expected IL**: Near zero
- **Typical APY**: 1-5% (low volume, but safe)

### Blue Chip Pairs (ETH/USDC)
- **Fee tier**: 0.05-0.3%
- **Expected IL**: 5-20% per year (high volatility)
- **Typical Net APY**: -10% to +15% (highly variable)

### Volatile Pairs (PEPE/ETH)
- **Fee tier**: 1%
- **Expected IL**: 20-50%+ per year
- **Typical Net APY**: Often negative despite high fees

---

## The Uncomfortable Truth

From research (Bancor/IntoTheBlock):
> "Over 51% of Uniswap v3 LPs were unprofitable due to impermanent losses exceeding their fee income."

### Why Most LPs Lose:
1. **Volatility kills**: Price movements cause IL that fees can't cover
2. **Adverse selection**: Arbitrageurs trade against LPs profitably
3. **Gas costs**: Frequent rebalancing erodes gains
4. **Wrong fee tier**: Mismatched fee to asset volatility

---

## Strategies for Positive Long-Term Returns

### 1. Stable Pairs Only
- Near-zero IL
- Lower but consistent returns
- Best for risk-averse LPs

### 2. Fee Tier Optimization
- Optimal fee = 70-80% of CEX spread (research finding)
- Higher volatility → Higher fee tier needed

### 3. Active Management (v3)
- Concentrate liquidity around current price
- Higher fee capture but higher IL risk
- Requires constant monitoring

### 4. Passive Wide Range (v3)
- Full range position (like v2)
- Lower fee capture but lower IL
- Better for long-term holding

### 5. Auto-Compounding
- Reinvest fees automatically
- Compounds returns over time
- KyberSwap, Gamma, Arrakis offer this

---

## Quick Estimation Tool

**Conservative estimate for 1-year ETH/USDC LP**:
```
Assumptions:
- Pool: ETH/USDC 0.3% fee
- Average daily volume: $50M
- Pool TVL: $100M
- Your position: $10,000
- ETH price change: ±50% over year

Fee Revenue:
= $10,000 × ($50M / $100M) × 0.3% × 365
= $10,000 × 0.5 × 0.003 × 365
= $5,475 (54.75% APY from fees)

Impermanent Loss (50% price move):
= $10,000 × 2.0%
= $200

Net Return:
= $5,475 - $200 = $5,275 (52.75% APY)
```

**BUT**: This assumes consistent volume. Real returns vary wildly.

---

## Research Gaps

1. **Multi-year studies**: Most research covers months, not years
2. **Compounding effects**: Limited data on reinvestment impact
3. **Market regime analysis**: Bull vs bear LP profitability
4. **Cross-cycle returns**: How do LPs perform over full crypto cycles?

---

## Bottom Line

**Expected 1-year return for LPs**:
- **Stablecoin pairs**: 1-10% APY (relatively safe)
- **Blue chip pairs**: -20% to +30% (high variance)
- **Volatile pairs**: Often negative (high risk)

**The harsh reality**: Without active management or stable pairs, most LPs underperform simply holding the assets.
