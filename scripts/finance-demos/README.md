# Finance Roast Central — Demo Videos

Proof-of-concept data visualization Shorts for the finance channel.
Each video follows the playbook's 5-part narrative structure:
**Hook (0-3s) → Setup (3-6s) → 3 Data Beats (6-42s) → Punchline → Closer**

All videos are muted-friendly with on-screen text overlays on every stat.

## Generated Videos

Output in `output/` (gitignored — regenerate with the scripts below).

### Demo 1: "24 Years of Tech Dominance in 50 Seconds"
```
python3 scripts/finance-demos/demo1_bar_chart_race.py
```
- **Duration:** 50s · 1080×1920 (9:16) · H.264
- **Data:** CompaniesMarketCap.com, Wikipedia, Visual Capitalist
- **Hook:** "Which company went from $3B to $3.4 TRILLION?"
- **Beat 1:** Apple's iPhone era ($15B → $500B)
- **Beat 2:** COVID tech explosion + Saudi Aramco at $2T
- **Beat 3:** Nvidia's 1,133x return
- **Punchline:** "$1,000 in Nvidia in 2000 = $1.1 MILLION today"

### Demo 2: "54 Years of US Inflation in 50 Seconds"
```
python3 scripts/finance-demos/demo2_inflation_timeline.py
```
- **Duration:** 50s · 1080×1920 (9:16) · H.264
- **Data:** BLS / FRED CPI-U annual average % change
- **Hook:** "The Fed says 2% inflation is 'normal.' Here's what ACTUALLY happened."
- **Beat 1:** 1980 Volcker peak at 13.5%
- **Beat 2:** 2009 deflation — prices actually fell
- **Beat 3:** 2022 post-COVID spike at 8.0%
- **Punchline:** "From 13.5% to 0% to 8% — all in one lifetime"

### Demo 3: "How Long to Earn $1 Billion? (You'll Hate This)"
```
python3 scripts/finance-demos/demo3_wealth_scale.py
```
- **Duration:** 55s · 1080×1920 (9:16) · H.264
- **Data:** Forbes billionaire list, BLS median wage
- **Hook:** "How long would it take YOU to earn $1 billion?"
- **Beat 1:** $1B = 16,667 years at median salary (before the pyramids)
- **Beat 2:** At $1/second, $1B takes 31 years and 8 months
- **Beat 3:** Elon's wealth = 4.2 million years of your salary
- **Punchline:** "If you started earning $60K when the dinosaurs went extinct... you'd still need 62 million more years"

## Requirements

```
pip install bar_chart_race matplotlib pandas pillow
apt install ffmpeg
```

## Narrative Structure (from Playbook §4, §11)

Every video follows:
1. **Hook (0-3s)** — Question or shocking claim. Works muted (on-screen text).
2. **Setup (3-6s)** — One line of context.
3. **Data Beats (6-42s)** — 3 stat reveals with on-screen commentary + pause holds.
4. **Punchline** — Biggest comparison with dramatic text reveal.
5. **Closer** — "FINANCE ROAST CENTRAL · Follow for more finance roasts"

## Brand Colors

- Navy: `#0A1628` (backgrounds)
- Lime: `#00FF88` (data highlights, positive reveals)
- Crimson: `#CC0000` (danger, crashes, roast punchlines)
- Off-white: `#F5F5F0` (text, labels)
- Gold: `#FFD700` (wealth/money reveals)
