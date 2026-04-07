#!/usr/bin/env python3
"""
Demo Video 1: Bar Chart Race — "24 Years of Tech Dominance in 50 Seconds"
Full narrative structure: Hook → Setup → 3 Data Beats → Punchline → Closer
9:16 vertical (1080×1920) · 50 seconds · 30fps

Data source: Curated from CompaniesMarketCap.com, Wikipedia, Visual Capitalist.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
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
SEMI_BG = "#0D1F35"

COMPANY_COLORS = {
    "Microsoft": "#00A4EF", "Apple": "#A2AAAD", "Amazon": "#FF9900",
    "Google": "#4285F4", "Meta": "#0082FB", "Saudi Aramco": "#00843D",
    "Nvidia": LIME, "Berkshire": "#6F263D", "Tesla": CRIMSON, "JPMorgan": "#003087",
}

# ── Market cap data (billions USD) ──
data = {
    "Year": [2000, 2004, 2008, 2012, 2016, 2018, 2020, 2022, 2024],
    "Microsoft": [510, 300, 173, 224, 483, 780, 1680, 1790, 3100],
    "Apple": [15, 18, 76, 500, 617, 746, 2250, 2070, 3700],
    "Amazon": [17, 18, 23, 114, 356, 737, 1630, 857, 2350],
    "Google": [0, 52, 97, 250, 539, 724, 1190, 1150, 2350],
    "Meta": [0, 0, 0, 62, 332, 374, 778, 320, 1580],
    "Saudi Aramco": [0, 0, 0, 0, 0, 0, 2000, 1900, 1800],
    "Nvidia": [3, 4, 5, 7, 57, 81, 323, 360, 3400],
    "Berkshire": [110, 130, 135, 210, 401, 497, 545, 680, 980],
    "Tesla": [0, 0, 0, 4, 34, 53, 670, 389, 1300],
    "JPMorgan": [120, 88, 67, 144, 240, 320, 380, 390, 680],
}
df = pd.DataFrame(data).set_index("Year")
years_full = np.arange(2000, 2025, 1)
df_full = df.reindex(years_full).interpolate(method="linear").fillna(0)

FPS = 30
N_BARS = 10

# ── Scene timeline (frame ranges) ──
HOOK_START, HOOK_END = 0, 90          # 0-3s
SETUP_START, SETUP_END = 90, 180      # 3-6s
RACE1_START, RACE1_END = 180, 480     # 6-16s   2000→2011
BEAT1_START, BEAT1_END = 480, 540     # 16-18s  pause at 2012
RACE2_START, RACE2_END = 540, 780     # 18-26s  2012→2019
BEAT2_START, BEAT2_END = 780, 870     # 26-29s  pause at 2020
RACE3_START, RACE3_END = 870, 1140    # 29-38s  2020→2024
BEAT3_START, BEAT3_END = 1140, 1260   # 38-42s  pause at 2024
PUNCH_START, PUNCH_END = 1260, 1410   # 42-47s  punchline
CLOSE_START, CLOSE_END = 1410, 1500   # 47-50s  closer
TOTAL_FRAMES = CLOSE_END

# Map frame ranges to year ranges for race sections
RACE_SECTIONS = [
    (RACE1_START, RACE1_END, 2000, 2012),
    (RACE2_START, RACE2_END, 2012, 2020),
    (RACE3_START, RACE3_END, 2020, 2024),
]
BEAT_YEARS = {BEAT1_START: 2012, BEAT2_START: 2020, BEAT3_START: 2024}


def get_year_for_frame(f):
    """Map a frame index to the current data year."""
    for rs, re, ys, ye in RACE_SECTIONS:
        if rs <= f < re:
            t = (f - rs) / max(re - rs - 1, 1)
            return ys + t * (ye - ys)
    # During beats, hold on the beat year
    for bs, be in [(BEAT1_START, BEAT1_END), (BEAT2_START, BEAT2_END), (BEAT3_START, BEAT3_END)]:
        if bs <= f < be:
            return BEAT_YEARS[bs]
    if f < RACE1_START:
        return 2000
    return 2024


def get_data_at_year(year):
    """Interpolate all company values at a fractional year."""
    vals = {}
    for col in df_full.columns:
        vals[col] = float(np.interp(year, years_full, df_full[col].values))
    return vals


def ease_out(t):
    return 1 - (1 - min(max(t, 0), 1)) ** 3


def draw_text_box(ax, text, x, y, fontsize=18, color=OFF_WHITE, bg_alpha=0.7, ha="center", va="center", bold=True):
    """Draw text with a semi-transparent background box."""
    ax.text(
        x, y, text, transform=ax.transAxes,
        fontsize=fontsize, color=color, ha=ha, va=va,
        fontweight="bold" if bold else "normal", fontfamily="sans-serif",
        linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=SEMI_BG, edgecolor="none", alpha=bg_alpha),
    )


def draw_bars(ax, year_val, max_override=None):
    """Draw the ranked bar chart at a given year value."""
    vals = get_data_at_year(year_val)
    sorted_items = sorted(vals.items(), key=lambda x: x[1])
    top = sorted_items[-N_BARS:]
    companies = [x[0] for x in top]
    values = [x[1] for x in top]
    colors = [COMPANY_COLORS.get(c, OFF_WHITE) for c in companies]

    ax.barh(range(len(companies)), values, color=colors, height=0.75, alpha=0.92)

    for i, (company, val) in enumerate(zip(companies, values)):
        if val > 0:
            ax.text(
                val + 20, i, f"  {company}  ${val:,.0f}B",
                va="center", ha="left", fontsize=11, fontweight="bold",
                color=OFF_WHITE, fontfamily="sans-serif",
            )

    # Year label
    ax.text(
        0.93, 0.12, f"{int(round(year_val))}",
        transform=ax.transAxes, fontsize=52, fontweight="bold",
        color=LIME, ha="right", va="bottom", alpha=0.85, fontfamily="sans-serif",
    )

    # Title bar
    ax.text(
        0.5, 0.97, "Top Companies by Market Cap",
        transform=ax.transAxes, fontsize=20, fontweight="bold",
        color=OFF_WHITE, ha="center", va="top", fontfamily="sans-serif",
    )
    ax.text(
        0.5, 0.935, "Billions USD",
        transform=ax.transAxes, fontsize=12, color=DARK_TEXT,
        ha="center", va="top", fontfamily="sans-serif",
    )

    # Source
    ax.text(
        0.5, 0.02, "Finance Roast Central",
        transform=ax.transAxes, fontsize=9, color=DARK_TEXT,
        ha="center", va="bottom", fontfamily="sans-serif",
    )

    max_val = max(values) if values else 100
    ax.set_xlim(0, (max_override or max_val) * 1.55)
    ax.set_yticks([])
    ax.set_xticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


# ── Build animation ──
fig, ax = plt.subplots(figsize=(6.75, 12), dpi=160)
fig.set_facecolor(NAVY)


def draw_frame(f):
    ax.clear()
    ax.set_facecolor(NAVY)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.06)

    # ── HOOK (0-3s): Text-only question ──
    if f < HOOK_END:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        t = ease_out((f - HOOK_START) / 30)
        ax.text(
            0.5, 0.55,
            "Which company went from\n$3B to $3.4 TRILLION?",
            transform=ax.transAxes, fontsize=32, color=LIME,
            ha="center", va="center", fontweight="bold",
            fontfamily="sans-serif", alpha=t, linespacing=1.6,
        )
        ax.text(
            0.5, 0.38, "In just 24 years.",
            transform=ax.transAxes, fontsize=18, color=OFF_WHITE,
            ha="center", va="center", alpha=t * 0.8, fontfamily="sans-serif",
        )
        return

    # ── SETUP (3-6s): Intro text + chart appears ──
    if f < SETUP_END:
        t = ease_out((f - SETUP_START) / 40)
        draw_bars(ax, 2000)
        draw_text_box(ax,
            "24 years of market cap rankings.\nWatch who rises — and who falls.",
            0.5, 0.55, fontsize=17, color=OFF_WHITE)
        return

    # ── RACE SECTIONS + BEATS ──
    if f < PUNCH_START:
        year = get_year_for_frame(f)
        draw_bars(ax, year)

        # Overlay text during race sections
        yr_int = int(round(year))

        # Race 1 commentary
        if RACE1_START + 120 < f < RACE1_START + 240 and f < RACE1_END:
            draw_text_box(ax, "Microsoft was king.\nNobody else was close.", 0.5, 0.55, fontsize=16)

        # Beat 1: iPhone era
        if BEAT1_START <= f < BEAT1_END:
            t = ease_out((f - BEAT1_START) / 20)
            draw_text_box(ax,
                "Apple: $15B → $500B\nThe iPhone changed everything.",
                0.5, 0.55, fontsize=17, color=LIME)

        # Race 2 commentary
        if RACE2_START + 80 < f < RACE2_START + 180 and f < RACE2_END:
            draw_text_box(ax, "Amazon + Google\nquietly creeping up.", 0.5, 0.55, fontsize=16)

        # Beat 2: COVID
        if BEAT2_START <= f < BEAT2_END:
            draw_text_box(ax,
                "COVID hit. Tech exploded.\nSaudi Aramco entered at $2T.",
                0.5, 0.55, fontsize=17, color=CRIMSON)

        # Race 3 commentary
        if RACE3_START + 100 < f < RACE3_START + 200 and f < RACE3_END:
            draw_text_box(ax, "Nvidia is coming...", 0.5, 0.55, fontsize=20, color=LIME)

        # Beat 3: Nvidia at top
        if BEAT3_START <= f < BEAT3_END:
            draw_text_box(ax,
                "Nvidia: $3B → $3,400B\nA 1,133x return.",
                0.5, 0.55, fontsize=20, color=LIME)
        return

    # ── PUNCHLINE (42-47s) ──
    if f < PUNCH_END:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
        t = ease_out((f - PUNCH_START) / 30)

        ax.text(
            0.5, 0.62,
            "$1,000 invested in\nNvidia in 2000...",
            transform=ax.transAxes, fontsize=24, color=OFF_WHITE,
            ha="center", va="center", fontweight="bold",
            fontfamily="sans-serif", alpha=t, linespacing=1.5,
        )

        if f > PUNCH_START + 45:
            t2 = ease_out((f - PUNCH_START - 45) / 25)
            ax.text(
                0.5, 0.40,
                "= $1.1 MILLION today",
                transform=ax.transAxes, fontsize=34, color=LIME,
                ha="center", va="center", fontweight="bold",
                fontfamily="sans-serif", alpha=t2, linespacing=1.5,
            )

        if f > PUNCH_START + 90:
            ax.text(
                0.5, 0.26,
                "Meanwhile, your savings account\nearned 0.01%.",
                transform=ax.transAxes, fontsize=16, color=CRIMSON,
                ha="center", va="center", fontweight="bold",
                fontfamily="sans-serif", alpha=0.9, linespacing=1.5,
            )
        return

    # ── CLOSER (47-50s) ──
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    t = ease_out((f - CLOSE_START) / 20)

    ax.text(
        0.5, 0.55, "FINANCE ROAST CENTRAL",
        transform=ax.transAxes, fontsize=28, color=LIME,
        ha="center", va="center", fontweight="bold",
        fontfamily="sans-serif", alpha=t,
    )
    ax.text(
        0.5, 0.42, "Follow for more finance roasts",
        transform=ax.transAxes, fontsize=16, color=OFF_WHITE,
        ha="center", va="center", fontfamily="sans-serif", alpha=t * 0.85,
    )


print("Generating Demo 1: Bar Chart Race (50s)...")
print(f"  Total frames: {TOTAL_FRAMES} at {FPS}fps = {TOTAL_FRAMES / FPS:.1f}s")
output_path = os.path.join(OUTPUT_DIR, "demo1_market_cap_race.mp4")

anim = animation.FuncAnimation(fig, draw_frame, frames=TOTAL_FRAMES, interval=1000 // FPS)
anim.save(output_path, writer="ffmpeg", fps=FPS, dpi=160)
plt.close("all")

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Done! {output_path} ({size_mb:.1f} MB, {TOTAL_FRAMES / FPS:.1f}s)")
