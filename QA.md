# Verification — 2026-10-10

## Persian charging cable correction

- Persian charging accessories are anchored using the native left offsets (144px desktop, 34px tablet, 22px mobile); only the accessory image is mirrored, keeping watch faces readable.
- The enhanced animation starts at a positive horizontal offset (400px desktop, 280px medium), bringing the cable in from the right. Browser scrolling confirmed the desktop start at +400px and connected position at 0px.
- Desktop inspection at 1600 × 1000 confirmed the cable begins at x=944 while the Persian copy ends at x=800, with no overlap at the connected state.
- Inspected the static layout at 1024 × 900 and 390 × 844: cable reaches the watch from the right, below the copy. Document width equals viewport width.
- Watch-layer images now match their picture dimensions in Persian, correcting the large intrinsic image sizes that broke alignment in the mobile fallback.
- `npm run check` passes. Screenshots: `artifacts/battery-rtl-desktop.jpg` and `artifacts/battery-rtl-mobile.jpg`.

## Requested fine-print removal

- Both generated pages omit the entire `.ac-gf-sosumi` footer section and every `#footnote-` link and its inline marker.
- Removal runs after localization so joined text nodes keep their Persian translations.
- Inspected the rendered Persian desktop footer at 1600 × 1000: the normal directory, shopping links and copyright remain; no fine-print section is present. Pinar remains the computed footer font.
- DOM checks found zero fine-print sections and zero footnote links; document widths match 1600 and 390 pixel viewports. Both generated HTML files passed the same removal checks and retained the normal footer.
- `npm run check` passes. Updated desktop evidence: `artifacts/footer-clean.jpg`.

## Persian localization

- `/` serves static Persian HTML with `lang="fa"` and `dir="rtl"`; `/en/` serves English with `lang="en-US"` and `dir="ltr"`.
- 618 source strings have explicit translations or preserved service/domain names, including marketing copy, technical descriptions, legal conditions, menus, image descriptions and accessibility labels. Native color-specific accessibility maps are localized too.
- Pinar DS4 is self-hosted in Light, Regular, Medium and Bold. Browser checks confirmed the actual computed Pinar font and loaded glyphs.
- Inspected widths: 320 × 780, 390 × 844, 1024 × 900 and 1600 × 1000. The document width matches the viewport at each width.
- The mobile language selector sits between navigation groups without covering Search or Bag. Persian mobile menu labels and the dynamic Close label render correctly.
- Switched Persian → English → Persian through the visible language control; English restores SF Pro and LTR. Search parameters and section fragments are preserved.
- Highlights selection tested with Sleep Score and Health app; both selected state and visible panel position were verified. Native RTL scrolling is retained. Media composition stays in its original physical direction while captions use Persian text flow.
- Product viewer: Health sensors opens/closes in Persian; Finishes switches to Midnight with matching Persian text and checked radio. On desktop, the image composition is shifted left to leave the right-side controls clear.
- Trade In information dialog opens with Persian heading, body, link and Close label. The RTL close SVG offset is corrected.
- All embedded native scripts match the retained English source. `npm run check` passes for local resources, responsive media, both locale routes and four Pinar font weights.
- Browser screenshots: `artifacts/fa-desktop.png` and `artifacts/fa-mobile.png`.

## Original English reconstruction

- Reference viewport: 1600 × 1000. Logo and headline aligned at x=170; hero ends at the reference viewport boundary. Original five-watch video used, with a stable reference frame at 2.8 seconds.
- Responsive inspection: 390 × 844 and 1024 × 900. No horizontal page overflow; mobile purchase bar and tablet content render correctly.
- SF Pro fonts loaded from local files.
- Manual Highlights tab selection confirmed through `aria-selected`.
- Product viewer: Health sensors opens real detail content; Close returns to the viewer; Finishes switches to Midnight with matching text and image.
- Apple Trade In opens the native information dialog.
- Sticky local product navigation appears after scrolling.
- Missing rendered images check returned an empty list.
- The native localnav animation anchor was repaired after replacing the current hero. No new native initialization errors appeared after this repair.
- Static validation checks every HTML/CSS asset reference and each configured responsive video variant.

## Scope and remaining differences

The available Refero evidence covers the first desktop viewport. Lower sections come from the current official page, so a full historical or mobile pixel comparison is unavailable. The film remains animated in normal browsing; `?reference=1` pauses a known matching composition for review. The paused control consequently shows Play.

Two lower-section videos (battery at small, fitness at large) use their original 1x variants because their 2x downloads timed out. Other available 2x variants and all hero 2x variants are local. This changes media resolution for those two cases, not layout or interaction.

No purchase, payment, account login or remote form submission was performed. Those destinations link to Apple's official site.
