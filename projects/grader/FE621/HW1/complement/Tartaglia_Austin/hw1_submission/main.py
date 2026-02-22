# FE621 Homework 1 - main orchestrator
# Runs all parts sequentially and generates output files

import os
import sys

os.makedirs("output", exist_ok=True)


def main():
    print("=" * 78)
    print("  FE621 COMPUTATIONAL FINANCE - HOMEWORK 1")
    print("=" * 78 + "\n")

    # Q3: descriptions
    from descriptions import print_descriptions, save_descriptions
    print_descriptions()
    save_descriptions("output/q3_descriptions.txt")

    # Q1-Q4: data gathering
    from data_gathering import gather_all
    data = gather_all()

    # Q5: BS sanity check
    from black_scholes import bs_call_price, bs_put_price
    print("=" * 78)
    print("Q5 - BLACK-SCHOLES SANITY CHECK")
    print("=" * 78)
    c = bs_call_price(100, 100, 1.0, 0.05, 0.2)
    p = bs_put_price(100, 100, 1.0, 0.05, 0.2)
    print(f"  bs_call_price(100, 100, 1, 0.05, 0.2) = {c:.4f}  (expect ~10.4506)")
    print(f"  bs_put_price (100, 100, 1, 0.05, 0.2) = {p:.4f}  (expect ~ 5.5735)\n")

    # Q6-Q8: implied volatility
    from implied_vol import run_implied_vol
    iv_df = run_implied_vol(data)

    # Q9: put-call parity
    from put_call_parity import run_put_call_parity
    run_put_call_parity(data)

    # Q10: volatility surface plots
    from vol_surface import run_vol_surface
    if iv_df is not None and not iv_df.empty:
        run_vol_surface(iv_df)

    # Q11: Greeks
    from greeks import run_greeks
    if iv_df is not None and not iv_df.empty:
        run_greeks(iv_df, data["risk_free_rate"])

    # Q12: reprice with DATA2
    from data2_pricing import run_data2_pricing
    if iv_df is not None and not iv_df.empty:
        run_data2_pricing(iv_df, data)

    # Part 3: AMM fee revenue
    from amm_fee_revenue import run_amm
    run_amm()

    # Part 4: bonus double integration
    from bonus_integration import run_bonus
    run_bonus()

    print("=" * 78)
    print("  ALL DONE - check output/ folder for CSVs and plots")
    print("=" * 78)


if __name__ == "__main__":
    main()
