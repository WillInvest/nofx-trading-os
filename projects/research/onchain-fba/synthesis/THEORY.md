# Theoretical Development — On-Chain Trustless FBA

## Definitions

### Trustless
A mechanism is **trustless** if no participant must trust any other party to behave honestly for the mechanism to function correctly. Security relies only on cryptographic assumptions and economic incentives.

### Front-Running
A front-running attack occurs when an adversary observes a pending transaction and submits their own transaction to execute before it, profiting from the price impact.

### Frequent Batch Auction (FBA)
Orders collected over a time interval are executed simultaneously at a uniform clearing price, eliminating ordering-based advantages.

## Formal Model

### Setting
- Set of traders $T = \{t_1, ..., t_n\}$
- Each trader $t_i$ has order $o_i = (d_i, q_i, p_i)$ where:
  - $d_i \in \{buy, sell\}$ is direction
  - $q_i > 0$ is quantity
  - $p_i$ is limit price
- Time divided into batches of duration $\Delta$

### Desiderata
1. **Privacy**: Order contents hidden until batch execution
2. **Fairness**: No trader can gain advantage from order timing within batch
3. **Liveness**: Batches always clear if valid orders exist
4. **Efficiency**: Gas cost bounded by $O(n)$ or better
5. **Incentive Compatibility**: Truthful bidding is optimal

### Threat Model
- Adversary controls subset of validators/sequencers
- Adversary can observe mempool (unless encrypted)
- Adversary can submit arbitrary transactions
- Adversary wants to extract MEV via front-running/sandwiching

## Key Theorems (To Develop)

### Theorem 1: Impossibility of Perfect Trustlessness?
*Conjecture*: Any FBA mechanism with sub-block latency requires at least one trusted party.

### Theorem 2: Commit-Reveal Security
If hash function is collision-resistant, commit-reveal FBA achieves order privacy until reveal phase.

### Theorem 3: Threshold Encryption Trade-offs
*(To be developed based on literature)*

---

## Update Log
- [2026-02-04] Initial framework created
