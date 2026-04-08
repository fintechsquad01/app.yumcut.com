# Finance Shorts Template Design Decisions

## Overview

This document captures the rationale behind every design decision for the YumCut finance Shorts templates. All decisions are informed by competitive research (see docs 01-04 in this directory).

## Critical Pipeline Fix: textPrompt → LLM Wiring

**Discovery:** The template's `textPrompt` field was stored in the DB but NEVER sent to the LLM. The daemon read only `jobPayload.prompt` (user input). All template textPrompts were dead code.

**Fix:** 3 files changed to wire textPrompt into the script generation:
1. Creation snapshot API now includes `template.textPrompt`
2. CreationSnapshot type includes `textPrompt` field
3. Script phase prepends `template.textPrompt` before user's prompt as: `[textPrompt]\n\nTopic: [user input]`

**Impact:** All templates (not just finance) now have their textPrompt influence the generated script. This is how the textPrompts were designed to work — as system instructions that shape how the LLM writes for any user topic.

## Templates: 3 (Renamed from Phase 1)

### Phase 2: Renamed to Remove Format Lock
Templates were renamed to be tone-flexible, not locked to "roast" or satire:

| Template | Code | Art Style | Purpose |
|----------|------|-----------|---------|
| Finance Story | `finance_story` | Editorial Cartoon | Versatile finance storytelling — any topic, any tone (satirical/dramatic/educational/trending) |
| Finance Reveal | `finance_reveal` | Visual Metaphor | Data stair-stepping — follow one number on a journey from relatable to incomprehensible |
| Finance Scenario | `finance_scenario` | Editorial Cartoon (shared) | What-if hypotheticals with real economic consequences — trending scenarios |

### Why Renamed (from `finance_roast`, `finance_dataviz`, `finance_whatif`)
- `finance_roast` locked the tone to satire. Top finance channels (Nick Invests, Primate Economics, Crayon Capital) are flexible.
- `finance_story` is the workhorse — any finance topic told as a story, adaptable to trends
- `finance_reveal` is the data format — the MrBeast stair-stepping principle applied to finance
- `finance_scenario` is the imagination format — trending hypotheticals with chain-reaction consequences

### Removed (Phase 1)
| Template | Code | Reason |
|----------|------|--------|
| Finance News Roast | `finance_news` | Overlaps with `finance_story` |
| Finance Podcast Roast | `finance_podcast` | Too niche — podcast summaries can use `finance_story` |

## Art Style: Editorial Cartoon (Economist/TIME)

### Why this style?
Research identified 7 visual style categories in animated finance Shorts. We chose **Cinematic Documentary Illustration** (Crayon Capital / Economist covers) because:

1. **Matches satirical tone** — editorial cartoons are inherently opinionated, which aligns with "Bloomberg data meets comedy club"
2. **Visual metaphors over literal data** — every research finding shows that expressive characters reacting to absurdity outperform literal charts
3. **AI image generators handle it well** — editorial illustration with bold outlines, flat colors, and clear composition produces consistent results
4. **Distinctiveness** — no other YumCut template uses this style; it won't overlap with Anime, Cyberpunk, or Cartoon
5. **Mobile readability** — bold silhouettes, high contrast, and simple compositions read well at 9:16 on small screens

### Art style prompt structure
Both prompts follow the proven YumCut pattern:
```
STYLE GUIDANCE:
- [Style reference (specific publications/artists, not vague genres)]
- [Character design guidance]
- [Visual metaphor direction]
- [Color palette with hex codes]
- [Ink/texture technique]
- [Composition rules (9:16, subject dominance)]
- [Lighting direction]
- [Scale contrast guidance]

REMINDER: [Core constraint — no text/lettering]
```

### The `finance-dataviz` pivot
The original dataviz art style asked for "charts, graphs, and data elements." Research showed this is wrong:
- AI image generators produce poor literal charts
- Viral finance Shorts use visual metaphors (shrinking baskets for inflation, crumbling buildings for crashes)
- The 5 viral visual principles all depend on metaphor, not data display

The rewritten prompt targets "cinematic visual metaphor illustration" — Der Spiegel / Economist cover art with painterly texture.

