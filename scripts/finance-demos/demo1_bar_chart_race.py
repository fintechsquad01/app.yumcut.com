#!/usr/bin/env python3
"""
Demo Video 1: Bar Chart Race — Top 10 Companies by Market Cap (2000–2024)
Generates a 9:16 vertical MP4 suitable for YouTube Shorts.

Data source: Manually curated from publicly available market cap records
(CompaniesMarketCap.com, Wikipedia, Visual Capitalist).
Output: scripts/finance-demos/output/demo1_market_cap_race.mp4
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

matplotlib.use("Agg")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Brand colors (Finance Roast Central) ---
NAVY = "#0A1628"
LIME = "#00FF88"
CRIMSON = "#CC0000"
OFF_WHITE = "#F5F5F0"
DARK_TEXT = "#8899AA"

# --- Curated market cap data (billions USD, approximate year-end values) ---
data = {
    "Year": [2000, 2004, 2008, 2012, 2016, 2018, 2020, 2022, 2024],
    "Microsoft":    [510, 300, 173, 224, 483,  780, 1680, 1790, 3100],
    "Apple":        [ 15,  18,  76, 500, 617,  746, 2250, 2070, 3700],
    "Amazon":       [ 17,  18,  23, 114, 356,  737, 1630,  857, 2350],
    "Google":       [  0,  52,  97, 250, 539,  724, 1190, 1150, 2350],
    "Meta":         [  0,   0,   0,  62, 332,  374,  778,  320, 1580],
    "Saudi Aramco": [  0,   0,   0,   0,   0,    0, 2000, 1900, 1800],
    "Nvidia":       [  3,   4,   5,   7,  57,   81,  323,  360, 3400],
    "Berkshire":    [110, 130, 135, 210, 401,  497,  545,  680,  980],
    "Tesla":        [  0,   0,   0,   4,  34,   53,  670,  389, 1300],
    "JPMorgan":     [120,  88,  67, 144, 240,  320,  380,  390,  680],
}

df = pd.DataFrame(data).set_index("Year")
years_full = np.arange(2000, 2025, 1)
df_full = df.reindex(years_full).interpolate(method="linear").fillna(0)

# Interpolate at sub-year level for smooth animation
STEPS = 6  # frames between each year
total_frames = (len(years_full) - 1) * STEPS + 1
fine_index = np.linspace(2000, 2024, total_frames)
df_fine = pd.DataFrame(index=fine_index, columns=df_full.columns, dtype=float)
for col in df_full.columns:
    df_fine[col] = np.interp(fine_index, years_full, df_full[col].values)

COMPANY_COLORS = {
    "Microsoft":    "#00A4EF",
    "Apple":        "#A2AAAD",
    "Amazon":       "#FF9900",
    "Google":       "#4285F4",
    "Meta":         "#0082FB",
    "Saudi Aramco": "#00843D",
    "Nvidia":       LIME,
    "Berkshire":    "#6F263D",
    "Tesla":        CRIMSON,
    "JPMorgan":     "#003087",
}

# --- Build animation ---
fig, ax = plt.subplots(figsize=(6.75, 12), dpi=160)
fig.set_facecolor(NAVY)
ax.set_facecolor(NAVY)

N_BARS = 10


def draw_frame(frame_idx):
    ax.clear()
    ax.set_facecolor(NAVY)

    row = df_fine.iloc[frame_idx]
    sorted_row = row.sort_values(ascending=True)
    top = sorted_row.tail(N_BARS)

    companies = top.index.tolist()
    values = top.values
    colors = [COMPANY_COLORS.get(c, OFF_WHITE) for c in companies]

    bars = ax.barh(range(len(companies)), values, color=colors, height=0.75, alpha=0.92)

    # Company labels on bars
    for i, (company, val) in enumerate(zip(companies, values)):
        label_text = f"  {company}  ${val:,.0f}B"
        ax.text(
            val + 20, i, label_text,
            va="center", ha="left",
            fontsize=12, fontweight="bold", color=OFF_WHITE,
            fontfamily="sans-serif",
        )

    # Year label (big, bottom-right)
    year_val = fine_index[frame_idx]
    ax.text(
        0.95, 0.08, f"{int(round(year_val))}",
        transform=ax.transAxes,
        fontsize=64, fontweight="bold", color=LIME,
        ha="right", va="bottom", alpha=0.85,
        fontfamily="sans-serif",
    )

    # Title
    ax.text(
        0.5, 0.97, "Top Companies by Market Cap",
        transform=ax.transAxes,
        fontsize=22, fontweight="bold", color=OFF_WHITE,
        ha="center", va="top",
        fontfamily="sans-serif",
    )

    # Subtitle
    ax.text(
        0.5, 0.94, "Billions USD · 2000–2024",
        transform=ax.transAxes,
        fontsize=13, color=DARK_TEXT,
        ha="center", va="top",
        fontfamily="sans-serif",
    )

    # Source label
    ax.text(
        0.5, 0.02, "Finance Roast Central · Data: Public market records",
        transform=ax.transAxes,
        fontsize=9, color=DARK_TEXT,
        ha="center", va="bottom",
        fontfamily="sans-serif",
    )

    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    max_val = max(values) if len(values) > 0 else 100
    ax.set_xlim(0, max_val * 1.55)

    fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.06)


print("Generating bar chart race video...")
print(f"  Total frames: {total_frames}")
output_path = os.path.join(OUTPUT_DIR, "demo1_market_cap_race.mp4")

anim = animation.FuncAnimation(fig, draw_frame, frames=total_frames, interval=80)
anim.save(output_path, writer="ffmpeg", fps=25, dpi=160)
plt.close("all")

# Check file
size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Done! Video saved: {output_path} ({size_mb:.1f} MB)")
