# AI Image & Video Generation Prompts for Finance Content

## Core Prompting Principles

### 1. Lead with metaphor, not data
Replace "a falling stock chart" with "a cathedral made of gold crumbling in slow motion." Visual metaphors that viewers already know, made concrete, outperform literal data visualization every time.

### 2. Use cinematographer vocabulary
Camera direction is the most powerful prompt element for video models. Terms like "crane shot," "handheld verite," "rack focus," and "shallow depth of field" are interpreted as direct directives by Veo 3.1, Kling 2.5, and Sora 2.

### 3. Specify style as reference, not genre
Instead of "editorial style," write "in the style of a TIME Magazine cover illustration, gouache on paper texture, bold flat colors." Doubling down on technique description produces more consistent results than vague genre labels.

## Platform Capabilities

| Platform | Output Type | Best For | Pricing |
|----------|-------------|----------|---------|
| Fal.ai + FLUX.1 [pro] | Static image | Editorial illustration, infographic-style | $0.03/megapixel |
| Fal.ai + FLUX.2 [pro] | Static image | High-consistency editorial, text rendering | $0.03-$0.09/image |
| Replicate + FLUX.1 | Static image | API-first, fine-tuning, style LoRA customization | Per-second compute |
| HuggingFace (FLUX.1-dev) | Static image | Open-source, no-cost experimentation | Free |
| Kling 2.5 Turbo | Animated clip (4-10s) | Physics-accurate financial metaphor motion | $6.99-$127.99/mo |
| Seedance 1.0 Pro | Animated clip (5-10s) | Multi-shot storytelling, cinematic style | ByteDance API/Fal |
| Higgsfield Cinema Studio | Cinematic clip | Director-controlled camera, emotional storytelling | API-based |
| Sora 2 (OpenAI) | Short video (up to 60s) | Surrealist/conceptual financial metaphor | ChatGPT Pro plan |
| Veo 3.1 (Google Flow) | Cinematic clip (4-8s) | High-fidelity realism, native audio sync | $250/mo AI Ultra |
| MiniMax (Hailuo) | Animated clip | Underwater/surreal dynamics, free tier available | Free-paid |
| OpenRouter | Routes to multiple models | Multi-model testing, API aggregation | Per-model token cost |

## 10 Finance Prompt Archetypes

### 1. Market Crash (Static — Fal.ai FLUX.1)
```
Editorial illustration for a financial magazine cover. A towering glass skyscraper
shaped like a bar chart at its peak shatters from the base upward, thousands of
glass shards catching golden afternoon light mid-explosion. People in business
suits below are frozen in shock, briefcases open, paper money swirling in the
debris cloud. The sky is blood-orange sunset. Style: painterly gouache illustration,
thick visible brushstrokes, bold shadows, deep reds and charcoal blacks.
Composition: low-angle wide shot, dramatic foreshortening.
Time Magazine cover quality editorial illustration.
```

### 2. Wealth Inequality (Animated — Kling 2.5 / Seedance)
```
A gilded palace floats in the sky above a flooded city street.
Velvet-roped golden staircases ascend from rooftops to the palace entrance;
people in threadbare clothing climb the stairs and collapse before reaching the top.
Water rises slowly in the streets below. The palace glows warmer and brighter
as the water rises higher. Camera: slow crane shot upward from street level to
palace entrance, ending on the gilded gate closing. Lighting: cold blue below,
warm amber above. Cinematic realism, shallow depth of field, film grain.
```

### 3. Inflation (Animated — MiniMax / Kling 2.5)
```
Wide shot: A grocery store aisle. A shopping basket in the foreground slowly
fills with items — bread, milk, vegetables — but as each item is placed inside,
the basket visibly shrinks. By the final item, the basket is the size of a toy.
A hand reaches in to take the groceries out; they barely fit in one palm.
The aisle background remains perfectly still and bright, contrast to the shrinking.
Camera: static medium shot, slight push-in over 8 seconds.
Warm retail lighting. Hyperrealistic. No text.
```

### 4. Central Bank / Interest Rates (Static — Fal.ai FLUX.2)
```
A giant stone hand emerges from grey storm clouds, holding a screw made of gold,
tightening it into the center of a vast city visible far below. Streets below
compress together as the screw turns — buildings get closer, streets narrow,
people shrink. The sky is stormy with dramatic crepuscular light rays breaking
through. Style: conceptual editorial illustration, reminiscent of Der Spiegel
or The Economist cover art, flat matte colors, geometric composition,
slight vintage texture overlay. 16:9 horizontal layout.
```

### 5. Tech Stock Dominance (Video — Veo 3.1 / Higgsfield)
```
An aerial crane shot descending from space to reveal Earth. As the camera
descends, six enormous corporate logos (rendered as glowing temple structures
on the landscape) cast shadows that cover entire continents. The remaining
buildings and cities around them are dark and tiny by comparison.
The logos pulse with blue-white light. The camera stops at ground level looking
up at one logo-temple, massive and imposing against the stars.
Style: cinematic realism, Blade Runner 2049 color palette — deep teal shadows,
amber light sources. No dialogue. Ambient synthetic hum audio. 9:16.
```

### 6. Debt Spiral (Static + Animated — FLUX.1 → Kling I2V)
**Image:**
```
Editorial illustration: A person in business attire stands at the center,
wrapped head-to-toe in chains made of gold. The chains extend outward and loop
back to attach to their own wrists and ankles — the person is holding their
own chains. Expression: exhausted and resigned. Background: infinite grey
marble floor, dramatic spotlight from above. Style: high-contrast graphic novel,
thick ink outlines, limited palette — gold chains, grey environment, red tie.
```
**Animate:**
```
The figure slowly realizes the chains are attached to their own hands.
They pull one chain and it tightens another.
Camera: slow zoom in on face as realization dawns.
Subtle chain movement. 8 seconds. Cinematic, no sudden cuts.
```

