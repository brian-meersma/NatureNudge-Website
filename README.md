# Nature Nudge — marketing website

Static marketing site for the [Nature Nudge](https://apps.apple.com/us/app/nature-nudge/id6762029266)
iOS app. Plain HTML, CSS and a little progressive-enhancement JavaScript — no build step.

Published at <https://brian-meersma.github.io/NatureNudge-Website/>.

## Structure

```
index.html        Landing page
privacy.html      Privacy policy
style.css         All styles
script.js         Sticky-header hairline + scroll reveal (decorative only)
favicon.ico       The app icon, multi-resolution
robots.txt        Allows indexing, points at the sitemap
sitemap.xml       Two URLs
tools/
  make-og-image.py          Regenerates the link-preview images
assets/
  app-icon.png              512px app icon (light appearance)
  favicon-*.png             16/32/48/192/512 app icon, for browser tabs
  apple-touch-icon.png      180px home-screen icon, opaque as iOS requires
  og-image.jpg              1200x630 link preview
  og-image-square.jpg       1200x1200 link preview
  hero-photo.jpg            The app's own onboarding welcome photo
  app-store-badge-*.svg     Apple's official US badges (white + black lockups)
  screens/                  Device screenshots, 720px wide
```

## Link previews

`assets/og-image.jpg` (1200x630) is what iMessage, Twitter/X, Slack, Discord,
Facebook and LinkedIn render. `og-image-square.jpg` (1200x1200) is listed second
for the handful of clients that prefer a square. Both are built from the
`05-pair-tight` hero in `~/Downloads/Nature Nudge Hero 2` by:

```bash
python3 tools/make-og-image.py
```

Edit the script, not the JPEGs. It needs Pillow and the source art on disk.

## Design

The palette mirrors the app: deep indigo night (`--ink: #0B0E24`) and sunrise
amber (`--amber: #F59A2E`).

Sections alternate between two token families:

- **The dark canvas** (`--ink`, `--on-dark`, `--line-dark`) drives the hero,
  feature band, CTA and footer. It is *identical in both colour schemes* — those
  bands are always dark, because that is the brand.
- **The surface canvas** (`--surface`, `--surface-alt`, `--on-surface`,
  `--accent-ink`, `--line`, `--card-surface`, `--on-accent`) drives everything
  else, and every one of those tokens flips inside the single
  `@media (prefers-color-scheme: dark)` block at the top of `style.css`.

That is the whole of dark mode — no component rule mentions a scheme. To add a
colour, add a token to both blocks rather than hardcoding a hex in a rule.

`--accent-ink` is the amber that is legible against the surface: `#8A4A05` in
light mode, `#FFB65A` in dark. `--on-accent` is its counterpart for text sitting
*on* an amber chip, and flips the opposite way.

## Accessibility

Targets WCAG 2.1 Level A and AA. Verified with axe-core 4.13 (`wcag2a`, `wcag2aa`,
`wcag21a`, `wcag21aa`, `wcag22aa`, `best-practice`): **zero violations** on both
pages, in both light and dark mode.

- Every text/background pair is checked; the lowest ratio anywhere on the site is
  5.93:1 against a 4.5:1 requirement.
- Hero and CTA text sits over a photo and gradient overlays, which axe cannot
  evaluate. Those were verified by compositing the layers and sampling the
  worst-case pixel under each text box — the lowest was 6.27:1.
- Skip link, visible `:focus-visible` rings, landmark regions, one `h1` per page,
  labelled sections, descriptive `alt` text on every screenshot, decorative art
  hidden from assistive tech.
- No horizontal scrolling down to a 320px viewport; checked at 320, 375, 393 and
  430 (iPhone SE through Pro Max).
- Tap targets are 44px or larger, except inline links inside sentences, which
  WCAG 2.2 exempts.
- `prefers-reduced-motion: reduce` disables all animation, transitions and smooth
  scrolling. `forced-colors: active` restores borders on flat surfaces.

When changing colours, re-check contrast in **both** schemes before shipping. When
adding a screenshot, give it an `alt` that describes the numbers and labels on
screen, not "app screenshot".

## Copy

Nature Nudge is behind a hard paywall. Nothing on this site may describe the app
as free, or imply the download does anything useful without a subscription.
Prices ($2.99/month, $19.99/year) are mirrored in the `SoftwareApplication`
structured data in `index.html` — update both together.

## Assets

Screenshots come from `~/Downloads/Nature Nudge App Store Screenshots/Raw device
screenshots`, downscaled to 720px wide. The App Store badges are Apple's official
US artwork — do not redraw, recolour or crop them. The white lockup is used on the
dark sections; the black lockup is included for any future light-background use.

## Local preview

```bash
python3 -m http.server 4173 --directory website
```

Then open <http://localhost:4173>.

## Deploying

GitHub Pages serves `main` directly. Push to `main` and the site updates.
