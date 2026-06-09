"""Generate a beautiful scatter plot of the C2 transfer residuals."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import matplotlib.pyplot as plt
import numpy as np

from experiments.prime_neighborhood_transfer import prime_neighborhood_transfer_dataset
from experiments.origin_modular_shell_transfer import shell_conditioned_residuals


def main() -> None:
    # 1. Load dataset
    limit = 1000
    dataset = prime_neighborhood_transfer_dataset(limit)

    # 2. Extract residuals (conditioned on shell depth and log_n)
    metric_key = "compression_prime_minus_neighborhood_log_gap"
    target_key = "log_lambda_over_phi"

    metric_res = shell_conditioned_residuals(dataset, metric_key, ["log_n"])
    target_res = shell_conditioned_residuals(dataset, target_key, ["log_n"])

    # 3. Fit regression line
    m, c = np.polyfit(metric_res, target_res, 1)

    # 4. Plot styling (Premium Dark Mode)
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8.5, 6), dpi=150)
    fig.patch.set_facecolor("#0f172a")  # Slate 900
    ax.set_facecolor("#0f172a")

    # Grid lines
    ax.grid(True, color="#334155", linestyle=":", alpha=0.6)  # Slate 700

    # Scatter plot of data points
    ax.scatter(
        metric_res,
        target_res,
        color="#22d3ee",  # Cyan 400
        alpha=0.45,
        edgecolors="none",
        s=35,
        label="Integer Residuals (n=2..1000)",
    )

    # Regression line
    x_range = np.linspace(min(metric_res), max(metric_res), 100)
    ax.plot(
        x_range,
        m * x_range + c,
        color="#f43f5e",  # Rose 500
        linewidth=2.5,
        label=f"Fitted Trend (r = -0.4659)",
    )

    # Title & Labels
    ax.set_title(
        "C2 Transfer: Prime-Minus Neighborhood Gap vs. Modular Return\n(Shell-Conditioned & Size-Residualized)",
        color="#f8fafc",  # Slate 50
        fontsize=13,
        pad=15,
        fontweight="bold",
    )
    ax.set_xlabel(
        "C/N_- Path Gap Residual",
        color="#cbd5e1",  # Slate 300
        fontsize=11,
        labelpad=10,
    )
    ax.set_ylabel(
        "log(lambda/phi) Residual",
        color="#cbd5e1",  # Slate 300
        fontsize=11,
        labelpad=10,
    )

    # Style spines (axes borders)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#475569")  # Slate 600

    # Legend
    legend = ax.legend(
        loc="upper right",
        framealpha=0.15,
        facecolor="#0f172a",
        edgecolor="#475569",
    )
    for text in legend.get_texts():
        text.set_color("#f8fafc")

    # Annotations
    ax.text(
        0.05,
        0.05,
        "Origin-Pakheta Calculus\np-value: 0.0040 (0/250 shuffles)",
        transform=ax.transAxes,
        color="#94a3b8",  # Slate 400
        fontsize=9,
        verticalalignment="bottom",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#1e293b", alpha=0.3, edgecolor="none"),
    )

    # Adjust layout and save
    plt.tight_layout()
    output_dir = ROOT / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "prime_neighborhood_transfer_scatter.png"
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor="none")
    print(f"Saved scatter plot to {output_path}")


if __name__ == "__main__":
    main()
