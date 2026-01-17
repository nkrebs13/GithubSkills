# Prompt Templates for Image Generation

## Base Prompt Structure

All prompts follow a structured format to ensure consistent, high-quality outputs from the Gemini image generation API.

```
[ASSET_TYPE] [STYLE_MODIFIERS], [SUBJECT_DESCRIPTION], [COLOR_PALETTE], [TECHNICAL_REQUIREMENTS], [NEGATIVE_CONSTRAINTS]
```

### Component Breakdown

| Component | Purpose | Example |
|-----------|---------|---------|
| ASSET_TYPE | Define the output format | "App icon design", "Splash screen" |
| STYLE_MODIFIERS | Art direction | "Modern flat design", "3D rendered" |
| SUBJECT_DESCRIPTION | Core visual content | "A minimalist mountain peak" |
| COLOR_PALETTE | Color guidance | "Using deep purple and gold accents" |
| TECHNICAL_REQUIREMENTS | Format specs | "Square format, centered composition" |
| NEGATIVE_CONSTRAINTS | What to avoid | "No text, no complex backgrounds" |

---

## App Icon Prompts

### High Certainty (Clear Brand/Concept)

Use when the app purpose, brand, and visual direction are well-defined.

```
App icon design, [STYLE: modern/minimalist/playful/professional] aesthetic,
depicting [CORE_SYMBOL/METAPHOR] representing [APP_PURPOSE],
primary colors [HEX_OR_NAME], accent [HEX_OR_NAME],
[GRADIENT_DIRECTION if applicable] gradient,
single centered symbol, clean geometric shapes,
suitable for small display sizes, high contrast,
no text, no photography, no busy backgrounds
```

**Example - Fitness App:**
```
App icon design, energetic modern aesthetic,
depicting a dynamic flame shape merged with an upward arrow representing fitness progress,
primary color vibrant orange #FF6B35, accent deep charcoal #2D3436,
radial gradient from center,
single centered symbol, clean geometric shapes,
suitable for small display sizes, high contrast,
no text, no photography, no busy backgrounds
```

**Example - Finance App:**
```
App icon design, professional minimalist aesthetic,
depicting an abstract shield interlocked with a growth chart representing secure investing,
primary color deep navy #1A365D, accent metallic gold #D4AF37,
subtle linear gradient top to bottom,
single centered symbol, clean geometric shapes,
suitable for small display sizes, high contrast,
no text, no photography, no busy backgrounds
```

### Medium Certainty (Partial Brand Direction)

Use when the app category is known but visual direction needs exploration.

```
App icon design exploring [CATEGORY] visual themes,
[2-3 POSSIBLE METAPHORS] as potential focal elements,
color palette leaning [WARM/COOL/NEUTRAL] with [MOOD] feeling,
[STYLE_RANGE: e.g., "between minimal and detailed"],
single focal point, adaptable to circular or square framing,
versatile for light and dark backgrounds,
no text, simple composition
```

**Example - Meditation App (Exploring):**
```
App icon design exploring wellness and mindfulness visual themes,
lotus flower, gentle wave, or abstract breath pattern as potential focal elements,
color palette leaning cool with serene and calming feeling,
between minimal geometric and soft organic styling,
single focal point, adaptable to circular or square framing,
versatile for light and dark backgrounds,
no text, simple composition
```

### Low Certainty (Discovery/Brainstorming)

Use for initial exploration when minimal direction exists.

```
App icon concept for [CATEGORY] application,
generate [MOOD/EMOTION] feeling through abstract or symbolic imagery,
experiment with [STYLE_A] or [STYLE_B] approaches,
color exploration: [OPEN_RANGE or SUGGESTED_FAMILY],
prioritize instant recognizability and memorability,
suitable for app store display,
no text, avoid generic clip-art aesthetics
```

**Example - Productivity App (Discovery):**
```
App icon concept for productivity and task management application,
generate focused and empowering feeling through abstract or symbolic imagery,
experiment with geometric precision or dynamic motion approaches,
color exploration: bold primaries or sophisticated neutrals with one accent,
prioritize instant recognizability and memorability,
suitable for app store display,
no text, avoid generic clip-art aesthetics
```

