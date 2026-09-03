---
name: Synthetic Intelligence Audit Console
colors:
  surface: '#0f131b'
  surface-dim: '#0f131b'
  surface-bright: '#353941'
  surface-container-lowest: '#0a0e15'
  surface-container-low: '#181c23'
  surface-container: '#1c2027'
  surface-container-high: '#262a32'
  surface-container-highest: '#31353d'
  on-surface: '#dfe2ed'
  on-surface-variant: '#bacbb9'
  inverse-surface: '#dfe2ed'
  inverse-on-surface: '#2d3038'
  outline: '#859585'
  outline-variant: '#3c4a3d'
  surface-tint: '#18e376'
  primary: '#46fc8b'
  on-primary: '#003918'
  primary-container: '#05df72'
  on-primary-container: '#005d2b'
  inverse-primary: '#006d34'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffd8ac'
  on-tertiary: '#472a00'
  tertiary-container: '#ffb34e'
  on-tertiary-container: '#714600'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#62ff96'
  primary-fixed-dim: '#18e376'
  on-primary-fixed: '#00210b'
  on-primary-fixed-variant: '#005226'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0f131b'
  on-background: '#dfe2ed'
  surface-variant: '#31353d'
typography:
  display-lg:
    fontFamily: inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.03em
  display-lg-mobile:
    fontFamily: inter
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0em
  label-code-md:
    fontFamily: geist
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0em
  label-code-sm:
    fontFamily: geist
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.02em
  label-ui:
    fontFamily: inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  space-xxs: 0.125rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-base: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
  gutter-table: 0.75rem
  margin-screen: 1.5rem
---

## Brand & Style

This design system establishes a mission-critical, high-density cockpit environment tailored for enterprise AI oversight, real-time conversational auditing, and automated conversational QA telemetry. Built for engineers, QA directors, and operations teams monitoring autonomous customer-facing voice and text agents, the system prioritizes surgical precision, instant defect legibility, and high-tech computational authority.

The aesthetic fuses **Modern Technical Minimalism** with **Tactical Cybernetic Accents**:
- Ultra-deep carbon baselines maximize contrast and eliminate ocular fatigue during extended shifts.
- Electric neon emerald signatures signal operational health, valid inference paths, and verified compliance benchmarks, directly tethered to brand heritage.
- Translucent surface layering, hairline borders, and subtle diffuse electromagnetic backlights denote system states without cluttering data-heavy analytical tables.
- Monospaced typography handles mathematical parity, timestamps, agent latency, and raw JSON payloads, while razor-sharp grotesk typography directs navigation and status narratives.

## Colors

The palette operates in an absolute dark-mode discipline. Layered slate and carbon foundations isolate visual noise and allow critical agent telemetry to emerge with sharp functional hierarchy.

### Functional Tonal Hierarchy
- **Canvas Base (`#090D14`):** Pure foundational substrate for zero-glare viewing and deep contrast.
- **Surface Layer 1 (`#0F172A`):** Core application panels, telemetry dockings, and primary container backgrounds.
- **Surface Layer 2 (`#1E293B`):** Hover states, active table rows, secondary toolbars, and structural dividers.
- **Hairline Borders (`#1E293B` / `rgba(30, 41, 59, 0.8)`):** Explicit boundaries defining high-density data matrices without visual mass.

### Signal & Alert Spectrum
- **Brand Neon Emerald (`#05DF72`):** Primary interactive targets, operational health (100% QA pass rate), agent latency within normal variance (<250ms), and live monitoring indicators.
- **Deep Emerald (`#10B981`):** Subdued status chips, badges, positive metrics trends, and active filters.
- **Telemetry Warning Amber (`#F59E0B`):** Confidence score degradation (between 60%–79%), soft policy drift, and non-blocking conversation anomalies.
- **Escalation Crimson (`#EF4444`):** Hallucination flags, sentiment breakdown alerts, compliance violations, and immediate human-in-the-loop triggers.

### Text Contrast Tiers
- **Primary Text (`#F8FAFC`):** Direct scores, payload metrics, and active header copy.
- **Secondary Text (`#94A3B8`):** Attribute labels, metadata keys, and secondary navigation items.
- **Muted Text (`#64748B`):** Timestamps, deactivated controls, and column guidelines.

## Typography

Typography balances rapid scanning with dense metric comprehension. 

- **Primary Interface Typeface (`Inter`):** Handles all core navigation, headings, and analytical narrative text. High x-height, neutral tone, and tight proportional kerning preserve visual clarity in multi-pane layouts.
- **Technical & Metric Subsystem (`Geist`):** Monospaced numeric alignment guarantees that real-time tables, timestamps, session IDs, confidence score percentages, and agent latency values retain absolute columnar alignment during continuous streaming updates.
- **Casing Rules:** Table headers, metric tags, and status chips apply uppercase transformations with expanded letter tracking (`0.04em`) to establish visual distinction against dense analytical data.

## Layout & Spacing

The layout is built upon an 8px technical rhythm with 4px sub-increments designed for maximum data density and minimal dead screen space.

