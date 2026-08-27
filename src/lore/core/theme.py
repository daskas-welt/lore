"""shadcn Theming for Lore — neutral baseColor, CSS variables (src: ui.shadcn.com/docs/theming).
Default theme scaffold (neutral) — :root / .dark — oklch + hex fallback for Textual TUI.
"""

# shadcn default neutral theme — @import "tailwindcss"; @import "shadcn/tailwind.css";
# @custom-variant dark (&:is(.dark *));
# cssVariables: true, baseColor: neutral, radius: 0.625rem
# TUI uses hex fallbacks (Textual has no oklch); oklch kept as reference in comments.

# :root — light
# --background: oklch(1 0 0)               #F7F6F2 (warm paper, overrides neutral white)
# --foreground: oklch(0.145 0 0)           #16150F (warm ink, overrides neutral)
# --card: oklch(1 0 0)                     #F7F6F2
# --card-foreground: oklch(0.145 0 0)      #16150F
# --popover: oklch(1 0 0)                  #F7F6F2
# --popover-foreground: oklch(0.145 0 0)   #16150F
# --primary: oklch(0.205 0 0)              #171717 (neutral-900)
# --primary-foreground: oklch(0.985 0 0)   #fafafa (neutral-50)
# --secondary: oklch(0.97 0 0)             #f5f5f5 (neutral-100)
# --secondary-foreground: oklch(0.205 0 0)
# --muted: oklch(0.97 0 0)
# --muted-foreground: oklch(0.556 0 0)     #737373 (neutral-500)
# --accent: oklch(0.97 0 0)
# --accent-foreground: oklch(0.205 0 0)
# --destructive: oklch(0.577 0.245 27.325) #ef4444
# --border: oklch(0.922 0 0)               #e5e5e5 (neutral-200)
# --input: oklch(0.922 0 0)
# --ring: oklch(0.708 0 0)                 #a3a3a3 (neutral-400)
# --chart-1..5, --sidebar* etc — see below

LIGHT = {
    # core — background/foreground pairs (token convention)
    "background": "#F7F6F2",
    "foreground": "#16150F",
    "card": "#F7F6F2",
    "cardForeground": "#16150F",
    "popover": "#F7F6F2",
    "popoverForeground": "#16150F",
    "primary": "#16150F",
    "primaryForeground": "#F7F6F2",
    "secondary": "#f5f5f5",
    "secondaryForeground": "#16150F",
    "muted": "#f5f5f5",
    "mutedForeground": "#16150F",
    "accent": "#f5f5f5",
    "accentForeground": "#16150F",
    "destructive": "#ef4444",
    "destructiveForeground": "#fafafa",
    "border": "#e5e5e5",
    "input": "#e5e5e5",
    "ring": "#a3a3a3",
    "chart1": "#f59e0b",
    "chart2": "#06b6d4",
    "chart3": "#3b82f6",
    "chart4": "#10b981",
    "chart5": "#8b5cf6",
    "sidebar": "#F7F6F2",
    "sidebarForeground": "#16150F",
    "sidebarPrimary": "#171717",
    "sidebarPrimaryForeground": "#F7F6F2",
    "sidebarAccent": "#f5f5f5",
    "sidebarAccentForeground": "#16150F",
    "sidebarBorder": "#e5e5e5",
    "sidebarRing": "#a3a3a3",
    "radius": "0.625rem",
    # aliases for legacy paper/ink code — map to background/foreground
    "paper": "#F7F6F2",
    "paper2": "#f5f5f5",
    "paper_press": "#e5e5e5",
    "ink": "#16150F",
    "ink2": "#16150F",
    "ink3": "#16150F",
    "rule": "#e5e5e5",
    "rule_soft": "#f5f5f5",
    "accent_legacy": "#16150F",
    "success": "#737373",
    # oklch references (for CSS generation / create preview)
    "oklch": {
        "background": "oklch(1 0 0)",
        "foreground": "oklch(0.145 0 0)",
        "primary": "oklch(0.205 0 0)",
        "secondary": "oklch(0.97 0 0)",
        "mutedForeground": "oklch(0.556 0 0)",
        "border": "oklch(0.922 0 0)",
        "ring": "oklch(0.708 0 0)",
        "destructive": "oklch(0.577 0.245 27.325)",
    },
}

