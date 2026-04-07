#!/usr/bin/env python3
"""
Demo Video 3: "How Long to Earn $1 Billion? (You'll Hate This)"
Full narrative structure: Hook → Setup → 3 Reveals → 3 Beats → Punchline → Closer
9:16 vertical (1080×1920) · 55 seconds · 30fps

Data source: Forbes Real-Time Billionaire List, BLS median wage data.
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

# ── Brand colors ──
NAVY = "#0A1628"
LIME = "#00FF88"
CRIMSON = "#CC0000"
OFF_WHITE = "#F5F5F0"
DARK_TEXT = "#8899AA"
SEMI_BG = "#0D1F35"
GOLD = "#FFD700"
ORANGE = "#FF6B35"

FPS = 30

# ── Scene timeline ──
HOOK_START, HOOK_END = 0, 90          # 0-3s
SETUP_START, SETUP_END = 90, 180      # 3-6s
REV1_START, REV1_END = 180, 360       # 6-12s   median salary
REV2_START, REV2_END = 360, 540       # 12-18s  top 1%
REV3_START, REV3_END = 540, 720       # 18-24s  millionaire
BEAT1_START, BEAT1_END = 720, 960     # 24-32s  BILLION reveal
BEAT2_START, BEAT2_END = 960, 1140    # 32-38s  $1/second
BEAT3_START, BEAT3_END = 1140, 1380   # 38-46s  Elon
PUNCH_START, PUNCH_END = 1380, 1560   # 46-52s  dinosaurs
CLOSE_START, CLOSE_END = 1560, 1650   # 52-55s  closer
TOTAL_FRAMES = CLOSE_END

# ── Data ──
MEDIAN_SALARY = 60_000
TOP_1_PCT = 600_000
MILLION = 1_000_000
BILLION = 1_000_000_000
ELON = 250_000_000_000


def ease_out(t):
    return 1 - (1 - min(max(t, 0), 1)) ** 3


def ease_out_expo(t):
    t = min(max(t, 0), 1)
    return 1 - 2 ** (-10 * t) if t > 0 else 0


def format_money(amount):
    if amount >= 1e12:
        return f"${amount / 1e12:.0f}T"
    if amount >= 1e9:
        return f"${amount / 1e9:.0f}B"
    if amount >= 1e6:
        return f"${amount / 1e6:.0f}M"
    if amount >= 1e3:
        return f"${amount / 1e3:.0f}K"
    return f"${amount:,.0f}"


def draw_text_centered(ax, text, y, fontsize=20, color=OFF_WHITE, alpha=1.0, bold=True):
    ax.text(0.5, y, text, transform=ax.transAxes,
            fontsize=fontsize, color=color, ha="center", va="center",
            fontweight="bold" if bold else "normal", fontfamily="sans-serif",
            alpha=alpha, linespacing=1.6)


def draw_bar_row(ax, y_pos, label, amount, max_amount, color, alpha=1.0, animate_t=1.0):
    """Draw one labeled horizontal bar at a normalized y position."""
    bar_left = 0.05
    bar_width = 0.9
    bar_h = 0.045

    # Track background
    ax.add_patch(mpatches.FancyBboxPatch(
        (bar_left, y_pos), bar_width, bar_h,
        boxstyle="round,pad=0.004", facecolor=NAVY, edgecolor=DARK_TEXT,
        linewidth=0.5, alpha=alpha * 0.4, transform=ax.transAxes, clip_on=False))

    # Filled portion
    ratio = min(amount / max_amount, 1.0) if max_amount > 0 else 0
    fill_w = max(ratio * bar_width * animate_t, 0.004)
    ax.add_patch(mpatches.FancyBboxPatch(
        (bar_left, y_pos), fill_w, bar_h,
        boxstyle="round,pad=0.004", facecolor=color, edgecolor="none",
        alpha=alpha * 0.85, transform=ax.transAxes, clip_on=False))

    # Label
    display_amount = int(amount * animate_t)
    ax.text(bar_left - 0.01, y_pos + bar_h / 2, label, transform=ax.transAxes,
            fontsize=9, color=OFF_WHITE, alpha=alpha, ha="right", va="center",
            fontweight="bold", fontfamily="sans-serif", linespacing=1.2)
    ax.text(bar_left + fill_w + 0.01, y_pos + bar_h / 2, format_money(display_amount),
            transform=ax.transAxes, fontsize=12, color=color, alpha=alpha,
            ha="left", va="center", fontweight="bold", fontfamily="sans-serif")


fig, ax = plt.subplots(figsize=(6.75, 12), dpi=160)
fig.set_facecolor(NAVY)


def draw_frame(f):
    ax.clear()
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

    # Title (persistent on bar scenes)
    def draw_title():
        ax.text(0.5, 0.96, "How Big Is a Billion?", transform=ax.transAxes,
                fontsize=26, fontweight="bold", color=OFF_WHITE,
                ha="center", va="top", fontfamily="sans-serif")
        ax.text(0.5, 0.02, "Finance Roast Central · Forbes / BLS 2024",
                transform=ax.transAxes, fontsize=9, color=DARK_TEXT,
                ha="center", va="bottom", fontfamily="sans-serif")

    # ── HOOK ──
    if f < HOOK_END:
        t = ease_out((f - HOOK_START) / 30)
        draw_text_centered(ax, "How long would it take\nYOU to earn $1 billion?", 0.55,
                           fontsize=30, color=LIME, alpha=t)
        if f > 50:
            t2 = ease_out((f - 50) / 20)
            draw_text_centered(ax, "Let's find out.", 0.37, fontsize=18, color=OFF_WHITE, alpha=t2)
        return

    # ── SETUP ──
    if f < SETUP_END:
        draw_title()
        t = ease_out((f - SETUP_START) / 30)
        draw_text_centered(ax, "Let's put wealth\nin perspective.", 0.55,
                           fontsize=22, color=OFF_WHITE, alpha=t)
        return

    # ── REVEAL 1: Median salary ──
    if f < REV1_END:
        draw_title()
        t = ease_out((f - REV1_START) / 30)
        # Scale relative to $1M for these first reveals
        draw_bar_row(ax, 0.80, "US Median\nSalary", MEDIAN_SALARY, MILLION, OFF_WHITE, alpha=t, animate_t=t)
        if f > REV1_START + 60:
            draw_text_centered(ax, "Most Americans earn this.\n$60,000 per year.", 0.55,
                               fontsize=17, color=OFF_WHITE, alpha=0.9)
        return

    # ── REVEAL 2: Top 1% ──
    if f < REV2_END:
        draw_title()
        t = ease_out((f - REV2_START) / 30)
        draw_bar_row(ax, 0.80, "US Median\nSalary", MEDIAN_SALARY, MILLION, OFF_WHITE)
        draw_bar_row(ax, 0.72, "Top 1%\nThreshold", TOP_1_PCT, MILLION, LIME, alpha=t, animate_t=t)
        if f > REV2_START + 60:
            draw_text_centered(ax, '10x the median.\nYou\'re "rich" now.', 0.50,
                               fontsize=17, color=LIME, alpha=0.9)
        return

    # ── REVEAL 3: Millionaire ──
    if f < REV3_END:
        draw_title()
        t = ease_out((f - REV3_START) / 30)
        draw_bar_row(ax, 0.80, "US Median\nSalary", MEDIAN_SALARY, MILLION, OFF_WHITE)
        draw_bar_row(ax, 0.72, "Top 1%\nThreshold", TOP_1_PCT, MILLION, LIME)
        draw_bar_row(ax, 0.64, "Millionaire", MILLION, MILLION, "#4285F4", alpha=t, animate_t=t)
        if f > REV3_START + 60:
            draw_text_centered(ax, "17 years of median salary.\nNot bad.", 0.45,
                               fontsize=17, color="#4285F4", alpha=0.9)
        return

    # ── BEAT 1: BILLION ──
    if f < BEAT1_END:
        draw_title()
        t = ease_out_expo((f - BEAT1_START) / 45)

        # Previous bars shrink to nothing (rescale to $1B)
        draw_bar_row(ax, 0.80, "Median", MEDIAN_SALARY, BILLION, OFF_WHITE, alpha=0.5)
        draw_bar_row(ax, 0.72, "Top 1%", TOP_1_PCT, BILLION, LIME, alpha=0.5)
        draw_bar_row(ax, 0.64, "Millionaire", MILLION, BILLION, "#4285F4", alpha=0.5)

        # The billion bar fills the screen
        draw_bar_row(ax, 0.54, "ONE BILLION\nDOLLARS", BILLION, BILLION, GOLD, alpha=t, animate_t=t)

        if f > BEAT1_START + 60:
            years_to_earn = BILLION / MEDIAN_SALARY
            draw_text_centered(ax,
                f"{years_to_earn:,.0f} YEARS\nat median salary.",
                0.35, fontsize=24, color=GOLD, alpha=0.95)
        if f > BEAT1_START + 120:
            draw_text_centered(ax, "That's before the\npyramids were built.",
                               0.22, fontsize=16, color=DARK_TEXT, alpha=0.8)
        return

    # ── BEAT 2: $1/second ──
    if f < BEAT2_END:
        t = ease_out((f - BEAT2_START) / 30)

        draw_text_centered(ax, "What if you earned\n$1 every SECOND?", 0.65,
                           fontsize=26, color=OFF_WHITE, alpha=t)

        if f > BEAT2_START + 50:
            # Counting animation
            elapsed = f - BEAT2_START - 50
            count_progress = ease_out(elapsed / 80)
            years_val = count_progress * 31.7
            draw_text_centered(ax, f"{years_val:.1f} years", 0.48,
                               fontsize=42, color=LIME, alpha=min(elapsed / 20, 1.0))
            draw_text_centered(ax, "to reach $1 billion.", 0.36,
                               fontsize=18, color=OFF_WHITE, alpha=min(elapsed / 30, 1.0))

        if f > BEAT2_START + 130:
            draw_text_centered(ax, "31 years and 8 months.\nNon-stop. No sleep.", 0.22,
                               fontsize=15, color=DARK_TEXT, alpha=0.85)
        return

    # ── BEAT 3: Elon ──
    if f < BEAT3_END:
        draw_title()
        t = ease_out_expo((f - BEAT3_START) / 45)

        # Rescale everything to Elon's wealth
        draw_bar_row(ax, 0.80, "Median", MEDIAN_SALARY, ELON, OFF_WHITE, alpha=0.3)
        draw_bar_row(ax, 0.72, "Top 1%", TOP_1_PCT, ELON, LIME, alpha=0.3)
        draw_bar_row(ax, 0.64, "Millionaire", MILLION, ELON, "#4285F4", alpha=0.3)
        draw_bar_row(ax, 0.56, "$1 Billion", BILLION, ELON, GOLD, alpha=0.5)

        # Elon's bar
        draw_bar_row(ax, 0.44, "Elon Musk\nNet Worth", ELON, ELON, CRIMSON, alpha=t, animate_t=t)

        if f > BEAT3_START + 80:
            years_elon = ELON / MEDIAN_SALARY
            draw_text_centered(ax,
                f"{years_elon / 1e6:.1f} MILLION YEARS\nof your salary.",
                0.25, fontsize=22, color=CRIMSON, alpha=0.95)

        if f > BEAT3_START + 150:
            draw_text_centered(ax, "Let that sink in.", 0.12,
                               fontsize=16, color=DARK_TEXT, alpha=0.85)
        return

    # ── PUNCHLINE ──
    if f < PUNCH_END:
        t = ease_out((f - PUNCH_START) / 30)
        draw_text_centered(ax,
            "If you started earning\n$60K/year when the\nDINOSAURS went extinct...",
            0.60, fontsize=22, color=OFF_WHITE, alpha=t)

        if f > PUNCH_START + 60:
            t2 = ease_out((f - PUNCH_START - 60) / 25)
            draw_text_centered(ax,
                "you'd STILL need another\n62 million years.",
                0.32, fontsize=26, color=CRIMSON, alpha=t2)

        if f > PUNCH_START + 120:
            draw_text_centered(ax, "...to match Elon.", 0.18,
                               fontsize=18, color=GOLD, alpha=0.9)
        return

    # ── CLOSER ──
    t = ease_out((f - CLOSE_START) / 20)
    draw_text_centered(ax, "FINANCE ROAST CENTRAL", 0.55,
                       fontsize=28, color=LIME, alpha=t)
    draw_text_centered(ax, "Follow for more finance roasts", 0.42,
                       fontsize=16, color=OFF_WHITE, alpha=t * 0.85)


print("Generating Demo 3: Wealth Scale (55s)...")
print(f"  Total frames: {TOTAL_FRAMES} at {FPS}fps = {TOTAL_FRAMES / FPS:.1f}s")
output_path = os.path.join(OUTPUT_DIR, "demo3_wealth_scale.mp4")

anim = animation.FuncAnimation(fig, draw_frame, frames=TOTAL_FRAMES, interval=1000 // FPS)
anim.save(output_path, writer="ffmpeg", fps=FPS, dpi=160)
plt.close("all")

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Done! {output_path} ({size_mb:.1f} MB, {TOTAL_FRAMES / FPS:.1f}s)")