### Grid & Composition Strategy
- **Master Canvas Structure:** Fixed collapsible left telemetry sidebar (64px mini / 260px expanded), fluid central telemetry canvas, and an optional 380px inspector drawer for conversational audio scrubbers, sentiment graphs, and defect JSON dumps.
- **Data Densities:**
  - **Compact Mode (Table rows, real-time audit logs):** 36px row height, 12px horizontal cell padding.
  - **Standard Mode (Card panels, metric overviews):** 16px to 24px internal container padding.
- **Breakpoints:**
  - **Desktop / Wallboard (`≥ 1440px`):** Multi-column multi-agent streaming view; simultaneous display of call trace, audio waveform, and confidence timeline.
  - **Laptop (`1024px – 1439px`):** Flexible 12-column system, collapsible inspector drawer into sliding overlay.
  - **Tablet / Mobile (`< 1024px`):** Single column stacked overview; audio waveform and detailed trace collapse into sheet drawers.

## Elevation & Depth

Visual hierarchy uses **tonal layering**, **semi-permeable glassmorphism**, and **tactical photon glows** rather than standard drop shadows. In an ultra-dark UI, diffuse shadows disappear against `#090D14`, making surface lighting and outline contrast the primary drivers of depth.

### Layer Architecture
1. **Base Substrate (`#090D14`):** The non-interactive infinite background plane.
2. **Standard Surface (`#0F172A` with 1px border of `#1E293B`):** Primary data containers, audit log panels, and telemetry matrices.
3. **Elevated & Hover Overlay (`#1E293B` or `rgba(15, 23, 42, 0.75)` with `backdrop-filter: blur(12px)`):** Fixed navigation headers, floating control bars, and contextual tooltips.
4. **Modal / Diagnostic Inspect Surface (`#0F172A` + `rgba(5, 223, 114, 0.08)` hairline halo):** High-priority inspection states.

### Luminescence & Glow Accents
- **System Normal Glow:** `box-shadow: 0 0 16px -2px rgba(5, 223, 114, 0.25)` applied to primary active switches, live agent nodes, and 100% compliance markers.
- **Anomaly Pulse:** `box-shadow: 0 0 16px -1px rgba(239, 68, 68, 0.35)` applied to agent failure chips, escalation triggers, and sentiment collapse boundaries.

## Shapes

The design uses **Soft Precision (`roundedness: 1`)** geometry. 
- Component containers, cards, and modal dialogs utilize `4px` to `8px` radii (`rounded-md` to `rounded-lg`).
- Form elements, table action tags, and status pills retain a structural, calibrated feel (`4px` for inputs and code wrappers; full pill `9999px` reserved strictly for live state indicator chips).
- Hairline `1px` structural borders are present across all cards, table cells, and panel intersections to sustain architectural crispness.

## Components

### Buttons & Actions
- **Primary Cybernetic CTA:** Background `#05DF72`, label text `#090D14` (`font-weight: 600`), 0 0 12px rgba(5, 223, 114, 0.3) aura on hover. Radii: 4px.
- **Secondary Diagnostic Button:** Background `rgba(30, 41, 59, 0.6)`, border `1px solid #1E293B`, text `#F8FAFC`. On hover: border-color `#05DF72`, background `#1E293B`.
- **Destructive / Escalation Button:** Background `rgba(239, 68, 68, 0.1)`, border `1px solid rgba(239, 68, 68, 0.4)`, text `#EF4444`. Hover: background `#EF4444`, text `#FFFFFF`.

### Telemetry Tables & Log Views
- **Header:** Sticky `#0F172A`, 1px solid `#1E293B`, uppercase `label-code-sm` font, text `#64748B`.
- **Data Rows:** Alternating micro-shading or uniform hairline borders. Active row selection applies a 2px left border accent in `#05DF72` with background `rgba(5, 223, 114, 0.03)`.
- **Data Alignment:** Numbers, percentages, and latency metrics right-aligned in `Geist Mono`; status chips and agent identification left-aligned.

### Status Indicators & Badges
- **Pill Architecture:** Height 22px, padding 2px 8px, font `label-code-sm`.
- **Operational / Passed:** Background `rgba(5, 223, 114, 0.12)`, border `1px solid rgba(5, 223, 114, 0.4)`, text `#05DF72`. Features a 6px pulsating dot.
- **Anomaly Warning:** Background `rgba(245, 158, 11, 0.12)`, border `1px solid rgba(245, 158, 11, 0.4)`, text `#F59E0B`.
- **Defect Escalate:** Background `rgba(239, 68, 68, 0.12)`, border `1px solid rgba(239, 68, 68, 0.4)`, text `#EF4444`.

### Input Fields & Filter Triggers
- Height: 36px compact. Background `#090D14`. Border: `1px solid #1E293B`.
- Focus state: Border transitions to `#05DF72` with a `0 0 0 1px #05DF72` inner focus ring. Placeholder text `#64748B`.

### Audio Waveform & Conversation Trace
- **Speaker Scrub Track:** Background `#090D14`, waveform segments mapped in dual track (Agent: `#05DF72`, Customer: `#94A3B8`). Defect flags marked with `#EF4444` vertical bookmark pins with timestamped popover cards.