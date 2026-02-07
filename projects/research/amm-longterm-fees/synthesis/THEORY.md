# Theory — Arbitrage-Driven AMM Fee Revenue

## Model Setup

### Assumptions
1. **External price** follows Geometric Brownian Motion (GBM):
   ```
   dP_t = μP_t dt + σP_t dW_t
   ```
   Where:
   - P_t = reference market price at time t
   - μ = drift (expected return)
   - σ = volatility
   - W_t = standard Brownian motion

2. **AMM price** is constrained within bounds:
   ```
   P_t / (1+φ) ≤ P_AMM ≤ P_t × (1+φ)
   ```
   Where φ = fee rate (e.g., 0.3% = 0.003)

3. **Only arbitrageurs trade**: When |P_AMM - P_external| > φ, arbitrage is profitable

---

## Key Results from Literature

### 1. LVR Formula (Loss-Versus-Rebalancing)
From Milionis et al. (2022):
```
LVR = σ² / 8 × L × dt
```
Where:
- σ = volatility (annualized)
- L = liquidity
- dt = time period

**Interpretation**: LP loss to arbitrageurs scales with volatility squared.

### 2. Fee Revenue from Arbitrage
From "Arbitrage Driven Price Dynamics" (2024):

The AMM price **mean-reverts** to the reference price through arbitrage. Each arbitrage trade:
- Moves AMM price toward external price
- Pays fee φ to LPs

**Expected arbitrage frequency**:
```
λ_arb ∝ σ / φ
```
Higher volatility → More frequent arbitrage → More fees collected.

### 3. Arbitrage Profit vs LP Fee Revenue
From Moallemi et al. (2023):

Without fees:
```
Arbitrageur profit = LP loss (LVR)
```

With fees:
```
Arbitrageur profit = LVR - Fees paid
LP revenue = Fees paid
LP net loss = LVR - Fees = Arbitrageur profit
```

**Key insight**: Fees transfer value from arbitrageurs to LPs, but don't eliminate LVR.

---

## Long-Term Fee Revenue Estimation

### Formula
```
Annual Fee Revenue ≈ C × σ × √(Volume × TVL)
```

Where C is a constant depending on the AMM design.

### More Precise: Arbitrage-Only Model

From arxiv 2401.01526:

If external price P_t follows GBM with volatility σ:
```
E[Fee Revenue] = φ × E[Arbitrage Volume]
E[Arbitrage Volume] ∝ σ × L × T
```

Therefore:
```
E[Annual Fee Revenue] ≈ φ × k × σ × L
```

Where:
- φ = fee rate
- k = constant (≈ 2-4 depending on model)
- σ = annual volatility
- L = liquidity

### Numerical Example

**Parameters**:
- Fee rate φ = 0.3% = 0.003
- Volatility σ = 80% annual (typical for ETH)
- Liquidity L = $10M
- k ≈ 3 (empirical constant)

**Calculation**:
```
Annual Fee Revenue = 0.003 × 3 × 0.8 × $10M
                   = 0.0072 × $10M
                   = $72,000
```

**Fee APY** = $72,000 / $10M = **7.2%**

But LVR loss:
```
LVR = σ²/8 × L × 1 year
    = 0.64/8 × $10M
    = $800,000
```

**Net LP return** = Fee Revenue - LVR = $72,000 - $800,000 = **-$728,000** 😱

---

## The Fundamental Problem

### Why Arbitrage-Only Doesn't Work

The math shows:
```
Fee Revenue ∝ σ (linear)
LVR ∝ σ² (quadratic)
```

At high volatility, **LVR always dominates fee revenue**.

### Breakeven Condition
```
Fee Revenue ≥ LVR
φ × k × σ × L ≥ σ²/8 × L
φ × k ≥ σ/8
φ ≥ σ / (8k)
```

For σ = 80%, k = 3:
```
φ ≥ 0.8 / 24 ≈ 3.3%
```

**Implication**: For volatile assets, you need **3%+ fees** to break even from arbitrage alone!

---

## What Saves LPs: Non-Arbitrage Volume

In reality, AMMs also have:
1. **Retail traders** (price-insensitive)
2. **Noise traders** (random trades)
3. **Rebalancers** (portfolio adjustment)

These traders:
- Pay fees without exploiting mispricings
- Don't cause LVR
- Pure profit for LPs

