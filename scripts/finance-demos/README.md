# Finance Roast Central — Demo Videos

Proof-of-concept data visualization animations for the finance Shorts channel.

## Generated Videos

All output in `output/` directory (gitignored — regenerate with the scripts below).

### Demo 1: Bar Chart Race — Top Companies by Market Cap (2000–2024)
```
python3 scripts/finance-demos/demo1_bar_chart_race.py
```
- **Format:** 1080×1920 (9:16), H.264 MP4, ~6s
- **Data:** Curated from CompaniesMarketCap.com, Wikipedia, Visual Capitalist
- **Shows:** Nvidia's dramatic rise, Apple overtaking Microsoft, market cap explosion post-2020

### Demo 2: Inflation Crisis Timeline (1970–2024)
```
python3 scripts/finance-demos/demo2_inflation_timeline.py
```
- **Format:** 1080×1920 (9:16), H.264 MP4, ~7s
- **Data:** BLS / FRED CPI-U annual average % change
- **Shows:** Oil crises, Volcker peak at 13.5%, post-COVID 8% spike, annotated crisis events

### Demo 3: Wealth Scale Comparison — "How Big Is a Billion?"
```
python3 scripts/finance-demos/demo3_wealth_scale.py
```
- **Format:** 1080×1920 (9:16), H.264 MP4, ~11s
- **Data:** Forbes billionaire list, BLS median wage
- **Shows:** Progressively absurd wealth comparisons ending with "4.2 million years of median salary"

## Requirements

```
pip install bar_chart_race matplotlib pandas pillow
apt install ffmpeg
```

## Brand Colors

- Navy: `#0A1628` (backgrounds)
- Lime: `#00FF88` (data highlights, positive)
- Crimson: `#CC0000` (danger, crashes, roast punchlines)
- Off-white: `#F5F5F0` (text, labels)