# .dark — dark overrides same tokens
# --background: oklch(0.145 0 0)           #0a0a0a
# --foreground: oklch(0.985 0 0)           #fafafa
# --card: oklch(0.205 0 0)                 #171717
# --primary: oklch(0.922 0 0)              #e5e5e5
# --secondary/muted/accent: oklch(0.269 0 0) #262626 (neutral-800)
# --border: oklch(1 0 0 / 10%)             #ffffff1a (white at 10%)
# --input: oklch(1 0 0 / 15%)
# --destructive: oklch(0.704 0.191 22.216) #ff6467
DARK = {
    "background": "#0a0a0a",
    "foreground": "#fafafa",
    "card": "#171717",
    "cardForeground": "#fafafa",
    "popover": "#171717",
    "popoverForeground": "#fafafa",
    "primary": "#e5e5e5",
    "primaryForeground": "#171717",
    "secondary": "#262626",
    "secondaryForeground": "#fafafa",
    "muted": "#262626",
    "mutedForeground": "#a3a3a3",
    "accent": "#262626",
    "accentForeground": "#fafafa",
    "destructive": "#ff6467",
    "destructiveForeground": "#171717",
    "border": "#262626",  # oklch(1 0 0 / 10%) ≈ #262626 on dark
    "input": "#404040",  # oklch(1 0 0 / 15%) ≈ #404040
    "ring": "#737373",
    "chart1": "#6366f1",
    "chart2": "#22d3ee",
    "chart3": "#fbbf24",
    "chart4": "#a78bfa",
    "chart5": "#f472b6",
    "sidebar": "#171717",
    "sidebarForeground": "#fafafa",
    "sidebarPrimary": "#6366f1",
    "sidebarPrimaryForeground": "#fafafa",
    "sidebarAccent": "#262626",
    "sidebarAccentForeground": "#fafafa",
    "sidebarBorder": "#262626",
    "sidebarRing": "#737373",
    "radius": "0.625rem",
    # legacy aliases
    "paper": "#0a0a0a",
    "paper2": "#171717",
    "paper_press": "#262626",
    "ink": "#fafafa",
    "ink2": "#a3a3a3",
    "ink3": "#737373",
    "rule": "#262626",
    "rule_soft": "#262626",
    "accent_legacy": "#fafafa",
    "success": "#a3a3a3",
    "oklch": {
        "background": "oklch(0.145 0 0)",
        "foreground": "oklch(0.985 0 0)",
        "primary": "oklch(0.922 0 0)",
        "secondary": "oklch(0.269 0 0)",
        "mutedForeground": "oklch(0.708 0 0)",
        "border": "oklch(1 0 0 / 10%)",
        "ring": "oklch(0.556 0 0)",
        "destructive": "oklch(0.704 0.191 22.216)",
    },
}

# Radius scale — derived from --radius (0.625rem = 10px)
# --radius-sm: calc(var(--radius) * 0.6)  → 0.375rem (6px)
# --radius-md: calc(var(--radius) * 0.8)  → 0.5rem (8px)
# --radius-lg: var(--radius)              → 0.625rem (10px)
# --radius-xl: calc(var(--radius) * 1.4)  → 0.875rem (14px)
# etc — components use radius-lg by default (cards, inputs, buttons)
RADIUS = {
    "radius": "0.625rem",
    "radiusSm": "0.375rem",
    "radiusMd": "0.5rem",
    "radiusLg": "0.625rem",
    "radiusXl": "0.875rem",
    "radius2xl": "1.125rem",
    "radius3xl": "1.375rem",
    "radius4xl": "1.625rem",
}

# Typography — Geist Sans/Mono per shadcn/typeset — size/leading/flow + base-nova
TYPOGRAPHY = {
    "font_sans": "Geist Sans",
    "font_mono": "Geist Mono",
    "h1": {
        "size": "2.25rem",
        "weight": "800",
        "tracking": "-0.025em",
        "leading": "1.1",
    },
    "h2": {
        "size": "1.875rem",
        "weight": "600",
        "tracking": "-0.025em",
        "leading": "1.2",
    },
    "h3": {
        "size": "1.5rem",
        "weight": "600",
        "tracking": "-0.025em",
        "leading": "1.25",
    },
    "h4": {
        "size": "1.25rem",
        "weight": "600",
        "tracking": "-0.025em",
        "leading": "1.3",
    },
    "p": {"leading": "1.75", "mt": "1.5rem"},
    "small": {"size": "0.875rem", "weight": "500", "leading": "1"},
    "muted": {"color": "mutedForeground"},
}
