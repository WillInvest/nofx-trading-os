# Theory — AMM LVR Mitigation

## Foundational Mathematics

### The LVR Formula

From Milionis et al. (2022), for a constant-product AMM (x·y = k):

**Instantaneous LVR:**
```
dLVR = (σ²/8) × L × dt
```

Where:
- σ = instantaneous volatility of the price process
- L = marginal liquidity (≈ √k for CPMM)
- dt = infinitesimal time

**Integrated LVR over [0, T]:**
```
LVR(T) = (1/8) × L × ∫₀ᵀ σ²(t) dt = (1/8) × L × σ² × T  (if σ constant)
```

### Impermanent Loss vs LVR

**IL** = Discrete comparison: LP value vs HODL at time T
**LVR** = Continuous extraction: cumulative arbitrageur profits

Relationship (Milionis et al.):
```
E[LVR] = E[IL] + convexity adjustment
```

For practical purposes: LVR ≥ IL always, and LVR is the "true cost"

### Fee Offset Condition

For LP to break even (ignoring other costs):
```
Fee Revenue ≥ LVR
```

With fee rate f and volume V:
```
f × V ≥ (σ²/8) × L × T
```

Rearranging for minimum fee:
```
f_min = (σ² × L × T) / (8 × V)
```

---

## Oracle-Based Pricing Theory

### UAMM Model (Im et al., 2023)

Let p_oracle be the external oracle price, p_amm be the AMM marginal price.

Standard CFMM: p_amm determined by reserves (x, y)
UAMM: p_trade = f(p_oracle, p_amm) where f ensures no arbitrage when p_oracle = true price

**Arbitrage condition:**
```
Arbitrage profit = |p_oracle - p_amm| × trade_size - fees
```

If AMM always trades at p_oracle: arbitrage profit = 0

**Trust assumption:** Oracle must be:
1. Accurate (reflects true market price)
2. Timely (updated faster than arbitrageurs can act)
3. Manipulation-resistant

---

## Batch Auction Theory

### FM-AMM (Canidio & Fritsch, 2023)

**Key insight:** If all trades in a batch execute at a single clearing price, arbitrageurs compete to set that price correctly.

**Mechanism:**
1. Collect orders during batch interval [t, t+Δ]
2. Find clearing price p* that maximizes trading function value
3. All trades execute at p*

**Why LVR = 0:**
- In equilibrium, arbitrageurs bid the clearing price to p* = true market price
- No stale price → no arbitrage profit
- Surplus (difference from naive execution) → LPs

**Formal result:**
```
Under competitive batch auctions: E[LVR] = 0
```

### Batch Duration Trade-off

Shorter batch → Better UX (lower latency)
Longer batch → More competition → better price discovery

Optimal Δ depends on:
- Number of arbitrageurs
- Transaction costs
- Volatility

---

## Dynamic Fee Theory

### Optimal Fee Framework (Campbell et al., 2025)

Model: AMM competes with CEX; traders choose venue based on execution cost.

**Optimal fee under Stackelberg game:**
```
f* = argmax_{f} E[Fee Revenue - LVR | f]
```

**Key findings:**
1. Under normal volatility: f* ≈ CEX trading cost (competitive)
2. Under high volatility: f* → high (protective)
3. Threshold policy is near-optimal:
   ```
   f = f_low   if σ < σ_threshold
   f = f_high  if σ ≥ σ_threshold
   ```

### Volatility Estimation

**On-chain methods:**
- TWAP deviation: |P_current - TWAP| / TWAP
- Realized vol: √(Σ(log returns)²)
- External oracle (Chainlink Volatility Index)

**Challenge:** Vol estimation lags true vol; high vol arrives suddenly

---

## Hedging Theory

### LP Position Greeks

A Uniswap v2 LP position in ETH/USDC has:

**Delta (Δ):** Exposure to ETH price
```
Δ_LP = 0.5 × (reserves in ETH)
```
(Always 50% exposed at current price)

**Gamma (Γ):** Rate of delta change
```
Γ_LP = -L / (4 × P^(3/2)) < 0
```
LP has **negative gamma** — delta decreases as price rises

