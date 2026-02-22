# Volatility surface plotting (Q10)
# 2D: IV vs strike for nearest expiry (and all expiries overlaid)
# 3D: IV surface as a function of strike and time-to-maturity

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import config


def plot_2d_nearest_expiry(iv_df, output_dir=config.OUTPUT_DIR):
    if iv_df.empty:
        return

    nearest_exp = sorted(iv_df["Expiry"].unique())[0]
    subset = iv_df[iv_df["Expiry"] == nearest_exp].dropna(subset=["IV_Bisection"])

    for ticker, grp in subset.groupby("Ticker"):
        fig, ax = plt.subplots(figsize=(10, 6))
        for otype, marker, color in [("call", "o", "tab:blue"),
                                      ("put", "s", "tab:red")]:
            odf = grp[grp["Type"] == otype].sort_values("Strike")
            if not odf.empty:
                ax.plot(odf["Strike"], odf["IV_Bisection"],
                        marker=marker, linestyle="-", color=color,
                        label=f"{otype.title()}s", markersize=4, alpha=0.8)

        ax.set_title(f"{ticker} - Implied Volatility vs Strike ({nearest_exp})")
        ax.set_xlabel("Strike Price ($)")
        ax.set_ylabel("Implied Volatility")
        ax.legend()
        ax.grid(True, alpha=0.3)
        path = os.path.join(output_dir, f"{ticker.lower()}_iv_vs_strike_nearest.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  -> {path}")


def plot_2d_all_expiries(iv_df, output_dir=config.OUTPUT_DIR):
    # overlay all three maturities with different colors
    if iv_df.empty:
        return

    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    for ticker, tgrp in iv_df.groupby("Ticker"):
        fig, ax = plt.subplots(figsize=(10, 6))
        for idx, (exp, egrp) in enumerate(
                tgrp.dropna(subset=["IV_Bisection"]).groupby("Expiry")):
            calls = egrp[egrp["Type"] == "call"].sort_values("Strike")
            if not calls.empty:
                ax.plot(calls["Strike"], calls["IV_Bisection"],
                        marker="o", linestyle="-", color=colors[idx % len(colors)],
                        label=f"Calls {exp}", markersize=3, alpha=0.7)
            puts = egrp[egrp["Type"] == "put"].sort_values("Strike")
            if not puts.empty:
                ax.plot(puts["Strike"], puts["IV_Bisection"],
                        marker="s", linestyle="--", color=colors[idx % len(colors)],
                        label=f"Puts {exp}", markersize=3, alpha=0.5)

        ax.set_title(f"{ticker} - Implied Volatility vs Strike (All Expiries)")
        ax.set_xlabel("Strike Price ($)")
        ax.set_ylabel("Implied Volatility")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        path = os.path.join(output_dir, f"{ticker.lower()}_iv_all_expiries.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  -> {path}")


def plot_3d_surface(iv_df, output_dir=config.OUTPUT_DIR):
    # 3D scatter + interpolated surface: sigma(K, T)
    if iv_df.empty:
        return

    for ticker, tgrp in iv_df.groupby("Ticker"):
        valid = tgrp.dropna(subset=["IV_Bisection"])
        calls = valid[valid["Type"] == "call"]
        if calls.empty:
            continue

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection="3d")

        taus = calls["T"].values
        strikes = calls["Strike"].values
        ivs = calls["IV_Bisection"].values

        ax.scatter(strikes, taus, ivs, c=ivs, cmap="viridis",
                   s=10, alpha=0.8)

        # try to add interpolated surface on top of scatter
        try:
            from scipy.interpolate import griddata
            K_grid = np.linspace(strikes.min(), strikes.max(), 50)
            T_grid = np.linspace(taus.min(), taus.max(), 20)
            KK, TT = np.meshgrid(K_grid, T_grid)
            IV_grid = griddata((strikes, taus), ivs, (KK, TT),
                               method="linear")
            ax.plot_surface(KK, TT, IV_grid, alpha=0.4, cmap="viridis",
                            edgecolor="none")
        except Exception:
            pass

        ax.set_xlabel("Strike ($)")
        ax.set_ylabel("Time to Maturity (years)")
        ax.set_zlabel("Implied Volatility")
        ax.set_title(f"{ticker} - 3D Volatility Surface")
        path = os.path.join(output_dir, f"{ticker.lower()}_vol_surface_3d.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  -> {path}")


def run_vol_surface(iv_df):
    print("=" * 78)
    print("Q10 - VOLATILITY SURFACE PLOTS")
    print("=" * 78)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    plot_2d_nearest_expiry(iv_df)
    plot_2d_all_expiries(iv_df)
    plot_3d_surface(iv_df)
    print()


if __name__ == "__main__":
    print("Run via main.py (needs IV data).")
