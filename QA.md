# Verification — 2026-10-10

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
