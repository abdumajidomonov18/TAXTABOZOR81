---
name: UstaYordam
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#524534'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#857462'
  outline-variant: '#d7c3ae'
  surface-tint: '#835500'
  primary: '#835500'
  on-primary: '#ffffff'
  primary-container: '#f5a623'
  on-primary-container: '#644000'
  inverse-primary: '#ffb955'
  secondary: '#555f6f'
  on-secondary: '#ffffff'
  secondary-container: '#d6e0f3'
  on-secondary-container: '#596373'
  tertiary: '#555f6d'
  on-tertiary: '#ffffff'
  tertiary-container: '#adb7c7'
  on-tertiary-container: '#3e4856'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffddb4'
  primary-fixed-dim: '#ffb955'
  on-primary-fixed: '#291800'
  on-primary-fixed-variant: '#633f00'
  secondary-fixed: '#d9e3f6'
  secondary-fixed-dim: '#bdc7d9'
  on-secondary-fixed: '#121c2a'
  on-secondary-fixed-variant: '#3d4756'
  tertiary-fixed: '#d9e3f4'
  tertiary-fixed-dim: '#bdc7d8'
  on-tertiary-fixed: '#121c28'
  on-tertiary-fixed-variant: '#3e4755'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  margin-main: 16px
  gutter-grid: 12px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style
The design system is engineered for a construction materials delivery platform that bridges industrial utility with modern e-commerce convenience. The personality is **Reliable, Efficient, and Accessible**, tailored for contractors and homeowners who need heavy materials delivered with precision.

The visual style follows a **Modern Corporate** aesthetic with a **Tactile** edge. It utilizes generous whitespace to reduce cognitive load in a data-heavy catalog, while employing high-contrast accents to signal action. The interface must feel like a native mobile tool—robust enough for a construction site, yet polished enough for a premium retail experience.

## Colors
The palette is rooted in construction industry semiotics. 
- **Primary Amber (#F5A623)**: Reserved for primary call-to-actions, active navigation states, and progress indicators. It provides high visibility against the neutral background.
- **Deep Charcoal (#1F2937)**: Used for high-level headings and primary text to ensure maximum legibility and an authoritative feel.
- **Off-white (#FAFAFA)**: The primary canvas color, creating a clean, "uncluttered" environment that allows product photography to stand out.
- **System States**: Success Green (#10B981) for order confirmations and Muted Red (#EF4444) for inventory errors or cancellations.

## Typography
The system uses **Inter** for its systematic, utilitarian clarity. It is highly legible on small mobile screens. 
- **Headings**: Use bold weights (700) and tight letter-spacing for a strong, "built" feel. 
- **Body Text**: Uses a medium-high line height (1.5x) to ensure technical product descriptions (measurements, weights) are easy to parse.
- **Localization**: All styles are optimized for the Uzbek Latin script, ensuring no descender clipping in high-density product lists.

## Layout & Spacing
The layout is optimized for a **390px viewport (Mobile-first)**.
- **Grid System**: A 2-column product grid with 12px gutters. This allows users to compare items side-by-side without sacrificing touch targets.
- **Margins**: A 16px safe area is maintained on the left and right of the screen for all text and container elements.
- **Vertical Rhythm**: Content blocks are separated by 24px increments, while internal card elements use 8px or 12px spacing to maintain tight groupings.

## Elevation & Depth
This design system uses **Tonal Layering** combined with **Ambient Shadows** to create a structured hierarchy:
- **Level 0 (Base)**: The Off-white (#FAFAFA) background.
- **Level 1 (Cards/Inputs)**: Pure White (#FFFFFF) surfaces with a subtle, very diffused shadow: `0px 4px 12px rgba(31, 41, 55, 0.05)`.
- **Level 2 (Floating/Active)**: Used for bottom navigation bars and sticky "Add to Cart" buttons. These use a more pronounced shadow: `0px -2px 10px rgba(31, 41, 55, 0.08)` to indicate they sit above the scrollable content.
- **Overlays**: Semi-transparent backdrops for modals use a 40% opacity of Deep Charcoal.

## Shapes
Shapes are defined by a **"Soft-Industrial"** logic. While construction is often about hard angles, the digital experience uses rounded corners to feel modern and user-friendly.
- **Standard UI (Buttons, Inputs)**: 8px (0.5rem) radius.
- **Containers (Product Cards, Modals)**: 16px (1rem) radius.
- **Selection Indicators (Chips)**: Fully rounded (pill-shaped) for maximum contrast against rectangular cards.

## Components
- **Bottom Navigation**: 4-tab bar (Bosh sahifa, Savatcha, Buyurtmalar, Profil). Icons use 24px size. Active state: Primary Amber icon + label; Inactive: Tertiary Grey.
- **Product Cards**: 2-column layout. Top-aligned image (aspect ratio 1:1), followed by product name (Body-md Bold), price (Body-lg Bold in Amber), and a small "plus" icon button for quick add.
- **Primary Buttons**: Full-width, 48px height, Primary Amber background, Deep Charcoal text (for contrast).
- **Search & Filter**: Search bar with 8px corner radius. A persistent "Filter" icon sits inside the right edge of the search bar, styled with a subtle vertical divider.
- **Status Badges**: Small, rounded tags (e.g., "Omborda bor" for In Stock) using success green with 10% opacity background and 100% opacity text.
- **Input Fields**: Outlined style with 1px border (#E5E7EB). On focus, border changes to Primary Amber with a 2px stroke.