## Script Generation (`textPrompt`)

### Key decisions
1. **No timecodes** — The LLM generates text, not timed narration. Timecodes (0-3s, 3-10s) are meaningless to the model.
2. **Hook-first structure** — All 3 templates open with a specific hook pattern drawn from the 6 research-backed archetypes.
3. **1-thesis rule** — Every template prompt enforces "all data points must prove the same single thesis."
4. **Loop mechanic** — All templates instruct the closer to "loop back to the opening hook" for replay-driven algorithm boost.
5. **Conversational + dramatic hybrid tone** — Matches research finding that this tone combination has the highest viral ceiling.

### Template-specific hook patterns
| Template | Primary Hook Type | Example |
|----------|------------------|---------|
| `finance_roast` | Reframe Stat / Contrarian Instruction | "Stop saving money" or "$5 coffee = $187K" |
| `finance_dataviz` | Reframe Stat / Scaled Consequence | "The average American will work 40 years and retire with less than $100K" |
| `finance_whatif` | Provocative Hypothetical | "What if the US printed a $1 trillion coin?" |

## Caption Preset: `financegold`

### Design rationale
The `financegold` preset targets a hybrid of:
- **System 1 (Hormozi Word-Highlight)** — word-by-word animation, gold keyword highlights, ALL CAPS, heavy stroke
- **System 5 (Kinetic Data)** — number counter animation for data reveals

This matches the finance niche conventions:
- Gold (#FFD700) for wealth/emphasis (maps to brand palette)
- Red (#CC0000) for negative concepts (stock market color convention)
- Green (#00FF88) for positive outcomes
- ALL CAPS + heavy black stroke for mobile readability
- Word-by-word produces +15% engagement lift for finance content

## Voice: Fast Male (ElevenLabs)

### Why male voice?
- The "data analyst doing late-night stand-up" persona maps most naturally to male voice delivery
- Research shows conversational + dramatic hybrid requires tonal range — ElevenLabs' fast male voices (Finn, Mark, Alex) handle this
- For >30s Shorts with irony/urgency, premium voice is required (AI voice has 19.6% higher drop-off for these tones)

### Voice hierarchy
```
fastMaleVoiceId resolution:
1. English + male + fast
2. English + male (any speed)
3. Male + fast (any language)
4. Male (any)
5. Fallback to female fast voice
```

## Music & Overlay

### Music: Backbeat Groove (default)
- Upbeat background music matches the satirical entertainment tone
- Finance Shorts research shows music is secondary to hook/narration for retention
- Default music is acceptable for initial launch; custom finance-specific music can be added later

### Overlay: Sparkles (default)
- Matches the entertainment/satirical tone
- Could be swapped for a more editorial overlay in the future
- Research shows overlay has minimal impact on retention vs hook quality

## Weight: 50 (Moderate Visibility)

- `weight: 0` = hidden from default template list (previous setting)
- `weight: 50` = visible but not dominant (established templates are 66-150)
- Allows discovery without competing with proven templates like Basic (100), Cyberpunk (96), etc.

## Script Guidance Files

### Why separate from templates?
- `scriptCreationGuidance` and `scriptAvoidanceGuidance` are **user-level settings**, not template-level
- Templates influence scripts only through `textPrompt`
- The guidance files (`content/prompts/finance-script-*.txt`) serve as copy-paste reference for users

### What they encode
- **Creation guidance**: Hook archetypes, 5-part structure, loop mechanic, stat sourcing rules
- **Avoidance guidance**: No financial advice, no setup before hook, no multi-thesis scripts, no bland transitions

## What Was Removed

| Item | Reason |
|------|--------|
| 3 Python demo scripts (matplotlib) | Bypassed YumCut pipeline entirely |
| Nano Banana Pro image provider | No external provider endpoint exists |
| images-phase.ts customData routing | Dead code without provider |
| finance-prompt-catalog.json | Not referenced by any code |
| 4 extra prompt files (infographic, thumbnail, editorial cartoon, crisis scene) | Not used by any template |
| .gitignore entry for demo output | Only needed for deleted demos |
