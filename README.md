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
  app-store-badge-*.svg     Apple's official US badges (black is the one in use)
  screens/                  Device screenshots, 720px wide
```

## Link previews

`assets/og-image.jpg` (1200x630) is the single link preview, built from the
`05-pair-tight` hero in `~/Downloads/Nature Nudge Hero 2` by:

```bash
python3 tools/make-og-image.py
```

Edit the script, not the JPEG. It needs Pillow and the source art on disk.

**One image, centre-composed, and it must stay that way.** An earlier version
also offered a 1200x1200 `og:image` as a second tag. iMessage chose the square,
cropped its left edge off, and rendered a card reading "e Nudge" over a sliced
headline. Two lessons, both baked into the script now:

- Advertise exactly one `og:image`. A second tag is an invitation for a client
  to pick the one you did not design for.
- Clients crop the preview to whatever their card wants, so keep everything that
  matters inside the centre square (x 285-915). The wordmark, headline and
  phones are all centred; only gradient reaches the edges. `tools/` has no test
  for this, so eyeball a centre-square crop after any change.

The phone art is a rectangular crop of painted sunrise, much lighter than the
ink ground, so `sink()` pulls its edges toward ink and `feather()` ramps all four
sides. Without both it reads as a photo pasted onto the card.

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

The hero background is built rather than photographed. An earlier draft used the
app's onboarding photo behind a veil; on an iPhone it read as murky noise and
competed with the product art. It is now a night-to-dawn gradient with the warm
horizon sitting behind the device, plus a 5%-opacity grain layer that stops the
large soft ramps banding on 8-bit displays. The only image in the hero is the
product. `--dawn-x` moves the horizon to follow the device, which is centred on
mobile and right-hand from 940px up.

`html` and `body` are painted `--ink`, not `--surface`. The header is sticky, so
at rest it sits *above* the hero over the page ground; with a cream body its
translucent bar picked that up and rendered as a grey slab detached from the
hero. Ink behind it also means top overscroll matches the header instead of
flashing cream.

Above the fold the hero carries one primary action. The App Store badge is the
CTA; "See how it works" is a text link rather than a second pill, and the trust
line is three plain phrases rather than three icon rows, which on an iPhone
stacked into a wall of text before the product was ever visible.

## Accessibility

Targets WCAG 2.1 Level A and AA. Verified with axe-core 4.13 (`wcag2a`, `wcag2aa`,
`wcag21a`, `wcag21aa`, `wcag22aa`, `best-practice`): **zero violations** on both
pages, in both light and dark mode.

- Every text/background pair is checked; the lowest ratio anywhere on the site is
  5.93:1 against a 4.5:1 requirement.
- Hero and CTA text sits over gradients, and the sticky header over a blurred
  backdrop; axe cannot evaluate any of those and reports them as "incomplete".
  They were verified by hand instead: the hero by rebuilding its gradient stack
  on a canvas and sampling the worst-case pixel under every text box (lowest
  11.21:1), the header by compositing it against each backdrop it can sit on
  (lowest 10.18:1), the CTA against its amber bloom (lowest 7.80:1).
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
US artwork; do not redraw, recolour or crop them. The **black** lockup is the one
in use: Apple names it the preferred badge for all marketing, and its grey border
is part of the artwork, drawn so it reads against a dark ground. The white lockup
is only an alternative for when black sits visually heavy, and is kept unused.
Apple also asks that the badge be legible but not dominant, which is why it is
132px in the header, 164px in the hero and 176px in the closing CTA rather than
as large as it will go.

## Local preview

```bash
python3 -m http.server 4173 --directory website
```

Then open <http://localhost:4173>.

## Deploying

GitHub Pages serves `main` directly. Push to `main` and the site updates.
