#!/usr/bin/env python3
"""
Demo Video 2: "54 Years of US Inflation in 50 Seconds"
Full narrative structure: Hook → Setup → 3 Data Beats → Punchline → Closer
9:16 vertical (1080×1920) · 50 seconds · 30fps

Data source: Bureau of Labor Statistics / FRED (CPI-U, annual average % change).
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

matplotlib.use("Agg")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Brand colors ──
NAVY = "#0A1628"
LIME = "#00FF88"
CRIMSON = "#CC0000"
OFF_WHITE = "#F5F5F0"
DARK_TEXT = "#8899AA"
GRID_COLOR = "#1A2A3D"
SEMI_BG = "#0D1F35"

# ── US CPI Inflation Rate (annual %, BLS/FRED) ──
years = list(range(1970, 2025))
inflation = [
    5.7, 4.4, 3.2, 6.2, 11.0, 9.1, 5.8, 6.5, 7.6, 11.3,   # 1970-79
    13.5, 10.3, 6.2, 3.2, 4.3, 3.6, 1.9, 3.6, 4.1, 4.8,    # 1980-89
    5.4, 4.2, 3.0, 3.0, 2.6, 2.8, 3.0, 2.3, 1.6, 2.2,      # 1990-99
    3.4, 2.8, 1.6, 2.3, 2.7, 3.4, 3.2, 2.8, 3.8, -0.4,     # 2000-09
    1.6, 3.2, 2.1, 1.5, 1.6, 0.1, 1.3, 2.1, 2.4, 1.8,      # 2010-19
    1.2, 4.7, 8.0, 4.1, 2.9,                                  # 2020-24
]

FPS = 30

# ── Scene timeline ──
HOOK_START, HOOK_END = 0, 90            # 0-3s
SETUP_START, SETUP_END = 90, 180        # 3-6s
DRAW1_START, DRAW1_END = 180, 480       # 6-16s   1970→1979
BEAT1_START, BEAT1_END = 480, 600       # 16-20s  Volcker peak hold
DRAW2_START, DRAW2_END = 600, 840       # 20-28s  1980→2007
BEAT2_START, BEAT2_END = 840, 930       # 28-31s  GFC deflation hold
DRAW3_START, DRAW3_END = 930, 1050      # 31-35s  2010→2019
BEAT3_START, BEAT3_END = 1050, 1200     # 35-40s  COVID spike hold
PUNCH_START, PUNCH_END = 1200, 1380     # 40-46s  punchline
CLOSE_START, CLOSE_END = 1380, 1500     # 46-50s  closer
TOTAL_FRAMES = CLOSE_END

# Map frames to data progression (year index into the arrays)
DRAW_SECTIONS = [
    (DRAW1_START, DRAW1_END, 0, 10),    # indices 0-9 → 1970-1979
    (DRAW2_START, DRAW2_END, 10, 38),   # indices 10-37 → 1980-2007
    (DRAW3_START, DRAW3_END, 38, 50),   # indices 38-49 → 2008-2019
]
BEAT_INDICES = {BEAT1_START: 10, BEAT2_START: 39, BEAT3_START: 52}  # index to hold at


def get_data_index(f):
    """Map frame to how many data points to show."""
    for ds, de, is_, ie in DRAW_SECTIONS:
        if ds <= f < de:
            t = (f - ds) / max(de - ds - 1, 1)
            return is_ + t * (ie - is_)
    for bs, be in [(BEAT1_START, BEAT1_END), (BEAT2_START, BEAT2_END), (BEAT3_START, BEAT3_END)]:
        if bs <= f < be:
            return BEAT_INDICES[bs]
    if f >= BEAT3_END:
        return len(years) - 1
    return 0


def ease_out(t):
    return 1 - (1 - min(max(t, 0), 1)) ** 3


def draw_text_box(ax, text, x, y, fontsize=17, color=OFF_WHITE, bg_alpha=0.75):
    ax.text(
        x, y, text, transform=ax.transAxes,
        fontsize=fontsize, color=color, ha="center", va="center",
        fontweight="bold", fontfamily="sans-serif", linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=SEMI_BG, edgecolor="none", alpha=bg_alpha),
    )


def draw_chart(ax, data_idx, show_full=False):
    """Draw the inflation chart up to data_idx (can be fractional)."""
    n = int(data_idx) + 1
    n = min(n, len(years))
    frac = data_idx - int(data_idx)

    show_years = years[:n]
    show_vals = inflation[:n]

    if frac > 0 and n < len(years):
        interp_val = show_vals[-1] + frac * (inflation[n] - show_vals[-1])
        show_years = show_years + [years[n - 1] + frac]
        show_vals = show_vals + [interp_val]

    if show_full:
        show_years = years
        show_vals = inflation

    # Grid
    for level in [-2, 0, 2, 4, 6, 8, 10, 12, 14]:
        ax.axhline(y=level, color=GRID_COLOR, linewidth=0.5, alpha=0.5)

    # Danger zone
    ax.axhspan(5, 16, alpha=0.06, color=CRIMSON)
    ax.axhline(y=5, color=CRIMSON, linewidth=1, alpha=0.35, linestyle="--")

    # Target zone
    ax.axhline(y=2, color=LIME, linewidth=1, alpha=0.25, linestyle="--")
    ax.text(1972, 2.3, "2% Fed Target", fontsize=8, color=LIME, alpha=0.5, fontfamily="sans-serif")

    # Main line
    ax.plot(show_years, show_vals, color=LIME, linewidth=3, alpha=0.95)

    # Fill under
    ax.fill_between(show_years, show_vals, 0, alpha=0.12, color=LIME)

    # Red fill above 5%
    ax.fill_between(
        show_years, show_vals, [5] * len(show_years),
        where=[v > 5 for v in show_vals],
        alpha=0.18, color=CRIMSON, interpolate=True,
    )

    # Current dot
    if len(show_years) > 0:
        ax.plot(show_years[-1], show_vals[-1], "o", color=LIME, markersize=9, zorder=5)

        # Rate readout
        rate = show_vals[-1]
        rate_color = CRIMSON if rate > 5 else LIME
        ax.text(0.93, 0.20, f"{rate:.1f}%", transform=ax.transAxes,
                fontsize=48, fontweight="bold", color=rate_color,
                ha="right", va="bottom", alpha=0.9, fontfamily="sans-serif")
        ax.text(0.93, 0.15, f"{int(round(show_years[-1]))}", transform=ax.transAxes,
                fontsize=24, fontweight="bold", color=OFF_WHITE,
                ha="right", va="bottom", alpha=0.7, fontfamily="sans-serif")

    # Title
    ax.text(0.5, 0.97, "US Inflation Rate", transform=ax.transAxes,
            fontsize=22, fontweight="bold", color=OFF_WHITE,
            ha="center", va="top", fontfamily="sans-serif")
    ax.text(0.5, 0.935, "CPI Annual % Change · 1970–2024", transform=ax.transAxes,
            fontsize=11, color=DARK_TEXT, ha="center", va="top", fontfamily="sans-serif")

    # Source
    ax.text(0.5, 0.02, "Finance Roast Central · Source: BLS / FRED", transform=ax.transAxes,
            fontsize=9, color=DARK_TEXT, ha="center", va="bottom", fontfamily="sans-serif")

    ax.set_xlim(1968, 2026)
    ax.set_ylim(-2, 16)
    ax.tick_params(axis="x", colors=DARK_TEXT, labelsize=9)
    ax.tick_params(axis="y", colors=DARK_TEXT, labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.spines["left"].set_color(GRID_COLOR)


fig, ax = plt.subplots(figsize=(6.75, 12), dpi=160)
fig.set_facecolor(NAVY)


def draw_frame(f):
    ax.clear()
    ax.set_facecolor(NAVY)
    fig.subplots_adjust(left=0.1, right=0.95, top=0.92, bottom=0.06)

    # ── HOOK ──
    if f < HOOK_END:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        t = ease_out((f - HOOK_START) / 30)
        ax.text(0.5, 0.58,
            'The Fed says 2% inflation\nis "normal."',
            transform=ax.transAxes, fontsize=28, color=OFF_WHITE,
            ha="center", va="center", fontweight="bold",
            fontfamily="sans-serif", alpha=t, linespacing=1.6)
        if f > 35:
            t2 = ease_out((f - 35) / 25)
            ax.text(0.5, 0.38,
                "Here's what ACTUALLY happened.",
                transform=ax.transAxes, fontsize=22, color=LIME,
                ha="center", va="center", fontweight="bold",
                fontfamily="sans-serif", alpha=t2)
        return

    # ── SETUP ──
    if f < SETUP_END:
        draw_chart(ax, 0)
        draw_text_box(ax, "54 years. One chart.\nLet's see.", 0.5, 0.55, fontsize=17)
        return

    # ── DRAWING + BEATS ──
    if f < PUNCH_START:
        idx = get_data_index(f)
        draw_chart(ax, idx)

        # Draw 1: 1970s commentary
        if DRAW1_START + 100 < f < DRAW1_START + 220:
            draw_text_box(ax, "1973: Oil Crisis.\nInflation doubled overnight.", 0.5, 0.55, fontsize=15)

        # Beat 1: Volcker peak
        if BEAT1_START <= f < BEAT1_END:
            draw_text_box(ax,
                "1980: Inflation hit 13.5%\nVolcker raised rates to 20%\nto kill it.", 0.5, 0.55,
                fontsize=17, color=CRIMSON)

        # Draw 2: calm era commentary
        if DRAW2_START + 120 < f < DRAW2_START + 200:
            draw_text_box(ax, "25 years of calm.\nPeople forgot what\n10% feels like.", 0.5, 0.55, fontsize=15)

        # Beat 2: GFC deflation
        if BEAT2_START <= f < BEAT2_END:
            draw_text_box(ax,
                "2009: Prices actually FELL.\nDeflation. The Fed panicked.", 0.5, 0.55,
                fontsize=17, color=OFF_WHITE)

        # Draw 3: "everything is fine"
        if DRAW3_START + 30 < f < DRAW3_START + 90:
            draw_text_box(ax, 'A decade of\n"everything is fine."', 0.5, 0.55, fontsize=16)

        # Beat 3: COVID spike
        if BEAT3_START <= f < BEAT3_END:
            draw_text_box(ax,
                "2022: 8.0%\nYour grocery bill\nwasn't lying.", 0.5, 0.55,
                fontsize=20, color=CRIMSON)
        return

    # ── PUNCHLINE ──
    if f < PUNCH_END:
        draw_chart(ax, len(years) - 1, show_full=True)
        t = ease_out((f - PUNCH_START) / 30)
        draw_text_box(ax,
            "From 13.5% to 0% to 8%\n— all in one lifetime.\n\nThe 'normal' never existed.",
            0.5, 0.55, fontsize=18, color=LIME)
        return

    # ── CLOSER ──
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    t = ease_out((f - CLOSE_START) / 20)
    ax.text(0.5, 0.55, "FINANCE ROAST CENTRAL", transform=ax.transAxes,
            fontsize=28, color=LIME, ha="center", va="center",
            fontweight="bold", fontfamily="sans-serif", alpha=t)
    ax.text(0.5, 0.42, "Follow for more finance roasts", transform=ax.transAxes,
            fontsize=16, color=OFF_WHITE, ha="center", va="center",
            fontfamily="sans-serif", alpha=t * 0.85)


print("Generating Demo 2: Inflation Timeline (50s)...")
print(f"  Total frames: {TOTAL_FRAMES} at {FPS}fps = {TOTAL_FRAMES / FPS:.1f}s")
output_path = os.path.join(OUTPUT_DIR, "demo2_inflation_timeline.mp4")

anim = animation.FuncAnimation(fig, draw_frame, frames=TOTAL_FRAMES, interval=1000 // FPS)
anim.save(output_path, writer="ffmpeg", fps=FPS, dpi=160)
plt.close("all")

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Done! {output_path} ({size_mb:.1f} MB, {TOTAL_FRAMES / FPS:.1f}s)")