---

## Splash Screen Prompts

### Branded Splash (With Existing Icon)

```
Mobile app splash screen, [ORIENTATION: portrait/landscape],
extending the visual language of [DESCRIBE_ICON_ELEMENTS],
[BACKGROUND_TREATMENT: solid/gradient/subtle pattern],
primary brand color [HEX] as dominant,
centered icon placement area with generous padding,
clean and professional, creates anticipation,
[ANIMATION_HINT if relevant: e.g., "radial reveal origin point"],
no text except optional brand wordmark zone
```

**Example:**
```
Mobile app splash screen, portrait orientation,
extending the visual language of a geometric flame icon with orange tones,
smooth gradient background transitioning from deep charcoal to near-black,
primary brand color #FF6B35 as accent glow effect,
centered icon placement area with generous padding,
clean and professional, creates anticipation,
subtle radial glow suggesting energy,
no text except optional brand wordmark zone below center
```

### Abstract/Ambient Splash

```
Mobile app splash screen, [ORIENTATION],
abstract [MOOD] background without literal imagery,
[COLOR_PALETTE] with smooth transitions,
[TEXTURE/PATTERN: e.g., "soft noise", "geometric mesh", "flowing curves"],
large negative space in center for icon overlay,
professional and polished, premium feel,
no text, no recognizable objects
```

---

## Feature Graphic Prompts (Google Play)

### Product-Focused Feature Graphic

```
Google Play feature graphic, 1024x500 pixels landscape,
showcasing [APP_NAME/CONCEPT] with [KEY_VISUAL_ELEMENT],
[STYLE] design approach,
primary colors [PALETTE] maintaining brand consistency,
device mockup showing [KEY_SCREEN/FEATURE] positioned [LEFT/RIGHT/CENTER],
headline text zone on [OPPOSITE_SIDE],
dynamic composition with clear visual hierarchy,
professional marketing quality, high impact
```

**Example:**
```
Google Play feature graphic, 1024x500 pixels landscape,
showcasing FitTrack fitness app with energetic motion graphics,
bold modern design approach,
primary colors vibrant orange and charcoal maintaining brand consistency,
phone mockup showing workout dashboard positioned right of center,
headline text zone on left third,
dynamic diagonal composition with clear visual hierarchy,
professional marketing quality, high impact
```

### Abstract/Brand Feature Graphic

```
Google Play feature graphic, 1024x500 pixels landscape,
abstract brand expression for [APP_CATEGORY],
[MOOD] atmosphere through color and shape,
brand colors [PALETTE] as foundation,
large logo/icon placement zone [POSITION],
supporting graphic elements suggesting [APP_BENEFIT],
clean and uncluttered, space for overlay text,
premium quality, distinctive
```

---

## Adaptive Icon Layer Prompts

### Foreground Layer

```
Adaptive icon foreground layer, 432x432 pixel canvas,
[ICON_SUBJECT] as single centered element,
content confined to inner 288x288 safe zone,
transparent background (alpha channel),
[STYLE] with [COLOR_TREATMENT],
optimized for circular, squircle, and rounded square masks,
clean edges, no anti-aliasing artifacts at boundaries
```

### Background Layer

```
Adaptive icon background layer, 432x432 pixels,
[SOLID_COLOR/GRADIENT/PATTERN] fill,
complementary to [FOREGROUND_DESCRIPTION],
[COLOR_SPECIFICATION],
subtle visual interest without competing with foreground,
seamless at edges if pattern-based
```

### Monochrome Layer (Android 13+)

```
Adaptive icon monochrome layer, 432x432 pixels,
silhouette version of [ICON_SUBJECT],
pure white on transparent background,
simplified shapes for single-color rendering,
maintain recognizability without color cues,
clean alpha channel edges
```

---

## Variation Directives

Use these modifiers to generate iterations while maintaining concept coherence.

### Color Variations

```
VARIATION: Regenerate with [NEW_COLOR_PALETTE] while maintaining identical composition and style
```

