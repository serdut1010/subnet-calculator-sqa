---
name: Technical Education System
colors:
  surface: '#f7f9ff'
  surface-dim: '#d7dae0'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4fa'
  surface-container: '#ebeef4'
  surface-container-high: '#e5e8ee'
  surface-container-highest: '#dfe3e8'
  on-surface: '#181c20'
  on-surface-variant: '#414754'
  inverse-surface: '#2d3135'
  inverse-on-surface: '#eef1f7'
  outline: '#727785'
  outline-variant: '#c1c6d6'
  surface-tint: '#005bc0'
  primary: '#005bbf'
  on-primary: '#ffffff'
  primary-container: '#1a73e8'
  on-primary-container: '#ffffff'
  inverse-primary: '#adc7ff'
  secondary: '#006e2b'
  on-secondary: '#ffffff'
  secondary-container: '#93f59e'
  on-secondary-container: '#00722d'
  tertiary: '#bb1712'
  on-tertiary: '#ffffff'
  tertiary-container: '#df3429'
  on-tertiary-container: '#ffffff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc7ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#96f8a1'
  secondary-fixed-dim: '#7adb87'
  on-secondary-fixed: '#002108'
  on-secondary-fixed-variant: '#00531f'
  tertiary-fixed: '#ffdad5'
  tertiary-fixed-dim: '#ffb4a9'
  on-tertiary-fixed: '#410001'
  on-tertiary-fixed-variant: '#930004'
  background: '#f7f9ff'
  on-background: '#181c20'
  surface-variant: '#dfe3e8'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 15px
    fontWeight: '500'
    lineHeight: 22px
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-tablet: 1.5rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-tablet: 2rem
  margin-desktop: 3rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system embodies an approachable, hyper-legible, and disciplined visual environment engineered for technical and vocational education. The aesthetic synthesizes the clarity and structure of modern Material architecture with the focused rigor of professional engineering workspaces.

Key Brand Attributes:
- **Didactic Clarity:** Information hierarchy eliminates visual noise to sustain deep cognitive focus across complex workflows (e.g., networking topologies, binary arithmetic, command line syntax).
- **Engineered Precision:** Crisp bounding strokes, deliberate whitespace, and structured modular panels anchor educational materials in reliable, predictable layouts.
- **Empathetic Utility:** Interactions feel responsive and forgiving; feedback is clear, immediate, and anchored by standard mental models from industry-standard tooling.

The visual style relies on minimal structural distraction: stark white and subtle slate surfaces, whisper-thin keyline divisions, and disciplined chromatic restraint where vibrant accents serve strictly semantic and pedagogical roles.

## Colors

The palette is anchored in utility, ensuring high legibility and immediate visual parsing across interactive simulations, terminal viewports, and tabular learning modules.

### Roles and Application
- **Canvas & Surfaces:**
  - Base canvas: `#FFFFFF` (pure white for root page backgrounds and active card interiors).
  - Surface subtle: `#F8F9FA` (used for app bars, side panels, nested containers, and alternating table rows).
  - Surface active / hover: `#F1F3F4` (interactive background state for inactive list tiles, chips, and muted controls).
- **Keylines & Boundaries:**
  - Standard border: `#E8EAED` (structural separators, container outlines, card borders).
  - Prominent border: `#DADCE0` (unfocused input strokes, prominent card perimeters, dividers requiring distinct visual anchoring).
- **Text & Iconography:**
  - Primary text: `#202124` (headlines, primary labels, code content; satisfies AAA contrast ratios on white).
  - Secondary text: `#5F6368` (supporting descriptions, metadata, inactive tab labels).
  - Muted / Placeholder text: `#80868B` (input placeholders, disabled iconography, tertiary timestamps).
- **Accents & Feedback:**
  - Primary action / Focus: `#1A73E8` (focus rings, active tabs, primary buttons). Active hover variant: `#174EA6`.
  - Educational validation (Success): `#188038` (successful test runs, verified packet routes, valid syntax markers).
  - Critical error / Alert: `#D93025` (syntax failures, malformed IP ranges, destructive resets).

## Typography

The typographic hierarchy separates explanatory pedagogical guidance from computational and technical values.

- **Primary Interface & Prose (`Plus Jakarta Sans`):** Delivers clean geometry with friendly, open apertures that reduce fatigue during extensive instructional reading and multi-step labs.
- **Data, Syntax, & Values (`JetBrains Mono`):** Dedicated exclusively to binary numbers, IPv4/IPv6 addresses, subnet masks, hexadecimal dumps, and terminal outputs. The fixed-width character grid guarantees alignment across multi-line binary matrices and tabular packet structures.
- **Implementation Rules:**
  - Terminal components and tabular metrics must strictly adopt `code-md` or `code-sm`.
  - Uppercase styling is permitted only for micro-labels (`label-sm`), state badges, and table column titles, paired with loose tracking (`0.04em`).

## Layout & Spacing

The layout is built upon an 8pt architectural rhythm, with a 4pt sub-grid reserved for fine micro-alignments (e.g., inline icons, code chip tags, and binary bit boxes).

### Grid System
- **Desktop (1024px+):** 12-column fluid grid within a 1440px maximum container. Gutters are fixed at `1.5rem` (24px) with `3rem` (48px) outside margin buffers. Split layouts prioritize interactive workspaces (8 cols) paired with reference/syllabus side panels (4 cols).
- **Tablet (600px - 1023px):** 8-column layout with `1.5rem` gutters and `2rem` outer padding. Auxiliary sidebars collapse into persistent drawer triggers.
- **Mobile (< 600px):** 4-column layout with `1rem` (16px) gutters and margins. Information density shifts into vertical stacks, while technical tables enable horizontal inertia scrolling.

