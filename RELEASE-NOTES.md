# NBA Hangtime 0.4.4

iOS build 9 · Windows x64 · iOS 16 or later

## Changes

- Match CRT curvature to the corrected ports: CURVATURE 1.0 with a 40% blend toward the flat image.
- Remove frame-artwork overscan and prevent outermost pixels from smearing beyond the curved screen.
- Fade the tube boundary into black with a 1.5-pixel edge mask.
- Generate the iOS and Windows CRT shaders from the same math.

## Downloads

- `NBA-Hangtime-iOS.ipa` — unsigned; sign with your sideloading tool.
- `NBA-Hangtime-Windows-x64.zip`
- `NBA-Hangtime-0.4.4-source.zip` — matching port and patched core source.

Companion SHA-256 checksums are included. Game ROMs are not included; the complete L1.1 arcade set is required. See `SOURCE.md` for source and license notices.

## Validation

Geometry regression checks cover the curvature values, symmetry, all four borders and edge fade. Windows and iOS release builds passed. OpenGL and Metal GPU tests passed shader compilation, rendering passes, black corners, image orientation, toggles and resizing. Package integrity and privacy checks passed before publication.

GPU tests ran on the Mac host. Visual confirmation on physical iOS and Windows devices remains pending.
