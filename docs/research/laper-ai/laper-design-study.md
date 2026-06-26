# Laper.ai Design Study

Date: 2026-06-27
Source: https://laper.ai/
Scope: desktop landing page visual system, component language, motion cues, and patterns that can be translated into 夜航船之书.

## Research Method

The desktop landing page was inspected in the in-app browser across the hero, transition panel, feature-card row, product demo frames, writing-assistant split, and lower conversion section. The public repository intentionally keeps only this synthesized study, not raw third-party screenshots or full page-capture text.

Mobile capture was attempted, but Laper intermittently returned `ERR_SSL_PROTOCOL_ERROR` in the in-app browser after the desktop session. Desktop evidence is sufficient for the current visual-language pass.

## Core Impression

Laper feels polished because it treats the page as a live product surface, not a brochure. The hero is not a decorative slogan; it shows a believable working object. The rest of the page continues that promise through product-state cards, repeated screenshot frames, quiet copy, and very small but precise controls.

The visual mood is restrained: off-white canvas, dark green-black text, muted green CTA, thin separators, pale grey-green surfaces, and low-opacity topographic lines. There is little color drama. The richness comes from depth, layering, and object realism.

## Visual System

- Canvas: almost white, slightly green-tinted, approximately `rgb(252,253,252)`.
- Primary text: near-black with green undertone, approximately `rgb(23,26,25)`.
- Secondary text: muted grey-green, approximately `rgb(107,115,112)`.
- Action green: deep but not saturated, approximately `rgb(26,74,53)`.
- Surfaces: translucent whites and `rgb(244,246,245)`, often separated by hairline borders.
- Background texture: subtle contour/topographic line pattern, low contrast and mostly decorative.
- Shadow: very light, usually `rgba(0,0,0,0.05)` with 1-6px blur range.

## Typography

- Global type is small and quiet. Most body and UI text sits at `12px`, `13px`, or `16px`.
- Headings are not oversized after the hero. Section headers around `20px` create a calm editorial rhythm.
- Weight is mostly 400. 500 and 600 are reserved for UI labels or script metadata. Heavy display type is avoided.
- Copy uses short lines and a lot of air. The page trusts spacing more than emphasis.

For 夜航船之书, this means the current very large WenKai title can remain as a signature, but the rest of the page needs smaller, quieter, denser product objects around it. The site should not be all calligraphic drama.

## Component Patterns

### Floating Composer

Laper's strongest component is the hero composer: a large rounded white input shell floating over product context. It immediately communicates "this product is usable here." Its button is small relative to the input, which makes the composition feel calm rather than salesy.

Translation for 夜航船: create a "夜航札记 / tool query" composer in the hero, where the visitor sees a short, typed Chinese intent and four tool chips. This should feel like opening the ship log, not like a chatbot.

### Product Pages Behind The Hero

The hero background shows multiple script pages and languages. It creates depth and product credibility before any explanation.

Translation for 夜航船: place faint product sheets or log pages behind the hero composer. They can show tool names, status, platform, and abstract usage rows, not fake app screenshots.

### Feature Cards As Product States

The feature cards are not generic icon cards. Each card contains a small product scene: a list, a comment bubble, an advisor list. This makes the card evidence-based.

Translation for 夜航船: product cards should include mini states: download/source/status, compact feature rows, small product preview, and a clear "enter" affordance.

### Large Demonstration Frames

Laper repeatedly uses product screenshots inside large frames. These frames have rounded corners, quiet shadows, and sit on textured image beds.

Translation for 夜航船: every product page should start with a large demo frame and then show smaller "artifact cards" below it. Future real screenshots/videos can replace these frames cleanly.

### Micro Controls

Buttons are compact pills. The CTA color is the only saturated element. Secondary actions often look like plain text links with a small arrow.

Translation for 夜航船: reduce button size and count. Keep one warm primary action; convert many secondary buttons into text-arrow links.

## Motion Patterns

Observed motion is subtle: scroll reveal, slight position changes, soft appearance, and UI state transitions. The site avoids obvious spectacle.

Useful translation:

- Hero composer cursor/typing effect.
- Slow horizontal drift for background sheets.
- Product cards reveal in a staggered rhythm.
- Hover should slightly raise product-state objects, not warp them.
- Scroll should change the relation between foreground composer and background pages.
- Respect `prefers-reduced-motion`.

## What Not To Copy

- Do not copy screenwriting terminology or screenplay layouts directly.
- Do not use Laper's logo or brand colors exactly.
- Do not replace 夜航船's Chinese literary identity with generic SaaS typography.
- Do not add decorative complexity without product evidence.

## Night Sailing Translation Rules

1. Build a hero around a live object: a quiet "tool request" composer over ship-log pages.
2. Make every section prove something with a product state, not only prose.
3. Use smaller UI text and calmer hierarchy after the hero.
4. Introduce a thin-lined paper/contour background system across the whole page.
5. Convert the product grid into a more editorial deck: first two released tools get more visual weight, planned tools become compact future slips.
6. Add a sticky side index or section rail on desktop so scrolling feels deliberate.
7. Product detail pages should feel like launch pages: hero composer/context, large demo frame, feature evidence cards, media dock.
8. Motion should be felt as page breathing: reveal, drift, cursor, hover lift, and image depth.

## Implementation Priorities

- Add hero composer and background product sheets.
- Refactor product cards into evidence-rich states.
- Add section rail and progress marks.
- Add staggered reveal classes and typing/cursor animation.
- Tighten typography after the hero: smaller labels, smaller section copy, fewer oversized headings.
- Keep Chinese WenKai as the title/poetic voice, but use cleaner sans text for product evidence.