**This is the source of IL/LVR:** Negative gamma means LP is short volatility.

### Hedging Strategies

**Delta hedge:** Short perps/futures to neutralize Δ
- Requires continuous rebalancing
- Cost: funding rate + slippage

**Gamma hedge:** Buy options or power perps to offset negative Γ
- Power perpetuals: payoff = P² (positive gamma = 2)
- Options: buy straddle (positive gamma near strike)

**Perfect hedge condition:**
```
Γ_LP + Γ_hedge = 0
```

Using Squeeth (power perp with payoff P²):
```
Squeeth needed = |Γ_LP| / 2
```

---

## Auction Mechanism Theory

### McAMM (MEV Capturing AMM)

**Auction design:**
- Sell right to be first trader in block
- Winner pays price reflecting expected MEV
- Payment → LPs

**Equilibrium:** Winning bid = E[MEV] in competitive auction

**Limitation:** MEV includes non-LVR components (sandwich, etc.)

### am-AMM (Harberger Lease)

**Mechanism:**
- Continuous auction for "manager" role
- Manager pays rent proportional to self-assessed valuation
- Anyone can buy manager role by paying current valuation
- Manager sets fees, captures arb

**Equilibrium:** Manager valuation = E[Arbitrage profit] - risk premium

---

## Synthesis: Comparing Approaches

| Approach | LVR Reduction | Mechanism | Trust |
|----------|--------------|-----------|-------|
| Oracle | ~100% | Price from external source | Oracle |
| FM-AMM | ~100% | Competitive batch pricing | Solver/sequencer |
| Dynamic fees | ~50-80%* | Fee ≥ LVR during high vol | None |
| Hedging | ~90%+ | External derivatives | Derivatives market |
| Auction rights | ~100% | Sell MEV to highest bidder | Auction mechanism |

*Depends on vol estimation accuracy and threshold calibration

---

## Open Theoretical Questions

1. **Lower bound on fees for LVR break-even without external info?**
   - Can pure on-chain data achieve competitive fees?

2. **Optimal batch duration formula?**
   - Δ* = f(n_arbs, σ, gas_cost, ...)?

3. **Composition effects?**
   - Does Oracle + Batch + Dynamic Fees give >100% protection?
   - Or diminishing returns?

4. **Concentrated liquidity adjustments?**
   - LVR formula for Uniswap v3 ranges?
   - (More complex; range affects L locally)

---

## Formulas to Implement

### 1. LVR Calculator
```python
def lvr_estimate(volatility, liquidity, time_hours):
    """Estimate LVR for constant-product AMM"""
    sigma_sq = volatility ** 2
    time_years = time_hours / (24 * 365)
    return (sigma_sq / 8) * liquidity * time_years
```

### 2. Optimal Fee Threshold
```python
def optimal_fee_threshold(base_fee, vol_threshold, current_vol):
    """Simple threshold-based dynamic fee"""
    if current_vol < vol_threshold:
        return base_fee
    else:
        # Scale fee with excess volatility
        return base_fee * (1 + (current_vol - vol_threshold) / vol_threshold)
```

### 3. Hedge Ratio Calculator
```python
def squeeth_hedge_amount(liquidity, price):
    """Squeeth needed to gamma-hedge LP position"""
    gamma_lp = -liquidity / (4 * price ** 1.5)
    squeeth_gamma = 2  # per unit
    return abs(gamma_lp) / squeeth_gamma
```

---

## New Theoretical Insights (2026-02-07)

### Fee Non-Additivity (Bartoletti et al., 2026)

**Formally proven in Lean 4**: With fee parameter φ ∈ (0, 1):

```
swap(Δx₁ + Δx₂) > swap(Δx₁) + swap(Δx₂)  when φ < 1
```

The fee structure breaks additivity. A single large trade yields strictly more output than splitting.

**Implication for arbitrage:**
The closed-form arbitrage solution with fees is unique:
```
Δx* = f(reserves, external_price, φ)
```
(Exact formula in paper — involves solving quadratic with fee adjustment)

