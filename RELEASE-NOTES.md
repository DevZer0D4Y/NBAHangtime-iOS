# NBA Hangtime 0.4.2

iOS build 7 · Windows x64 · iOS 16 or later

## Changes since 0.4.0

- Fix Windows Xbox input by reading buttons, sticks and triggers through XInput. Gameplay, controller setup and menus use the same polled input state.
- Improve iOS controller event delivery, including Menu/Start and gamepad routing on iOS 18 and later.
- Keep controller slots stable across reordering and disconnects. Controllers join as Player 1, Player 3, Player 2 and Player 4.
- Align Player 1 and Player 4 possession indicators and scoring flashes with their status plates.
- Restore camera tracking at both near-side corners. Limit the inbound view separately so it stays inside the available scenery at both court ends.
- Preserve live settings changes, including switching head size during gameplay. Normal, big and huge head settings apply to all four players.
- Strip private build paths and debug metadata from release binaries. Check packages for ROMs, signing credentials and development artifacts.
- Include license notices and matching source references in both binary packages.

## Downloads

- `NBA-Hangtime-Windows-x64.zip`
- `NBA-Hangtime-iOS.ipa` (unsigned; sign using your sideloading tool)
- `NBA-Hangtime-0.4.2-source.zip`

Each archive has a companion SHA-256 checksum. Game ROMs are not included; the complete arcade L1.1 set is required. See `SOURCE.md` for source and distribution notices.

## Validation

Windows and iOS release builds succeeded. ROM importer, controller routing, native XInput decoding, controller remapping, camera bounds, live widescreen switching, core bridge and release hygiene tests passed.

Physical Xbox testing on Windows and iOS and visual confirmation of the revised inbound view remain outstanding. This build is ready for release-candidate testing; those checks are needed before calling it fully verified on hardware.