### 7. Money Printing / QE (Video — Sora 2 / Veo 3.1)
```
A printing press the size of a mountain. It prints gold banknotes the size of
surfboards. As the notes fly off the press and fill the landscape, the sky
darkens and the color drains from the notes — they become visibly grey
and translucent. A man stands in the growing pile, initially celebrating,
then looking at his handful as it fades. The pile is enormous but weightless —
notes blow away like ash in the wind. Camera: wide (mountain press),
then cut to close-up of man's face and fading notes.
Style: Cinematic photorealism. Warm golden to cold grey color grade transition.
No text or labels. 9:16 vertical format.
```

### 8. Recession (Static + Animated — Replicate FLUX.1 → Seedance)
**Image:**
```
Editorial illustration for a business newspaper. A vast country made entirely
of origami paper folds inward on itself — mountains fold flat, cities compress
into a suitcase, rivers fold into a drawer. The whole country shrinks to
the size of a briefcase on a boardroom table. A person in a suit stands beside
it, looking at the miniaturized country with a measuring tape.
Style: The Economist illustration aesthetic — clean, editorial, muted blue-grey
palette, conceptual composition, minimal but not childish.
```

### 9. Bull vs Bear / Volatility (Higgsfield + Seedance)
**Image:**
```
Cinematic wide shot of a medieval jousting arena. On one side,
a glowing golden bull the size of a building charges.
On the other, an enormous black bear in silver armor braces.
The crowd fills the stands — all wearing suits and ties.
The arena floor is covered with ticker symbols instead of sand.
Dramatic backlight from the setting sun.
Color palette: deep navy stadium, gold bull, obsidian bear. Film grain.
```
**Animate:**
```
The bull and bear charge at full speed toward each other.
As they collide, the arena shakes and ticker symbols explode outward
like confetti. The crowd flings briefcases — half in celebration, half panic.
Camera: wide tracking shot that pulls back as the collision happens.
Duration 8s, cinematic slow-motion collision, 1080p.
```

### 10. AI Disruption (Multi-shot — Sora 2 / Veo 3.1)
```
Scene 1 (0-8s): A stately marble bank building, centuries old. Suited bankers
work at wooden desks inside, counting cash by hand. Warm sepia light.
Slow dolly shot through the window.

Scene 2 (8-16s): Lightning strikes. The marble walls peel back like
fruit skin to reveal a glowing data center beneath — server racks where
vaults were, fiber optic cables where marble columns stood.
Match cut: wooden desk morphs into a screen showing live trading data.

Scene 3 (16-24s): Wide shot — bank exterior is now half-marble,
half-holographic. Traditional bankers and glowing robotic figures work
side by side, uncertain expressions on both.

Camera: cinematic progression warm to cold color temperature.
Audio: quill on paper → electric hum → silence. 9:16. Film grain.
```

## Platform-to-Use-Case Matrix

| Finance Topic | Static Image | Short Clip (4-10s) | Cinematic Video (15-60s) |
|--------------|-------------|-------------------|------------------------|
| Market Crash | Fal.ai FLUX.1 | Kling 2.5 I2V | Sora 2 multi-shot |
| Wealth Inequality | Replicate FLUX.1-dev | Seedance 1.0 Pro | Higgsfield + Veo 3.1 |
| Inflation | HuggingFace FLUX.1-dev | MiniMax text-to-video | Veo 3.1 Google Flow |
| Central Bank Policy | Fal.ai FLUX.2 | Kling 2.5 Turbo | Sora 2 |
| Tech Dominance | Midjourney (painterly) | Seedance 1.0 Pro | Veo 3.1 |
| Debt Spiral | Fal.ai FLUX.1 base image | Kling 2.5 I2V | Higgsfield Cinema |
| QE / Money Printing | Replicate FLUX.1 | MiniMax | Sora 2 |
| Recession | Replicate fine-tuned FLUX | Seedance 1.0 lens switch | Veo 3.1 |
| Market Volatility | HuggingFace FLUX.1-dev | Higgsfield → Seedance | Sora 2 |
| AI Disruption | Fal.ai FLUX.2 | Kling 2.5 multi-shot | Sora 2 / Veo 3.1 |

## 5 Viral Visual Principles

1. **Instant decoding** — Metaphor communicates concept in <2 seconds with sound off
2. **Scale contrast** — Tiny person vs enormous structure makes abstract quantities visceral
3. **Familiar made strange** — Everyday objects with financial logic applied surreally
4. **Color as narrative** — Warm-to-cold transition carries entire stories (prosperity → crisis)
5. **No text overlay needed** — Visual alone drives emotional response; text reinforces but isn't required

## Advanced Techniques

### Style Locking for Series Consistency
LoRA fine-tuning on Replicate with 15-20 reference images ($1.85 training run on H100) produces a style-locked model for consistent editorial illustrations across an entire content series.

### Multi-Shot Video with Seedance 1.0 Pro
The `lens switch` command creates editorial-style cut sequences within a single prompt. A full Shorts-length narrative (5-7 shots) can be generated from a single prompt by chaining `lens switch` transitions.

### Higgsfield + Veo 3.1 + Seedance Pipeline
1. Higgsfield Popcorn → Lock composition, tone, character visual
2. Seedance or Veo 3.1 → Animate with full scene motion
3. Higgsfield Recast → Replace or refine characters without breaking lighting

### Veo 3.1 Native Audio
Generate synchronized ambient sound from the text prompt — breaking glass, printing press noise, alarm bells — no audio post-production required.

## Source

Perplexity research, April 2025. Platform capabilities from official documentation and creator tutorials.