**Implication for LP strategy:**
- Fee revenue is **sub-additive** in number of trades
- Pool with few large trades ≠ pool with many small trades (same total volume)
- Suggests fee structure should account for trade size distribution

### LVR as Option Theta (Singh et al., 2025) ⭐ MAJOR

**Central result**: LVR is analytically identical to the continuous funding fees (theta) of an embedded at-the-money continuous-installment (CI) option.

**Continuous-Installment Option Model**:
A CI option is an exotic option where the holder pays a continuous premium stream (installments) while holding the option. The holder can stop paying at any time (exercise/abandon).

**Mapping to AMM LP:**
- LP deposits ≈ buying a CI option portfolio
- Fee income ≈ installment payments received
- LVR ≈ theta decay of the CI option
- Withdrawal ≈ exercising the abandonment right

**Formal equivalence:**
```
LVR = θ_{CI}(ATM)
```
Where θ_{CI}(ATM) is the time decay of the at-the-money CI option in the replicating portfolio.

**Practical implications:**
1. **Constant-LVR profiles exist**: Can choose liquidity range/depth such that LVR is approximately constant regardless of price path
2. **Calibration method**: Use implied volatility term structure to set constant vol parameter
3. **Forward-looking LVR**: LPs can estimate expected adverse selection for arbitrary time windows
4. **Position optimization**: Choose parameters to target specific LVR rate acceptable to LP

**Formula for constant-LVR boundary:**
```python
def constant_lvr_boundaries(target_lvr_rate, implied_vol, risk_free_rate, time_window):
    """
    Compute price boundaries for approximately constant LVR
    Based on CI option theta calibration
    """
    # Uses implied vol calibration from term structure
    # Boundaries define a range where delta profile matches constant-LVR condition
    # See arXiv:2508.02971 for full derivation
    pass  # Implementation requires numerical methods
```

### LP Token as Derivative (Bichuch & Feinstein, 2026)

**Key insight**: LP tokens should be priced as derivatives on underlying assets, not at naive pool share valuation.

**Black-Scholes analogy for AMMs:**
- Standard: Option value = f(S, K, σ, r, T)
- LP token: V_LP = g(P, L, σ, fees, ...)

**Risk-neutral pricing:**
Under no-arbitrage, a hedged LP position should grow at risk-free rate:
```
d(V_LP - Δ × S) = r × (V_LP - Δ × S) × dt
```

**Empirical finding**: On-chain LP token prices deviate from risk-neutral valuation — suggesting either:
1. Market inefficiency (arbitrage opportunity)
2. Hidden risk premiums not captured in model
3. Liquidity/friction effects

**Volatility calibration:**
Can back out "implied LP volatility" from observed LP token prices:
```
σ_implied = solve for σ such that V_model(σ) = V_market
```

This provides updated (non-market) valuation consistent with continuous hedging.

**Connection to LVR:**
- Both papers treat LP as options holder
- Singh: LVR = theta (time decay)
- Bichuch/Feinstein: LP value = derivative with Greeks

**Combined framework:**
```
LP Greeks:
- Delta (Δ): Exposure to underlying price
- Gamma (Γ): Rate of delta change (negative for LP)
- Theta (θ): Time decay ≈ -LVR rate
- Vega (ν): Sensitivity to volatility
```

### Volatility Buffering Effect (Computational Economics, 2026)

**Empirical finding**: V-S pools exhibit lower IL sensitivity to external volatility shocks.

**Formal model**: Let IL_t denote impermanent loss at time t.
```
IL_t = α + β₁ × CVI_t + β₂ × VIX_t + γ × IL_{t-1} + ε_t
```

Key parameters estimated:
- γ > 0 (IL is autoregressive)
- β_V-S < β_V-V (buffering effect: V-S pools have lower vol sensitivity)

**Practical formula for IL forecasting:**
```python
def forecast_il(prev_il, cvi, vix, pool_type):
    """Forecast next period IL using AR model"""
    alpha = POOL_ALPHA[pool_type]
    beta_cvi = POOL_BETA_CVI[pool_type]
    beta_vix = POOL_BETA_VIX[pool_type]
    gamma = POOL_GAMMA[pool_type]
    return alpha + beta_cvi * cvi + beta_vix * vix + gamma * prev_il
```