```
VARIATION: Create warmer/cooler temperature shift, moving primary toward [TARGET_HUE]
```

```
VARIATION: Increase/decrease saturation by approximately [PERCENTAGE]%, preserve value relationships
```

### Style Variations

```
VARIATION: Same concept with [MORE/LESS] geometric precision, [SOFTEN/SHARPEN] edges
```

```
VARIATION: Shift toward [ALTERNATIVE_STYLE: e.g., "3D rendered", "hand-drawn", "neon glow"]
```

```
VARIATION: Simplify complexity, reduce detail level while preserving core recognition
```

### Composition Variations

```
VARIATION: Adjust scale of central element [LARGER/SMALLER] by approximately [PERCENTAGE]%
```

```
VARIATION: Rotate primary element [DEGREES] clockwise/counterclockwise
```

```
VARIATION: Shift visual weight toward [TOP/BOTTOM/LEFT/RIGHT], maintain balance
```

### Mood Variations

```
VARIATION: Make [MORE/LESS] [MOOD: playful/serious/energetic/calm] through shape and color adjustment
```

```
VARIATION: Add [SUBTLE/PRONOUNCED] sense of [QUALITY: depth/motion/stability/innovation]
```

---

## Iteration Learning Templates

Use after evaluation to guide next generation.

### Improvement Prompt (Score < 7)

```
ITERATION based on feedback:
Previous attempt [DESCRIBE_WHAT_WORKED],
Issues identified: [SPECIFIC_PROBLEMS],
Adjustments needed:
- [CHANGE_1]
- [CHANGE_2]
- [CHANGE_3]
Maintain: [ELEMENTS_TO_PRESERVE]
Regenerate with these modifications
```

### Refinement Prompt (Score 7-8.5)

```
REFINEMENT iteration:
Strong foundation with [SUCCESSFUL_ELEMENTS],
Polish needed in [SPECIFIC_AREAS],
Subtle adjustments:
- [TWEAK_1]
- [TWEAK_2]
Preserve overall composition and color harmony,
Increase [SPECIFIC_QUALITY: e.g., "professional polish", "visual impact"]
```

### Alternative Exploration (Score 7+ but exploring options)

```
ALTERNATIVE exploration:
Current direction successful, generating variant for comparison,
Same core concept with [ALTERNATIVE_APPROACH],
Maintain brand alignment and technical requirements,
Explore [DIFFERENT_ASPECT] as distinguishing element
```

---

## Technical Quality Modifiers

Add these to any prompt for improved output quality.

### Resolution and Clarity
```
High resolution, crisp edges, no blur, no compression artifacts
```

### Professional Polish
```
Production-ready quality, suitable for commercial use, polished finish
```

### Format Compliance
```
[SQUARE/RECTANGULAR] format, [DIMENSIONS] pixels, [WITH/WITHOUT] transparency
```

### Print/Digital Optimization
```
Optimized for [SCREEN/PRINT] reproduction, [RGB/CMYK] color space considerations
```

---

## Prompt Chaining Strategy

For complex assets, use sequential prompts:

1. **Concept Generation**: Low certainty prompt to explore directions
2. **Direction Selection**: Evaluate outputs, identify strongest concept
3. **Refinement**: Medium certainty prompt building on selected direction
4. **Polish**: High certainty prompt with specific requirements
5. **Variations**: Generate color/style alternatives of final concept
6. **Asset Production**: Technical prompts for each required size/format

---

## Anti-Patterns to Avoid

### Overly Vague
```
BAD: "Make a nice app icon"
GOOD: "App icon design, minimalist flat aesthetic, depicting an abstract book with bookmark, navy and gold palette..."
```

### Contradictory Requirements
```
BAD: "Simple icon with lots of intricate details"
GOOD: "Clean icon with one detailed focal element on simple background"
```

### Technical Impossibilities
```
BAD: "Photorealistic 3D icon that looks hand-drawn"
GOOD: "3D rendered icon with soft, illustrative shading"
```

### Brand Misalignment
```
BAD: "Playful cartoon icon" (for a law firm app)
GOOD: "Professional, trustworthy icon with subtle sophistication"
```
