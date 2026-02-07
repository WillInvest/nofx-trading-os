# Implementation Plan — On-Chain Trustless FBA

## Overview

Target: Solidity smart contracts for EVM-compatible chains

## Phases

### Phase 1: Prototype Commit-Reveal Batch Auction
- [ ] Basic order commitment contract
- [ ] Reveal and batch execution logic
- [ ] Uniform clearing price calculation
- [ ] Basic tests in Foundry

### Phase 2: Add Cryptographic Enhancements
- [ ] Evaluate threshold encryption integration
- [ ] Consider time-lock puzzle approach
- [ ] Implement chosen enhancement

### Phase 3: Gas Optimization
- [ ] Profile gas costs
- [ ] Optimize storage patterns
- [ ] Consider L2 deployment

### Phase 4: Security Audit Prep
- [ ] Formal verification where possible
- [ ] Invariant testing
- [ ] Edge case analysis

### Phase 5: Testnet Deployment
- [ ] Deploy to Sepolia/Goerli
- [ ] Integration testing with real wallets
- [ ] Performance benchmarking

## Technical Stack

- **Language**: Solidity 0.8.x
- **Framework**: Foundry
- **Testing**: Forge tests + fuzzing
- **Deployment**: Foundry scripts

## Key Contracts

```
contracts/
├── BatchAuction.sol       # Core auction logic
├── OrderCommitment.sol    # Commit-reveal handling
├── PriceDiscovery.sol     # Clearing price calculation
├── interfaces/
│   └── IBatchAuction.sol
└── libraries/
    └── OrderLib.sol
```

## Blockers
- Waiting on theoretical framework to solidify before implementation
- Need to decide on cryptographic approach

## Update Log
- [2026-02-04] Plan created