---

## Thermodynamic Framework (Meister, 2026)

### CPMM as Carnot Engine

A novel perspective: view CPMM as a multi-phase thermodynamic cycle.

**Phase mapping:**
| AMM Action | Thermo Phase | Energy Flow |
|------------|--------------|-------------|
| Liquidity taker swap | Work extraction | ΔW = fees - slippage |
| Price adjustment | Adiabatic process | Internal state change |
| LP deposit | Reservoir coupling | Heat input (new capital) |
| LP withdrawal | Reservoir decoupling | Heat output |

**Efficiency concept:**
Like a heat engine, CPMM has "efficiency" bounded by Carnot limit:
```
η_AMM = (Fee Revenue) / (Fee Revenue + LVR) ≤ η_Carnot
```

The "entropy leak" = LVR: irreversible loss to informed traders.

### Market Impact Derivation

**Standard assumption**: Linear price impact (many DEXs use this)
```
ΔP = λ × V  (linear in volume V)
```

**Meister result**: For optimal-growth LPs facing random walk prices:
```
ΔP = λ × √V  (square-root impact)
```

This matches the classic Kyle (1985) result from traditional market microstructure!

**Extension to fractional O-U:**
For mean-reverting prices with Hurst exponent H:
```
ΔP = λ × V^(H+1/2)
```

**Implication**: 
- H = 0.5 (random walk) → square-root impact
- H < 0.5 (mean-reverting) → sub-linear impact
- H > 0.5 (trending) → super-linear impact

### Entropy and LVR Connection

In thermodynamics: ΔS ≥ 0 (entropy always increases)

In AMM context:
```
Entropy generation = LVR / T_effective
```

Where T_effective is related to volatility (higher vol = "higher temperature" system)

**Physical intuition**: 
- LVR is "waste heat" — energy that cannot be captured as useful work
- More volatile markets = "hotter" systems = more entropy generation
- Perfect efficiency impossible (2nd law analog)

### Catastrophe Risk for Stablecoins

Meister models stablecoin depeg as a fold catastrophe:

**State variable**: Stablecoin price P
**Control variable**: Market stress / flight-to-safety demand

**Bifurcation condition**: When control exceeds threshold, system jumps from stable equilibrium (P ≈ 1) to unstable region (P << 1).

**Insurance pricing:**
```
Premium = E[Depeg Loss] × P(Catastrophe)
```

Using catastrophe bond mathematics:
```
Premium = Loss_max × ∫ p(x) × I(x > x_crit) dx
```

Where p(x) is stress distribution, x_crit is depeg threshold.

**Connection to LP strategy:**
LPs in stablecoin pools face jump risk not captured by standard IL/LVR models. The catastrophe framework provides risk pricing for this tail exposure.

---

## Unified LVR Framework (Emerging)

### Multi-Perspective Equivalence

Recent work suggests deep connections between different LVR characterizations:

| Framework | LVR Analog | Mathematical Object |
|-----------|------------|-------------------|
| Options (Singh) | Theta (θ) | Time decay rate |
| Thermodynamics (Meister) | Entropy production (dS/dt) | Irreversibility |
| Microstructure (Milionis) | Adverse selection cost | Information rent |
| Derivatives (Bichuch) | Hedging cost | Replication error |

**Conjecture**: These are all manifestations of the same underlying phenomenon:

```
LVR ≡ θ_option ≡ T × (dS/dt) ≡ λ × σ² ≡ (∂V/∂t + ½σ²S²∂²V/∂S² + ...)
```

Where the last term is the BSM PDE residual for a hedged LP position.

### Implications for Unified Theory

If this equivalence holds, LVR mitigation can be approached from any perspective:
1. **Options lens**: Reduce theta by managing option-like exposure
2. **Thermo lens**: Minimize entropy production (irreversibility)
3. **Microstructure lens**: Reduce information asymmetry
4. **Derivatives lens**: Improve replication accuracy

**Research direction**: Develop category-theoretic framework where these perspectives are functorially equivalent.
