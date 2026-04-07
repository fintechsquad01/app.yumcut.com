#!/usr/bin/env python3
"""
Demo Video 3: Wealth Scale Comparison — "How Big Is a Billion?"
Animated stacked bar visualization showing wealth at incomprehensible scales.

Data source: Forbes Real-Time Billionaire List, BLS median wage data.
Output: scripts/finance-demos/output/demo3_wealth_scale.mp4
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
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
GOLD = "#FFD700"
ORANGE = "#FF6B35"

# --- Wealth comparison data ---
# Concept: show how absurdly large billionaire wealth is vs normal income
comparisons = [
    {
        "label": "US Median\nAnnual Salary",
        "amount": 60_000,
        "color": OFF_WHITE,
        "note": "$60K",
    },
    {
        "label": "Top 1%\nThreshold",
        "amount": 600_000,
        "color": LIME,
        "note": "$600K",
    },
    {
        "label": "A Really\nGood Year",
        "amount": 1_000_000,
        "color": "#4285F4",
        "note": "$1M",
    },
    {
        "label": "Median Home\nPrice (US)",
        "amount": 420_000,
        "color": ORANGE,
        "note": "$420K",
    },
    {
        "label": "1 Billion\nDollars",
        "amount": 1_000_000_000,
        "color": GOLD,
        "note": "$1B",
    },
    {
        "label": "Elon Musk\nNet Worth",
        "amount": 250_000_000_000,
        "color": CRIMSON,
        "note": "$250B",
    },
]

# --- Scene sequence (each scene reveals one comparison) ---
FRAMES_PER_SCENE = 45
HOLD_END = 60
total_scenes = len(comparisons)
total_frames = total_scenes * FRAMES_PER_SCENE + HOLD_END

fig, ax = plt.subplots(figsize=(6.75, 12), dpi=160)
fig.set_facecolor(NAVY)


def format_money(amount):
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.0f}B"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.0f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    return f"${amount:,.0f}"


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def draw_frame(frame_idx):
    ax.clear()
    ax.set_facecolor(NAVY)

    current_scene = min(frame_idx // FRAMES_PER_SCENE, total_scenes - 1)
    scene_frame = frame_idx % FRAMES_PER_SCENE
    anim_progress = ease_out_cubic(min(scene_frame / 25.0, 1.0))

    visible = comparisons[: current_scene + 1]

    # Determine scale — use log for the final scenes, linear for early
    max_amount = visible[-1]["amount"]

    # Title
    ax.text(
        0.5, 0.97, "How Big Is a Billion?",
        transform=ax.transAxes,
        fontsize=28, fontweight="bold", color=OFF_WHITE,
        ha="center", va="top", fontfamily="sans-serif",
    )
    ax.text(
        0.5, 0.935, "Wealth at incomprehensible scale",
        transform=ax.transAxes,
        fontsize=13, color=DARK_TEXT,
        ha="center", va="top", fontfamily="sans-serif",
    )

    # Draw comparisons as horizontal bars
    bar_y_start = 0.82
    bar_height = 0.065
    bar_gap = 0.025
    bar_left = 0.08
    bar_width = 0.84

    for i, comp in enumerate(visible):
        y_pos = bar_y_start - i * (bar_height + bar_gap)

        # Scale: width proportional to amount (log scale for sanity)
        if max_amount > 0:
            ratio = comp["amount"] / max_amount
        else:
            ratio = 0

        # Animate the current (newest) bar
        if i == current_scene:
            ratio *= anim_progress
            alpha = anim_progress
        else:
            alpha = 1.0

        # Bar background (track)
        ax.add_patch(mpatches.FancyBboxPatch(
            (bar_left, y_pos), bar_width, bar_height,
            boxstyle="round,pad=0.005",
            facecolor=NAVY, edgecolor=DARK_TEXT, linewidth=0.5, alpha=0.5,
            transform=ax.transAxes, clip_on=False,
        ))

        # Bar fill
        fill_width = max(ratio * bar_width, 0.003)
        ax.add_patch(mpatches.FancyBboxPatch(
            (bar_left, y_pos), fill_width, bar_height,
            boxstyle="round,pad=0.005",
            facecolor=comp["color"], edgecolor="none", alpha=alpha * 0.85,
            transform=ax.transAxes, clip_on=False,
        ))

        # Label (left side)
        ax.text(
            bar_left - 0.02, y_pos + bar_height / 2,
            comp["label"],
            transform=ax.transAxes,
            fontsize=10, color=OFF_WHITE, alpha=alpha,
            ha="right", va="center", fontfamily="sans-serif",
            fontweight="bold", linespacing=1.2,
        )

        # Amount (on bar or right side)
        display_amount = comp["amount"] * (anim_progress if i == current_scene else 1.0)
        ax.text(
            bar_left + fill_width + 0.015, y_pos + bar_height / 2,
            format_money(int(display_amount)),
            transform=ax.transAxes,
            fontsize=14, color=comp["color"], alpha=alpha,
            ha="left", va="center", fontfamily="sans-serif",
            fontweight="bold",
        )

    # "Mind-blow" stat at bottom when Elon is revealed
    if current_scene >= 4:  # After billion is shown
        billion = comparisons[4]["amount"]
        salary = comparisons[0]["amount"]
        years_to_earn = billion / salary
        stat_alpha = anim_progress if current_scene == 4 else 1.0

        ax.text(
            0.5, 0.18,
            f"At ${salary / 1000:.0f}K/year, earning $1B\nwould take {years_to_earn:,.0f} years",
            transform=ax.transAxes,
            fontsize=16, color=GOLD, alpha=stat_alpha * 0.95,
            ha="center", va="center", fontfamily="sans-serif",
            fontweight="bold", linespacing=1.4,
        )

    if current_scene >= 5:  # After Elon is shown
        elon = comparisons[5]["amount"]
        salary = comparisons[0]["amount"]
        years_elon = elon / salary
        stat_alpha = anim_progress if current_scene == 5 else 1.0

        ax.text(
            0.5, 0.10,
            f"Elon's wealth = {years_elon / 1_000_000:.1f} MILLION years\nof median US salary",
            transform=ax.transAxes,
            fontsize=18, color=CRIMSON, alpha=stat_alpha * 0.95,
            ha="center", va="center", fontfamily="sans-serif",
            fontweight="bold", linespacing=1.4,
        )

    # Source
    ax.text(
        0.5, 0.02, "Finance Roast Central · Forbes / BLS 2024",
        transform=ax.transAxes,
        fontsize=9, color=DARK_TEXT,
        ha="center", va="bottom", fontfamily="sans-serif",
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)


print("Generating wealth scale comparison video...")
print(f"  Total frames: {total_frames}")
output_path = os.path.join(OUTPUT_DIR, "demo3_wealth_scale.mp4")

anim = animation.FuncAnimation(fig, draw_frame, frames=total_frames, interval=67)
anim.save(output_path, writer="ffmpeg", fps=30, dpi=160)
plt.close("all")

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Done! Video saved: {output_path} ({size_mb:.1f} MB)")