### Revised Model
```
Total Fee Revenue = Arbitrage Fees + Non-Arb Fees
LP Net Return = (Arb Fees + Non-Arb Fees) - LVR
             = Non-Arb Fees - (LVR - Arb Fees)
             = Non-Arb Fees - Arbitrageur Profit
```

**Key insight**: LP profitability depends on **non-arbitrage volume ratio**.

---

## Estimation Framework

### For Long-Term Fee Revenue:

**Step 1**: Estimate total volume
```
Total Volume = Arbitrage Volume + Non-Arb Volume
```

**Step 2**: Decompose by type
```
Arb Volume ≈ k × σ × L × T
Non-Arb Volume = (observed total) - Arb Volume
```

**Step 3**: Calculate revenues
```
Fee Revenue = φ × Total Volume
```

**Step 4**: Calculate LVR
```
LVR = σ²/8 × L × T
```

**Step 5**: Net return
```
Net = Fee Revenue - LVR
```

---

## Practical Implications

### 1. Low Volatility = Better for LPs
- LVR ∝ σ² (quadratic)
- Stable pairs minimize LVR

### 2. High Non-Arb Ratio = Better for LPs
- More "organic" trading → More profit
- Meme coins often have high retail volume

### 3. Higher Fees Help (Up to a Point)
- Higher fees reduce arbitrage profitability
- But too high kills volume
- Optimal: ~70-80% of CEX spread

### 4. Concentrated Liquidity Trade-off
- Higher fee capture per dollar
- But also higher LVR per dollar
- Net effect depends on price range choice

---

---

## Long-Term Logarithmic Growth Rate

### Key Paper: "Growth rate of LP wealth in G3Ms" (arxiv 2403.18177)

This paper extends one-step fee analysis to **long-term expected logarithmic growth**.

**Core Approach**:
- Uses stochastic reflected diffusion processes
- Analyzes G3M dynamics under arbitrage-driven markets
- Calculates long-term expected log growth of LP wealth

**Key Formula** (simplified):
```
E[log(W_T/W_0)] / T → g  as T → ∞
```

Where g = long-term logarithmic growth rate of LP wealth.

**Factors determining g**:
1. Fee rate φ
2. Volatility σ
3. G3M type (weights, curvature)
4. Arbitrage frequency

**Extension from One-Step to Long-Term**:

| One-Step Analysis | Long-Term Analysis |
|-------------------|-------------------|
| Fee revenue per trade | Compounded fee growth |
| IL at time T | Average IL rate |
| Spot PnL | Logarithmic growth rate |

### From One-Step to Multi-Period

**One-step fee revenue**:
```
ΔFee = φ × Volume_step
```

**Multi-period compounding**:
```
W_T = W_0 × ∏(1 + r_t)
log(W_T/W_0) = Σ log(1 + r_t) ≈ Σ r_t  (for small r_t)
```

**Long-term growth rate**:
```
g = lim (T→∞) E[log(W_T/W_0)] / T
  = E[r] - Var(r)/2  (by Kelly criterion)
```

### Practical Implication

The paper shows that **fee revenue compounds** but so does **IL drag**. The long-term growth rate depends on the balance:

```
g ≈ (Fee Rate × Volume/TVL) - (σ²/8 per unit time) - (transaction costs)
```

For LP profitability: g > 0 required.

---

## Key Papers

1. **Growth rate of LP wealth in G3Ms** (arxiv 2403.18177) ⭐ KEY
   - Long-term logarithmic growth
   - Stochastic reflected diffusion
   - Extends to various G3M types

2. **Optimal Fees for G3Ms** (arxiv 2104.00446)
   - Fee optimization framework
   - LP value maximization

3. **Arbitrage driven price dynamics** (arxiv 2401.01526)
   - GBM + arbitrage model
   - Local time analysis

4. **Automated Market Making and Arbitrage Profits in Presence of Fees** (Moallemi)
   - Fee impact on arbitrage behavior
   - Breakeven analysis

5. **LVR II** (arxiv 2502.04097, Feb 2025)
   - GBM vs Brownian comparison
   - Long-term dynamics

6. **Fees in AMMs: Quantitative Study** (arxiv 2406.12417)
   - Empirical simulation
   - Directional fee optimization
