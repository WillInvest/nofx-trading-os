// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Test.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {Hooks} from "v4-core/src/libraries/Hooks.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {BalanceDelta} from "v4-core/src/types/BalanceDelta.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {CurrencyLibrary, Currency} from "v4-core/src/types/Currency.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {Deployers} from "@uniswap/v4-core/test/utils/Deployers.sol";
import {OutputFeeHook} from "../code/OutputFeeHook.sol";

contract OutputFeeHookTest is Test, Deployers {
    using PoolIdLibrary for PoolKey;
    using CurrencyLibrary for Currency;

    OutputFeeHook hook;
    PoolId poolId;

    uint24 constant FEE_RATE = 30; // 0.30% in basis points

    function setUp() public {
        // Deploy v4 core contracts
        deployFreshManagerAndRouters();
        (currency0, currency1) = deployMintAndApprove2Currencies();

        // Deploy our hook
        address hookAddress = address(
            uint160(Hooks.AFTER_SWAP_FLAG | Hooks.AFTER_SWAP_RETURNS_DELTA_FLAG)
        );
        deployCodeTo("OutputFeeHook.sol:OutputFeeHook", abi.encode(manager, FEE_RATE), hookAddress);
        hook = OutputFeeHook(hookAddress);

        // Initialize pool with hook
        (key, ) = initPool(
            currency0,
            currency1,
            IHooks(address(hook)),
            3000, // 0.3% swap fee (not used since we do output fee)
            SQRT_PRICE_1_1,
            ZERO_BYTES
        );
        poolId = key.toId();

        // Add liquidity
        modifyLiquidityRouter.modifyLiquidity(
            key,
            IPoolManager.ModifyLiquidityParams({
                tickLower: -60,
                tickUpper: 60,
                liquidityDelta: 10 ether,
                salt: bytes32(0)
            }),
            ZERO_BYTES
        );
    }

    function test_OutputFeeIsCharged() public {
        // Swap token0 for token1
        bool zeroForOne = true;
        int256 amountSpecified = -1 ether; // exact input
        
        uint256 token1Before = currency1.balanceOfSelf();
        
        BalanceDelta swapDelta = swap(key, zeroForOne, amountSpecified, ZERO_BYTES);
        
        uint256 token1After = currency1.balanceOfSelf();
        uint256 received = token1After - token1Before;
        
        // Check that fee was accumulated
        uint256 accumulatedFee = hook.getAccumulatedFees(currency1);
        assertGt(accumulatedFee, 0, "Fee should be accumulated");
        
        // The user should receive less than the gross swap output
        // Fee should be approximately 0.3% of output
        uint256 grossOutput = received + accumulatedFee;
        uint256 expectedFee = (grossOutput * FEE_RATE) / 10000;
        
        assertApproxEqRel(accumulatedFee, expectedFee, 0.01e18, "Fee should be ~0.3% of output");
    }

    function test_OutputFeeAccumulatesCorrectToken() public {
        // Swap token0 → token1: fee should accumulate in token1
        swap(key, true, -1 ether, ZERO_BYTES);
        assertGt(hook.getAccumulatedFees(currency1), 0, "Should accumulate token1 fees");
        
        uint256 token0FeesBefore = hook.getAccumulatedFees(currency0);
        
        // Swap token1 → token0: fee should accumulate in token0
        swap(key, false, -1 ether, ZERO_BYTES);
        assertGt(
            hook.getAccumulatedFees(currency0), 
            token0FeesBefore, 
            "Should accumulate token0 fees"
        );
    }

    function test_OutputFee_LPAccumulatesAppreciatingAsset() public {
        // This test demonstrates the key insight:
        // When many users buy token1, LPs accumulate token1 (the appreciating asset)
        
        // Simulate many buys of token1 (selling token0)
        for (uint i = 0; i < 10; i++) {
            swap(key, true, -0.1 ether, ZERO_BYTES);
        }
        
        // Fees should be accumulated in token1 (the bought/appreciating token)
        uint256 token1Fees = hook.getAccumulatedFees(currency1);
        assertGt(token1Fees, 0, "Should have accumulated token1 fees");
        
        // Under input fees, LPs would have accumulated token0 (the sold token)
        // Under output fees, LPs accumulate token1 (the bought token)
        // In a rising market for token1, output fees give LPs the winner
    }
}