### Spacing Application
- Use `space-xs` (4px) and `space-sm` (8px) for tightly coupled interface clusters: checkbox-to-label pairs, inline pill elements, and input inner vertical padding.
- Use `space-md` (16px) for interior card padding, row separations, and component grouping.
- Use `space-lg` (24px) and `space-xl` (40px) for container padding, section dividers, and lab transition blocks.

## Elevation & Depth

This system intentionally departs from heavy drop shadows to prioritize optical clarity, relying on surface tonal layering and crisp hairline strokes.

- **Level 0 (Flat Ground):** `#FFFFFF` canvas or `#F8F9FA` workspace backing with zero elevation.
- **Level 1 (Card & Module Resting):** Defined solely by a 1px uniform perimeter stroke of `#DADCE0` or `#E8EAED` against the `#FFFFFF` container background. A minimal diffuse shadow is introduced strictly to separate actionable cards from the canvas: `0 1px 3px 0 rgba(60, 64, 67, 0.08)`.
- **Level 2 (Hover & Interactive Focus):** Card elements lift slightly on hover via `0 4px 12px 0 rgba(60, 64, 67, 0.12)` accompanied by border enhancement (`#DADCE0`).
- **Level 3 (Overlays, Flyouts & Floating Tooltips):** Floating command prompts, contextual code hints, and modal dialogs receive `0 8px 24px -4px rgba(60, 64, 67, 0.16)` alongside a 1px `#DADCE0` perimeter boundary.
- **Focus Rings:** Never obscured or replaced with simple color changes. Keyboard and active form navigation must produce a high-contrast dual-layer focus treatment: a 2px offset with a 2px solid `#1A73E8` halo.

## Shapes

The shape system balances modern Material ergonomics with strict architectural order.

- **Primary Cards & Learning Modules:** Built with `rounded-lg` (16px) to frame multi-section lab components gracefully, producing distinct visual modules without visual harshness.
- **Interactive Controls (Buttons, Text Inputs, Dropdowns):** Configured with standard roundedness (8px) for balanced proportions and touch targets.
- **Status Badges, Filter Chips, & Bit Indicators:** Configured with continuous pill geometry or soft 4px-6px radii for compact binary registers.
- **Internal Nested Containers:** Must maintain optical harmony: nested elements carry a corner radius 4px smaller than their enclosing parent container (e.g., an 8px interactive sub-panel nested inside a 12px card).

## Components

### Buttons
- **Primary:** Filled `#1A73E8` background, white label, 8px radius, height 40px (desktop) / 44px (touch). Hover shifts to `#174EA6`. Active state scales down subtly (0.99).
- **Secondary (Tonal / Outlined):** Surface `#FFFFFF`, 1px solid border `#DADCE0`, text `#1A73E8`. Hover shifts background to `#F8F9FA` with border tint `#1A73E8`.
- **Text Button:** No border or resting background, text `#1A73E8`, padding horizontal 12px. Hover introduces `#F1F3F4` fill.

### Input Fields
- **Resting:** Background `#FFFFFF`, 1px solid `#DADCE0`, 8px radius, height 44px, typography `body-md` (`#202124`). Placeholders styled in `#80868B`.
- **Active / Focused:** 2px border `#1A73E8` without layout jump, overlaid with subtle glow `box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.2)`.
- **Validation (Error / Success):** Border shifts to `#D93025` with assistive feedback text in matching red. Successful validation turns stroke to `#188038`.
- **Technical Inputs (IP / Subnet / Hex):** Font family automatically shifts to `JetBrains Mono` (`code-md`), centered alignment where segmented masks are utilized.

### Cards & Lab Containers
- **Structure:** Surface `#FFFFFF`, stroke 1px `#E8EAED`, radius 12px to 16px.
- **Header Structure:** Clean separation via `#F8F9FA` top banner or 1px bottom border stroke `#E8EAED` separating title actions from active instructional space.
- **Interactive State:** Hover displays an elevation lift and increases border prominence to `#DADCE0`.

### Chips & Filter Tags
- **Selection Chips:** 32px height, 16px pill radius. Resting has `#F1F3F4` fill, `#5F6368` label. Selected switches to `#E8F0FE` fill, `#1A73E8` text, and 1px border `#1A73E8`.
- **Bit / Byte Flags:** Monospaced micro-chips, height 24px, radius 4px, background `#F8F9FA`, border 1px solid `#DADCE0`, text `code-sm`.

### Checkboxes & Radio Controls
- **Geometry:** Checkboxes use 4px radius; radios use pure circular shape (18px diameter).
- **States:** Inactive has 2px stroke `#5F6368`. Checked state transitions fill to `#1A73E8` with a crisp white glyph inside.

### Tabular Layouts (Technical Data)
- **Table Container:** Bound within a 12px rounded container with an outer `#DADCE0` perimeter.
- **Header Cells:** Background `#F8F9FA`, text `label-sm` in `#5F6368`, border bottom 1px `#DADCE0`.
- **Data Rows:** Background alternates cleanly (`#FFFFFF` to `#F8F9FA` on hover). Numerical and network values aligned using `JetBrains Mono`. Height standard 48px with cell padding horizontal `1rem`.