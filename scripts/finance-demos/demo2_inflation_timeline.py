#!/usr/bin/env python3
"""
Demo Video 2: US Inflation Crisis Timeline (1970–2024)
Animated line chart showing CPI inflation rate with crisis annotations.

Data source: Bureau of Labor Statistics / FRED (CPI-U, annual average % change).
Output: scripts/finance-demos/output/demo2_inflation_timeline.mp4
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

matplotlib.use("Agg")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Brand colors ---
NAVY = "#0A1628"
LIME = "#00FF88"
CRIMSON = "#CC0000"
OFF_WHITE = "#F5F5F0"
DARK_TEXT = "#8899AA"
GRID_COLOR = "#1A2A3D"

# --- US CPI Inflation Rate (annual %, BLS/FRED data) ---
years = list(range(1970, 2025))
inflation = [
    5.7, 4.4, 3.2, 6.2, 11.0, 9.1, 5.8, 6.5, 7.6, 11.3,  # 1970-1979
    13.5, 10.3, 6.2, 3.2, 4.3, 3.6, 1.9, 3.6, 4.1, 4.8,   # 1980-1989
    5.4, 4.2, 3.0, 3.0, 2.6, 2.8, 3.0, 2.3, 1.6, 2.2,     # 1990-1999
    3.4, 2.8, 1.6, 2.3, 2.7, 3.4, 3.2, 2.8, 3.8, -0.4,    # 2000-2009
    1.6, 3.2, 2.1, 1.5, 1.6, 0.1, 1.3, 2.1, 2.4, 1.8,     # 2010-2019
    1.2, 4.7, 8.0, 4.1, 2.9,                                 # 2020-2024
]

# --- Crisis annotations ---
annotations = [
    (1973, 11.0, "Oil Crisis", "above"),
    (1979, 11.3, "Energy Crisis", "above"),
    (1980, 13.5, "Volcker Peak\n13.5%", "above"),
    (2008, 3.8, "Financial Crisis", "above"),
    (2009, -0.4, "Deflation!", "below"),
    (2022, 8.0, "Post-COVID\n8.0%", "above"),
]

# --- Build animation ---
fig, ax = plt.subplots(figsize=(6.75, 12), dpi=160)
fig.set_facecolor(NAVY)
ax.set_facecolor(NAVY)

# Frames: draw line progressively, 3 frames per year + hold at end
FRAMES_PER_YEAR = 3
HOLD_FRAMES = 50
total_frames = len(years) * FRAMES_PER_YEAR + HOLD_FRAMES


def draw_frame(frame_idx):
    ax.clear()
    ax.set_facecolor(NAVY)

    # How many data points to show
    progress = min(frame_idx / FRAMES_PER_YEAR, len(years) - 1)
    n_points = int(progress) + 1
    frac = progress - int(progress)

    # Interpolated current point
    show_years = years[:n_points]
    show_inflation = inflation[:n_points]

    if frac > 0 and n_points < len(years):
        next_val = inflation[n_points]
        interp_val = show_inflation[-1] + frac * (next_val - show_inflation[-1])
        show_years = show_years + [years[n_points - 1] + frac]
        show_inflation = show_inflation + [interp_val]

    # Grid
    ax.set_axisbelow(True)
    for level in [-2, 0, 2, 4, 6, 8, 10, 12, 14]:
        ax.axhline(y=level, color=GRID_COLOR, linewidth=0.5, alpha=0.6)

    # Danger zone (above 5%)
    ax.axhspan(5, 15, alpha=0.08, color=CRIMSON)
    ax.axhline(y=5, color=CRIMSON, linewidth=1, alpha=0.4, linestyle="--")

    # Target zone (2%)
    ax.axhline(y=2, color=LIME, linewidth=1, alpha=0.3, linestyle="--")

    # Main line
    ax.plot(show_years, show_inflation, color=LIME, linewidth=3, alpha=0.95)

    # Fill under the line with gradient effect
    ax.fill_between(
        show_years, show_inflation, 0,
        alpha=0.15, color=LIME,
    )

    # Red fill for high-inflation periods
    high_y = [max(v, 5) for v in show_inflation]
    low_y = [5] * len(show_years)
    ax.fill_between(
        show_years, show_inflation, low_y,
        where=[v > 5 for v in show_inflation],
        alpha=0.2, color=CRIMSON,
        interpolate=True,
    )

    # Current value dot
    if len(show_years) > 0:
        ax.plot(show_years[-1], show_inflation[-1], "o",
                color=LIME, markersize=10, zorder=5)

        # Current rate readout
        current_year = int(round(show_years[-1]))
        current_rate = show_inflation[-1]
        rate_color = CRIMSON if current_rate > 5 else LIME
        ax.text(
            0.95, 0.22, f"{current_rate:.1f}%",
            transform=ax.transAxes,
            fontsize=56, fontweight="bold", color=rate_color,
            ha="right", va="bottom", alpha=0.9,
            fontfamily="sans-serif",
        )
        ax.text(
            0.95, 0.18, f"{current_year}",
            transform=ax.transAxes,
            fontsize=28, fontweight="bold", color=OFF_WHITE,
            ha="right", va="bottom", alpha=0.7,
            fontfamily="sans-serif",
        )

    # Annotations (show when timeline reaches them)
    for ann_year, ann_val, ann_text, ann_pos in annotations:
        if ann_year <= show_years[-1]:
            y_offset = 0.8 if ann_pos == "above" else -1.2
            ax.annotate(
                ann_text,
                xy=(ann_year, ann_val),
                xytext=(ann_year, ann_val + y_offset),
                fontsize=10, fontweight="bold",
                color=CRIMSON if ann_val > 5 else OFF_WHITE,
                ha="center", va="bottom" if ann_pos == "above" else "top",
                fontfamily="sans-serif",
                arrowprops=dict(arrowstyle="-", color=DARK_TEXT, lw=0.8),
            )

    # Title
    ax.text(
        0.5, 0.97, "US Inflation Rate",
        transform=ax.transAxes,
        fontsize=26, fontweight="bold", color=OFF_WHITE,
        ha="center", va="top", fontfamily="sans-serif",
    )
    ax.text(
        0.5, 0.94, "CPI Annual % Change · 1970–2024",
        transform=ax.transAxes,
        fontsize=13, color=DARK_TEXT,
        ha="center", va="top", fontfamily="sans-serif",
    )

    # Labels
    ax.text(
        0.03, 0.58, "DANGER ZONE", rotation=90,
        transform=ax.transAxes,
        fontsize=9, color=CRIMSON, alpha=0.5,
        ha="left", va="center", fontfamily="sans-serif",
    )
    ax.text(
        1975, 2.3, "2% Fed Target",
        fontsize=9, color=LIME, alpha=0.5,
        ha="left", va="bottom", fontfamily="sans-serif",
    )

    # Source
    ax.text(
        0.5, 0.01, "Finance Roast Central · Source: BLS / FRED",
        transform=ax.transAxes,
        fontsize=9, color=DARK_TEXT,
        ha="center", va="bottom", fontfamily="sans-serif",
    )

    ax.set_xlim(1968, 2026)
    ax.set_ylim(-2, 15)
    ax.tick_params(axis="x", colors=DARK_TEXT, labelsize=10)
    ax.tick_params(axis="y", colors=DARK_TEXT, labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.spines["left"].set_color(GRID_COLOR)

    fig.subplots_adjust(left=0.1, right=0.95, top=0.92, bottom=0.06)


print("Generating inflation timeline video...")
print(f"  Total frames: {total_frames}")
output_path = os.path.join(OUTPUT_DIR, "demo2_inflation_timeline.mp4")

anim = animation.FuncAnimation(fig, draw_frame, frames=total_frames, interval=60)
anim.save(output_path, writer="ffmpeg", fps=30, dpi=160)
plt.close("all")

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Done! Video saved: {output_path} ({size_mb:.1f} MB)")
